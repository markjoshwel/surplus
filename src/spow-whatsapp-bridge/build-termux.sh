mkdir -p "$HOME/.local/bin"
pkg install golang
go build
mv spow_whatsapp_bridge "$HOME/.local/bin/s+ow-whatsapp-bridge"
