#!/bin/bash
cd "$(dirname "$0")"
cd bot
pip3 install -r requirements.txt
cd ..
cp config.yml bot/config.yml
cp engine.sh bot/engines/engine.sh
cd bot
chmod +x engines/engine.sh
python3 lichess-bot.py -v