#!/usr/bin/env bash

if ! command -v jq &> /dev/null; then
  echo "Error: jq is not installed."
  exit 1
fi

# Define the GraphQL endpoints
ENDPOINTS=(
  "https://axiom-au.ddn.hasura.app/graphql"
  "https://axiom-eu.ddn.hasura.app/graphql"
  "https://axiom-us-west.ddn.hasura.app/graphql"
  "https://axiom-us-east.ddn.hasura.app/graphql"
  "https://axiom-sg.ddn.hasura.app/graphql"
  "https://axiom-test.ddn.hasura.app/graphql"
  "https://axiom-dev.ddn.hasura.app/graphql"
)

QUERY='{
  "query": "query buildUserDashboard { formatDateToIso(dateString: \"2025-01-01\") usersById(id: 1) { email } customers(limit: 1, where: {segment: {_eq: \"family\"}}) { firstName lastName email segment customerLinks { customerPreferences { socialMedia { linkedin } } supportDB { supportHistory { date status } } } creditCards(where: {expiry: {_gte: \"2024-01-01\"}}) { maskCreditCard expiry cvv } billings(where: {billingDate: {_lte: \"2025-01-01\"}}) { formatBillingDate paymentStatus totalAmount } } calls(limit: 1) { callid } cdr(limit: 1) { guid } documents(limit: 1) { uuid } }", "operationName": "buildUserDashboard"
}'

TESTQUERY='{
  "query": "query simpleUserRetrieval { customers(limit: 1) { customerId } }", "operationName": "simpleUserRetrieval"
}'

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

for ENDPOINT in "${ENDPOINTS[@]}"; do
  query="$QUERY"
  if [[ "$ENDPOINT" =~ https://axiom-(test|dev).ddn.hasura.app/graphql ]]; then
    query="$TESTQUERY"
  fi
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
done