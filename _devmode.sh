#!/bin/bash
# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv_flounder"
#echo "DEV_MODE: $DEV_MODE"
if [ "$DEV_MODE" = "True" ]; then
    DEV_MODE="False"
    deactivate
    echo "Dev mode disabled"
else
    DEV_MODE="True"
    . "$VENV_PATH/bin/activate"
    echo "Dev mode enabled"
fi

export DEV_MODE="$DEV_MODE"

