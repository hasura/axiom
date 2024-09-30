#!/bin/bash

# Define the GraphQL endpoints
ENDPOINTS=(
  "https://axiom-au.ddn.hasura.app/graphql"
  "https://axiom-eu.ddn.hasura.app/graphql"
  "https://axiom-us-west.ddn.hasura.app/graphql"
  "https://axiom-us-east.ddn.hasura.app/graphql"
  "https://axiom-sg.ddn.hasura.app/graphql"
  "https://axiom-test.ddn.hasura.app/graphql"
)

# Define the query
QUERY='{
  "query": "query getUsers { auth_users(limit: 1) { id } customer_customers(limit: 1) { customerId } customer_maskCardNumber(cardNumber: \"1234123412341234\") customerPreferences(limit: 1) { id } network_calls(limit: 1) { callid } network_cdr(limit: 1) { guid } support_convertDataUsageToMb(usageInGb: 1.5) support_documents(limit: 1) { uuid } support_userProfiles(limit: 1) { id } }"
}'
TESTQUERY='{
  "query": "query getUsers { customer_customers(limit: 1) { customerId } }"
}'

# Function to get current time in milliseconds
current_time_ms() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: use gdate from coreutils
    gdate +%s%3N
  else
    # Linux: use date
    date +%s%3N
  fi
}

for ENDPOINT in "${ENDPOINTS[@]}"; do
  {
    if [[ "$ENDPOINT" == "https://axiom-test.ddn.hasura.app/graphql" ]]; then
      QUERY="$TESTQUERY"
    fi

    START_TIME=$(current_time_ms)
    RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST -H "Content-Type: application/json" -d "$QUERY" "$ENDPOINT")
    END_TIME=$(current_time_ms)

    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1 | sed 's/HTTP_CODE://')
    RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')
    DURATION=$((END_TIME - START_TIME))

    echo "Endpoint: $ENDPOINT | HTTP Code: $HTTP_CODE | Time Taken: ${DURATION}ms | Response: $RESPONSE_BODY"
  } &
done

wait