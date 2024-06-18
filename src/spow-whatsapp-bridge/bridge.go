// Copyright (c) 2021 Tulir Asokan
// Copyright (c) 2024 Mark Joshwel
//
// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

// from https://github.com/tulir/whatsmeow/commit/792d96fbe610bfbf1039ec3b8d3f37f630025aea

package main

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"mime"
	"os"
	"os/signal"
	"path"
	"strings"
	"sync/atomic"
	"syscall"
	"time"

	_ "github.com/mattn/go-sqlite3"
	"github.com/mdp/qrterminal/v3"
	"google.golang.org/protobuf/proto"

	"go.mau.fi/whatsmeow"
	"go.mau.fi/whatsmeow/appstate"
	waBinary "go.mau.fi/whatsmeow/binary"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/store"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	"go.mau.fi/whatsmeow/types/events"
	waLog "go.mau.fi/whatsmeow/util/log"
)

var cli *whatsmeow.Client
var log waLog.Logger

var logLevel = "INFO"
var debugLogs = flag.Bool("debug", false, "Enable debug logs?")
var dbDialect = flag.String("db-dialect", "sqlite3", "Database dialect (sqlite3 or postgres)")
var dbAddress = flag.String("db-address", "file:mdtest.db?_foreign_keys=on", "Database address")
var requestFullSync = flag.Bool("request-full-sync", false, "Request full (1 year) history sync when logging in?")
var pairRejectChan = make(chan bool, 1)

// s+ow-whatsapp-bridge: define important paths
var dataDir = path.Join(os.Getenv("HOME"), ".local", "share", "s+ow-whatsapp-bridge")
var sharetextPath = path.Join(os.Getenv("HOME"), ".cache", "s+ow", "message")

func main() {
	waBinary.IndentXML = true
	flag.Parse()

	if *debugLogs {
		logLevel = "DEBUG"
	}
	if *requestFullSync {
		store.DeviceProps.RequireFullSync = proto.Bool(true)
		store.DeviceProps.HistorySyncConfig = &waProto.DeviceProps_HistorySyncConfig{
			FullSyncDaysLimit:   proto.Uint32(3650),
			FullSyncSizeMbLimit: proto.Uint32(102400),
			StorageQuotaMb:      proto.Uint32(102400),
		}
	}
	log = waLog.Stdout("Main", logLevel, true)

	// s+ow-whatsapp-bridge: make and change dir
	err := os.MkdirAll(dataDir, os.ModePerm)
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: s+ow-whatsapp-bridge: Failed to create directory: %v", err)
		return
	}
	err = os.Chdir(dataDir)
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: s+ow-whatsapp-bridge: Failed to change directory: %v", err)
		return
	}

	dbLog := waLog.Stdout("Database", logLevel, true)
	storeContainer, err := sqlstore.New(*dbDialect, *dbAddress, dbLog)
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: Failed to connect to database: %v", err)
		return
	}
	device, err := storeContainer.GetFirstDevice()
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: Failed to get device: %v", err)
		return
	}

	cli = whatsmeow.NewClient(device, waLog.Stdout("Client", logLevel, true))
	var isWaitingForPair atomic.Bool
	cli.PrePairCallback = func(jid types.JID, platform, businessName string) bool {
		isWaitingForPair.Store(true)
		defer isWaitingForPair.Store(false)
		log.Infof("s+ow-whatsapp-bridge: Pairing %s (platform: %q, business name: %q). Type r within 3 seconds to reject pair", jid, platform, businessName)
		select {
		case reject := <-pairRejectChan:
			if reject {
				log.Infof("s+ow-whatsapp-bridge: Rejecting pair")
				return false
			}
		case <-time.After(3 * time.Second):
		}
		log.Infof("s+ow-whatsapp-bridge: Accepting pair")
		return true
	}

	ch, err := cli.GetQRChannel(context.Background())
	if err != nil {
		// This error means that we're already logged in, so ignore it.
		if !errors.Is(err, whatsmeow.ErrQRStoreContainsID) {
			log.Errorf("s+ow-whatsapp-bridge: Failed to get QR channel: %v", err)
		}
	} else {
		go func() {
			for evt := range ch {
				if evt.Event == "code" {
					qrterminal.GenerateHalfBlock(evt.Code, qrterminal.L, os.Stdout)
				} else {
					log.Infof("s+ow-whatsapp-bridge: QR channel result: %s", evt.Event)
				}
			}
		}()
	}

	cli.AddEventHandler(handler)
	err = cli.Connect()
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: Failed to connect: %v", err)
		return
	}

	c := make(chan os.Signal, 1)
	input := make(chan string)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		defer close(input)
		scan := bufio.NewScanner(os.Stdin)
		for scan.Scan() {
			line := strings.TrimSpace(scan.Text())
			if len(line) > 0 {
				input <- line
			}
		}
	}()

	// s+ow-whatsapp-bridge
	// - if 'login' in os.Args, we exit here
	for _, arg := range os.Args {
		if arg == "login" {
			for {
				select {
				case <-c:
					log.Infof("Interrupt received, exiting")
					cli.Disconnect()
					return
				case cmd := <-input:
					if len(cmd) == 0 {
						log.Infof("Stdin closed, exiting")
						cli.Disconnect()
						return
					}
				}
			}
		}
	}

	// - if using as cli
	args := os.Args[1:]
	if len(args) > 0 {
		handleCmd(strings.ToLower(args[0]), args[1:])
		return
	}

	// - else, "normal" operation:

	// - - read file ~/.cache/s+ow/message
	sharetext, err := os.ReadFile(sharetextPath)
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: Failed to open file: %v", err)
		return
	}

	// - - read JID targets from stdin
	targets := <-input
	split := strings.Split(targets, ",")
	for _, target := range split {
		// strip whitespace
		target = strings.TrimSpace(target)

		// check if prefixed with "wa:"
		if strings.HasPrefix(target, "wa:") {
			// send message to group
			recipient, ok := parseJID(target[3:])
			if !ok {
				return
			}

			// reference the "send" case in handleCmd as a single source of truth
			msg := &waProto.Message{Conversation: proto.String(strings.TrimSpace(string(sharetext)))}
			resp, err := cli.SendMessage(context.Background(), recipient, msg)
			if err != nil {
				log.Errorf("s+ow-whatsapp-bridge: Error sending message: %v", err)
			} else {
				log.Infof("s+ow-whatsapp-bridge: Message sent (server timestamp: %s)", resp.Timestamp)
			}
		}
	}

	log.Infof("s+ow-whatsapp-bridge: Exiting")
	cli.Disconnect()
	return
}

func parseJID(arg string) (types.JID, bool) {
	if arg[0] == '+' {
		arg = arg[1:]
	}

	if !strings.ContainsRune(arg, '@') {
		return types.NewJID(arg, types.DefaultUserServer), true
	}

	recipient, err := types.ParseJID(arg)
	if err != nil {
		log.Errorf("s+ow-whatsapp-bridge: Invalid JID %s: %v", arg, err)
		return recipient, false
	} else if recipient.User == "" {
		log.Errorf("s+ow-whatsapp-bridge: Invalid JID %s: no server specified", arg)
		return recipient, false
	}
	return recipient, true
}

func handleCmd(cmd string, args []string) {
	// s+ow-whatsapp-bridge: we only need the bare minimum:
	// - account-related: pair-phone, logout, reconnect
	// - chat-related: list, send
	switch cmd {
	case "pair-phone":
		if len(args) < 1 {
			log.Errorf("s+ow-whatsapp-bridge: Usage: pair-phone <number>")
			return
		}
		linkingCode, err := cli.PairPhone(args[0], true, whatsmeow.PairClientChrome, "Chrome (Linux)")
		if err != nil {
			panic(err)
		}
		fmt.Println("Linking code:", linkingCode)
	case "reconnect":
		cli.Disconnect()
		err := cli.Connect()
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Failed to connect: %v", err)
		}
	case "logout":
		err := cli.Logout()
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Error logging out: %v", err)
		} else {
			log.Infof("s+ow-whatsapp-bridge: Successfully logged out")
		}
	case "list":
		groups, err := cli.GetJoinedGroups()
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Failed to get group list: %v", err)
		} else {
			for _, group := range groups {
				fmt.Printf("%s\t\t%s\n", group.JID, group.Name)
			}
		}
	case "send":
		if len(args) < 2 {
			log.Errorf("s+ow-whatsapp-bridge: Usage: send <jid> <text>")
			return
		}
		recipient, ok := parseJID(args[0])
		if !ok {
			return
		}
		msg := &waProto.Message{Conversation: proto.String(strings.Join(args[1:], " "))}
		resp, err := cli.SendMessage(context.Background(), recipient, msg)
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Error sending message: %v", err)
		} else {
			log.Infof("s+ow-whatsapp-bridge: Message sent (server timestamp: %s)", resp.Timestamp)
		}
	}
}

var historySyncID int32
var startupTime = time.Now().Unix()

func handler(rawEvt interface{}) {
	switch evt := rawEvt.(type) {
	case *events.AppStateSyncComplete:
		if len(cli.Store.PushName) > 0 && evt.Name == appstate.WAPatchCriticalBlock {
			err := cli.SendPresence(types.PresenceAvailable)
			if err != nil {
				log.Warnf("Failed to send available presence: %v", err)
			} else {
				log.Infof("s+ow-whatsapp-bridge: Marked self as available")
			}
		}
	case *events.Connected, *events.PushNameSetting:
		if len(cli.Store.PushName) == 0 {
			return
		}
		// Send presence available when connecting and when the pushname is changed.
		// This makes sure that outgoing messages always have the right pushname.
		err := cli.SendPresence(types.PresenceAvailable)
		if err != nil {
			log.Warnf("Failed to send available presence: %v", err)
		} else {
			log.Infof("s+ow-whatsapp-bridge: Marked self as available")
		}
	case *events.StreamReplaced:
		os.Exit(0)
	case *events.Message:
		metaParts := []string{fmt.Sprintf("pushname: %s", evt.Info.PushName), fmt.Sprintf("timestamp: %s", evt.Info.Timestamp)}
		if evt.Info.Type != "" {
			metaParts = append(metaParts, fmt.Sprintf("type: %s", evt.Info.Type))
		}
		if evt.Info.Category != "" {
			metaParts = append(metaParts, fmt.Sprintf("category: %s", evt.Info.Category))
		}
		if evt.IsViewOnce {
			metaParts = append(metaParts, "view once")
		}
		if evt.IsViewOnce {
			metaParts = append(metaParts, "ephemeral")
		}
		if evt.IsViewOnceV2 {
			metaParts = append(metaParts, "ephemeral (v2)")
		}
		if evt.IsDocumentWithCaption {
			metaParts = append(metaParts, "document with caption")
		}
		if evt.IsEdit {
			metaParts = append(metaParts, "edit")
		}

		log.Infof("s+ow-whatsapp-bridge: Received message %s from %s (%s): %+v", evt.Info.ID, evt.Info.SourceString(), strings.Join(metaParts, ", "), evt.Message)

		if evt.Message.GetPollUpdateMessage() != nil {
			decrypted, err := cli.DecryptPollVote(evt)
			if err != nil {
				log.Errorf("s+ow-whatsapp-bridge: Failed to decrypt vote: %v", err)
			} else {
				log.Infof("s+ow-whatsapp-bridge: Selected options in decrypted vote:")
				for _, option := range decrypted.SelectedOptions {
					log.Infof("s+ow-whatsapp-bridge: - %X", option)
				}
			}
		} else if evt.Message.GetEncReactionMessage() != nil {
			decrypted, err := cli.DecryptReaction(evt)
			if err != nil {
				log.Errorf("s+ow-whatsapp-bridge: Failed to decrypt encrypted reaction: %v", err)
			} else {
				log.Infof("s+ow-whatsapp-bridge: Decrypted reaction: %+v", decrypted)
			}
		}

		img := evt.Message.GetImageMessage()
		if img != nil {
			data, err := cli.Download(img)
			if err != nil {
				log.Errorf("s+ow-whatsapp-bridge: Failed to download image: %v", err)
				return
			}
			exts, _ := mime.ExtensionsByType(img.GetMimetype())
			savePath := fmt.Sprintf("%s%s", evt.Info.ID, exts[0])
			err = os.WriteFile(savePath, data, 0600)
			if err != nil {
				log.Errorf("s+ow-whatsapp-bridge: Failed to save image: %v", err)
				return
			}
			log.Infof("s+ow-whatsapp-bridge: Saved image in message to %s", savePath)
		}
	case *events.Receipt:
		if evt.Type == types.ReceiptTypeRead || evt.Type == types.ReceiptTypeReadSelf {
			log.Infof("s+ow-whatsapp-bridge: %v was read by %s at %s", evt.MessageIDs, evt.SourceString(), evt.Timestamp)
		} else if evt.Type == types.ReceiptTypeDelivered {
			log.Infof("s+ow-whatsapp-bridge: %s was delivered to %s at %s", evt.MessageIDs[0], evt.SourceString(), evt.Timestamp)
		}
	case *events.Presence:
		if evt.Unavailable {
			if evt.LastSeen.IsZero() {
				log.Infof("s+ow-whatsapp-bridge: %s is now offline", evt.From)
			} else {
				log.Infof("s+ow-whatsapp-bridge: %s is now offline (last seen: %s)", evt.From, evt.LastSeen)
			}
		} else {
			log.Infof("s+ow-whatsapp-bridge: %s is now online", evt.From)
		}
	case *events.HistorySync:
		id := atomic.AddInt32(&historySyncID, 1)
		fileName := fmt.Sprintf("history-%d-%d.json", startupTime, id)
		file, err := os.OpenFile(fileName, os.O_WRONLY|os.O_CREATE, 0600)
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Failed to open file to write history sync: %v", err)
			return
		}
		enc := json.NewEncoder(file)
		enc.SetIndent("", "  ")
		err = enc.Encode(evt.Data)
		if err != nil {
			log.Errorf("s+ow-whatsapp-bridge: Failed to write history sync: %v", err)
			return
		}
		log.Infof("s+ow-whatsapp-bridge: Wrote history sync to %s", fileName)
		_ = file.Close()
	case *events.AppState:
		log.Debugf("s+ow-whatsapp-bridge: App state event: %+v / %+v", evt.Index, evt.SyncActionValue)
	case *events.KeepAliveTimeout:
		log.Debugf("s+ow-whatsapp-bridge: Keepalive timeout event: %+v", evt)
	case *events.KeepAliveRestored:
		log.Debugf("s+ow-whatsapp-bridge: Keepalive restored")
	case *events.Blocklist:
		log.Infof("s+ow-whatsapp-bridge: Blocklist event: %+v", evt)
	}
}
