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
      path: "/v1/api/rest/stale-opps",
      methods: ["GET"],
      query: `
        query CustomersAndAccounts($close_date: varchar = "2025-03-20", ) {
          opportunities(
            where: {_and: {close_date: {_lte: $close_date}, stage: {_not: {_eq: "Closed Won"}}}}
          ) {
            close_date
            account_id
            amount
            created_date
            name
            id
            probability
            stage
          }
        }
      `,
    },
  ],
};
  