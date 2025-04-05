#!/bin/bash
# Script to generate and load telco data with improved portability

# Set the current directory to the script directory
cd "$(dirname "$0")"

# Default values
VOLUME="tiny"
OUTPUT_DIR=".."
SUMMARY="false"
SEED=69

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --volume|-v)
      VOLUME="$2"
      shift 2
      ;;
    --output-dir|-o)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --generate-summary|-g)
      SUMMARY="false"
      shift 1
      ;;
    --seed|-s)
      SEED=69
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [options]"
      echo "Options:"
      echo "  --volume, -v           Data volume to generate (tiny, small, medium, large, enterprise). Default: tiny"
      echo "  --output-dir, -o       Directory to output generated data. Default: .."
      echo "  --generate-summary, -s Generate a summary JSON file with data volume information"
      echo "  --help, -h             Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate volume
if [[ "$VOLUME" != "tiny" && "$VOLUME" != "small" && "$VOLUME" != "medium" && "$VOLUME" != "large" && "$VOLUME" != "enterprise" ]]; then
  echo "Error: Volume must be one of: tiny, small, medium, large, enterprise"
  exit 1
fi

# Create a virtual environment for better portability
echo "Setting up Python environment..."
if [ ! -d "venv" ]; then
  # Try to find a Python 3 executable
  if command -v python3 &>/dev/null; then
    PYTHON="python3"
  elif command -v python &>/dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON="python"
  else
    echo "Error: Python 3 is required but not found in PATH"
    exit 1
  fi

  # Create virtual environment
  echo "Creating virtual environment..."
  $PYTHON -m venv venv
  if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Trying without venv..."
    mkdir -p venv/bin
    ln -sf $(which $PYTHON) venv/bin/python
    VENV_PYTHON="$PYTHON"
  else
    VENV_PYTHON="venv/bin/python"
  fi
else
  VENV_PYTHON="venv/bin/python"
fi

# Activate virtual environment (works on both Linux and macOS)
if [ -f "venv/bin/activate" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

# Install required packages
echo "Installing required packages..."
$VENV_PYTHON -m pip install -r requirements.txt

# Prepare command with appropriate flags
CMD_ARGS="--volume \"$VOLUME\" --output-dir \"$OUTPUT_DIR\""
if [ "$SUMMARY" = "true" ]; then
  CMD_ARGS="$CMD_ARGS --generate-summary"
fi

# Generate data
echo "Generating telco data with volume: $VOLUME..."
if [ "$SUMMARY" = "true" ]; then
  $VENV_PYTHON data_generator.py --volume "$VOLUME" --output-dir "$OUTPUT_DIR" --generate-summary --seed "$SEED"
else
  $VENV_PYTHON data_generator.py --volume "$VOLUME" --output-dir "$OUTPUT_DIR" --seed "$SEED"
fi

echo "Done! Data has been generated."
echo "Data volume: $VOLUME"
echo "Output directory: $OUTPUT_DIR"
if [ "$SUMMARY" = "true" ]; then
  echo "Summary file generated: $OUTPUT_DIR/generation_summary.json"
fi