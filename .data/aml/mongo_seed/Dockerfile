FROM mongo:8.0

ARG DATABASE_URI
ARG USERNAME
ARG PASSWORD

ENV DATABASE_URI=${DATABASE_URI}
ENV USERNAME=${USERNAME}
ENV PASSWORD=${PASSWORD}

# Copy the data and script
COPY accounts.json /accounts.json
COPY sanctions.json /sanctions.json
COPY aml_cases.json /aml_cases.json
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Use entrypoint script to ensure logs and debugging
ENTRYPOINT ["/entrypoint.sh"]
