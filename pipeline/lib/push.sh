#!/bin/bash
# push.sh cNN... : envoie film.mp4 et vertical.mp4 dans le dépôt (transit) et affiche les liens
cd /home/claude/entrelien && mkdir -p v
for c in "$@"; do T=$(date +%H%M%S); cp /home/claude/prod/$c/film.mp4 v/$c-long-$T.mp4; cp /home/claude/prod/$c/vertical.mp4 v/$c-vert-$T.mp4; done
git add v && git -c user.name="Presentio Automation" -c user.email="noreply@anthropic.com" commit -q -m "Transit $*

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Rn5yPgthiVU7hEAndLMqWf" && git -c push.negotiate=true push -q 2>&1 | grep -v negotiation
for f in v/*.mp4; do L=$(stat -c %s $f); R=$(curl -sSI https://raw.githubusercontent.com/presentioautomation-bit/entrelien/main/$f | grep -i content-length | tr -dc 0-9); [ "$L" = "$R" ] && S=OK || S="ECART local=$L distant=$R"; echo "https://raw.githubusercontent.com/presentioautomation-bit/entrelien/main/$f $S"; done
