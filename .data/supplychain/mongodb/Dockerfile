FROM mongo:latest

# Set environment variables with default values
ENV DATABASE_URI="mongodb://localhost:27017/ecommerce"
ENV USERNAME=""
ENV PASSWORD=""

# Copy JSON data files
COPY customer_orders.json /customer_orders.json

# Copy and set permissions for the entrypoint script
COPY entrypoint.sh /docker-entrypoint-initdb.d/entrypoint.sh
RUN chmod +x /docker-entrypoint-initdb.d/entrypoint.sh

# Default command (will be passed to the MongoDB entrypoint)
CMD ["mongod", "--wiredTigerCacheSizeGB", "0.25"]