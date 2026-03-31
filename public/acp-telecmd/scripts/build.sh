#!/bin/bash

# This script orchestrates acpx to run the project's native build.sh
# It should be called from the OpenClaw environment.

# Ensure the correct working directory for acpx
CWD="/home/ubuntu/.openclaw/workspace/projects/synotelecommand-client"
MODEL="openai-codex/gpt-5.3-codex"
BUILD_SCRIPT="./testfiles/build.sh"

npx acpx \
  --approve-all \
  --allowed-tools shell.exec \
  --cwd "$CWD" \
  --model "$MODEL" \
  codex prompt "\nRun and show the result of the project build script:\n$BUILD_SCRIPT\n"
