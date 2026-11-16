#!/bin/bash
# dl.sh <dossier> <workspace> <clé session/génération signature>...
D=$1; WS=$2; shift 2; mkdir -p $D/tts
while [ $# -ge 3 ]; do curl -sS -o $D/tts/$1.mp3 "https://elevenlabsusercontent.com/database/workspace/$WS/content_generation/$2/content.mp3?Expires=${EXP:-1794866400}&KeyName=assets-cdn-key-1&Signature=$3" -w "$1 %{http_code}\n"; shift 3; done
