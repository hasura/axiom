export const Config = {
  graphqlServer: {
    headers: {
      additional: {
        "Content-Type": "application/json",
      },
      forward: ["X-Hasura-Role", "Authorization", "X-Hasura-ddn-token"],
    },
  },
  headers: {
    "hasura-m-auth": process.env.RESTIFIED_PLUGIN_SECRET,
  },
  restifiedEndpoints: [
    {
      path: "/v1/api/rest/customers",
      methods: ["GET"],
      query: `
        query CustomersAndAccounts($limit: Int = 10, $offset: Int = 0) {
          customers (limit: $limit, offset: $offset) {
            name
            dob
            nationality
            account_details {
              name
              risk
            }
          }
        }
      `,
    },
  ],
};
  