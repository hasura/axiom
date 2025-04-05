FROM mongo:8.0

ARG DATABASE_URI
ARG USERNAME
ARG PASSWORD

ENV DATABASE_URI=${DATABASE_URI}
ENV USERNAME=${USERNAME}
ENV PASSWORD=${PASSWORD}

# Copy the data and script
COPY customer_preferences.json /customer_preferences.json
COPY user_profiles.json /user_profiles.json
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Use entrypoint script to ensure logs and debugging
ENTRYPOINT ["/entrypoint.sh"]
