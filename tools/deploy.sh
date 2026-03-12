#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR/.."

if [ ! -f "$ROOT/.env" ]; then
  echo "Error: .env file not found. Copy .env.example and fill in your credentials." >&2
  exit 1
fi

source "$ROOT/.env"

if [ -z "$TIDBYT_API_TOKEN" ] || [ "$TIDBYT_API_TOKEN" = "your_api_token_here" ]; then
  echo "Error: TIDBYT_API_TOKEN not set in .env" >&2
  exit 1
fi

if [ -z "$TIDBYT_DEVICE_ID" ] || [ "$TIDBYT_DEVICE_ID" = "your_device_id_here" ]; then
  echo "Error: TIDBYT_DEVICE_ID not set in .env" >&2
  exit 1
fi

echo "Building..."
python3 "$ROOT/tools/build_app.py"

echo "Pushing to Tidbyt..."
pixlet push --api-token "$TIDBYT_API_TOKEN" "$TIDBYT_DEVICE_ID" "$ROOT/app/app.star"

echo "Done."
