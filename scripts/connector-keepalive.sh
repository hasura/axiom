#!/usr/bin/env bash

set -e

if [[ -z "${cron_url}" ]] || [[ -z "${cron_query}" ]] || [[ -z "${SLACK_WEBHOOK}" ]]; then
  echo "cron_url, cron_query, and SLACK_WEBHOOK environment variables must all be defined"
  exit 1;
fi

if ! command -v jq &> /dev/null; then
  echo "Error: jq is not installed."
  exit 1
fi

ERROR_FILE="/tmp/axiom_error_counts.json"

if [[ ! -f "$ERROR_FILE" ]]; then
  echo '{}' > "$ERROR_FILE"
fi

ERROR_COUNTS=$(cat "$ERROR_FILE")
ERROR_LIMIT=5

# Function to get current time in milliseconds
current_time_ms() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    gdate +%s%3N
  else
    date +%s%3N
  fi
}

notify_slack() {
  local message=$1
  payload=$(jq -n --arg text "$message" '{text: $text}')
  curl -s -X POST -H "Content-Type: application/json" -d "$payload" "$SLACK_WEBHOOK"
}

# Read from environment variables
ENDPOINT="$cron_url"
query="$cron_query"

START_TIME=$(current_time_ms)
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST -H "Content-Type: application/json" -d "$query" "$ENDPOINT")
END_TIME=$(current_time_ms)

HTTP_CODE=$(echo "$RESPONSE" | tail -n 1 | sed 's/HTTP_CODE://')
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')
DURATION=$((END_TIME - START_TIME))

MESSAGE="Endpoint: $ENDPOINT | HTTP Code: $HTTP_CODE | Time Taken: ${DURATION}ms | Response: $RESPONSE_BODY"
echo "$MESSAGE"

ERROR_COUNT=$(echo "$ERROR_COUNTS" | jq -r --arg ENDPOINT "$ENDPOINT" '.[$ENDPOINT] // 0')

if echo "$RESPONSE_BODY" | grep -qi "error"; then
  ERROR_COUNT=$((ERROR_COUNT + 1))

  # Update error file
  ERROR_COUNTS=$(echo "$ERROR_COUNTS" | jq --arg ENDPOINT "$ENDPOINT" --argjson COUNT "$ERROR_COUNT" '. + {($ENDPOINT): $COUNT}')
  echo "$ERROR_COUNTS" > "$ERROR_FILE"

  if [[ "$ERROR_COUNT" -ge "$ERROR_LIMIT" ]]; then
    notify_slack "⚠️ Consecutive errors detected ($ERROR_COUNT) for $ENDPOINT! Last response: $MESSAGE"
  fi
else
  if [[ "$ERROR_COUNT" -ge "$ERROR_LIMIT" ]]; then
    notify_slack "✅ $ENDPOINT has recovered after $ERROR_COUNT failures."
  fi

  # Reset error count
  ERROR_COUNTS=$(echo "$ERROR_COUNTS" | jq --arg ENDPOINT "$ENDPOINT" '. + {($ENDPOINT): 0}')
  echo "$ERROR_COUNTS" > "$ERROR_FILE"
fi
