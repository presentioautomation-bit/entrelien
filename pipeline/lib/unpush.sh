#!/bin/bash
cd /home/claude/entrelien && git rm -q -r v && git -c user.name="Presentio Automation" -c user.email="noreply@anthropic.com" commit -q -m "Fin de transit

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Rn5yPgthiVU7hEAndLMqWf" && git -c push.negotiate=true push -q 2>&1 | grep -v negotiation; echo retiré
