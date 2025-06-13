FROM mongo:latest

# Copy the JSON data files
COPY accounts.json /accounts.json
COPY aml_cases.json /aml_cases.json
COPY sanctions.json /sanctions.json

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
