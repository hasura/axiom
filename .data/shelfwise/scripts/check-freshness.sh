#!/bin/bash
# Check if ShelfWise data is current
# Alert if data is more than 2 days old
# 
# Usage:
#   ./check-freshness.sh           # Check and exit with status
#   ./check-freshness.sh --alert   # Send alert if stale (configure alert method)

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHELFWISE_HOME="$(dirname "$SCRIPT_DIR")"

# Load database credentials
if [ -f "$SHELFWISE_HOME/.env" ]; then
    source "$SHELFWISE_HOME/.env"
fi

export PGHOST="${POSTGRES_HOST:-localhost}"
export PGPORT="${POSTGRES_PORT:-5432}"
export PGDATABASE="${POSTGRES_DB:-shelfwise}"
export PGUSER="${POSTGRES_USER:-postgres}"
export PGPASSWORD="${POSTGRES_PASSWORD}"

# Get last date in database
LAST_DATE=$(psql -t -c "SELECT MAX(date) FROM sales_daily;" 2>/dev/null | xargs)

if [ -z "$LAST_DATE" ]; then
    echo "ERROR: Cannot query database or no data found"
    exit 2
fi

# Calculate how many days old
LAST_DATE_EPOCH=$(date -d "$LAST_DATE" +%s)
TODAY_EPOCH=$(date +%s)
DAYS_OLD=$(( (TODAY_EPOCH - LAST_DATE_EPOCH) / 86400 ))

# Determine status
if [ $DAYS_OLD -le 1 ]; then
    STATUS="OK"
    EXIT_CODE=0
elif [ $DAYS_OLD -le 2 ]; then
    STATUS="WARNING"
    EXIT_CODE=1
else
    STATUS="CRITICAL"
    EXIT_CODE=2
fi

# Output
echo "[$STATUS] ShelfWise data freshness"
echo "  Last date: $LAST_DATE"
echo "  Days old: $DAYS_OLD"
echo "  Status: $STATUS"

# Send alert if requested and status is not OK
if [ "$1" = "--alert" ] && [ $EXIT_CODE -gt 0 ]; then
    MESSAGE="ShelfWise data is $DAYS_OLD days old (last: $LAST_DATE)"
    
    # TODO: Configure your alert method here
    # Examples:
    # - Email: echo "$MESSAGE" | mail -s "ShelfWise Alert" admin@example.com
    # - Slack: curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$MESSAGE\"}" YOUR_SLACK_WEBHOOK
    # - PagerDuty: curl -X POST https://events.pagerduty.com/v2/enqueue ...
    
    echo "ALERT: $MESSAGE"
fi

exit $EXIT_CODE