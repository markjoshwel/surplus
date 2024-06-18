#!/bin/sh
# surplus on wheels: termux installation script
set -e

# get packages
yes | pkg upgrade
yes | pkg install python cronie termux-api termux-services wget

# install pipx and surplus
pip install pipx
pipx install surplus

# install s+ow
mkdir -p ~/.local/bin/
if ping -c 1 surplus.joshwel.co ; then
	wget -O ~/.local/bin/s+ow https://surplus.joshwel.co/spow.sh
else
	wget -O ~/.local/bin/s+ow https://raw.githubusercontent.com/markjoshwel/surplus/main/src/surplus-on-wheels/s+ow
fi
chmod +x ~/.local/bin/s+ow

# setup path
echo "export PATH=\$PATH:\$HOME/.local/bin/" >> ~/.profile

printf "
----- done! -----

if you're going to set a cron job up:

	1. restart termux
	2. run crontab -e
	3. add \"59 * * * *      bash -l -c \"(SPOW_TARGETS="" SPOW_CRON=y s+ow)\"\"
	   (remember to minimally fill in the SPOW_TARGETS variable)

else, surplus on wheels has been set up!

"
