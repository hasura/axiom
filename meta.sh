#!/bin/bash

# Define the directory to search
SEARCH_DIR=${1:-.}

# Output CSV file
OUTPUT_FILE="collibra_import.csv"

# Initialize CSV header
echo "File Name,Kind,Name,Description" > "$OUTPUT_FILE"

# Find all .hml files and process them
find "$SEARCH_DIR" -type f -name "*.hml" | while read -r FILE; do
  # Extract YAML fragments containing 'kind: ObjectType'
  YAML_FRAGMENT=$(sed -n '/kind: ObjectType/,/^\s*$/p' "$FILE")
  
  # If a fragment was found, process it
  if [ -n "$YAML_FRAGMENT" ]; then
    # Convert YAML to JSON and extract relevant fields using yq or python (assuming yq is installed)
    JSON_FRAGMENT=$(echo "$YAML_FRAGMENT" | yq eval -j - 2>/dev/null)
    
    if [ $? -ne 0 ]; then
      # Use python if yq is not available
      JSON_FRAGMENT=$(echo "$YAML_FRAGMENT" | python3 -c 'import sys, yaml, json; print(json.dumps(yaml.safe_load(sys.stdin)))')
    fi
    
    # Extract fields from JSON using jq or python (assuming jq is installed)
    NAME=$(echo "$JSON_FRAGMENT" | jq -r '.definition.name // empty')
    KIND=$(echo "$JSON_FRAGMENT" | jq -r '.kind // empty')
    DESCRIPTION=$(echo "$JSON_FRAGMENT" | jq -r '.definition.description // empty')

    # If jq is not installed, fallback to using python for JSON parsing
    if [ $? -ne 0 ]; then
      NAME=$(echo "$JSON_FRAGMENT" | python3 -c 'import sys, json; print(json.loads(sys.stdin.read()).get("definition", {}).get("name", ""))')
      KIND=$(echo "$JSON_FRAGMENT" | python3 -c 'import sys, json; print(json.loads(sys.stdin.read()).get("kind", ""))')
      DESCRIPTION=$(echo "$JSON_FRAGMENT" | python3 -c 'import sys, json; print(json.loads(sys.stdin.read()).get("definition", {}).get("description", ""))')
    fi

    # Append to the CSV file
    echo "\"$FILE\",\"$KIND\",\"$NAME\",\"$DESCRIPTION\"" >> "$OUTPUT_FILE"
  fi
done

# Output final CSV file location
echo "CSV file created: $OUTPUT_FILE"
