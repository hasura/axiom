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
      path: "/v1/api/rest/manufacturing-capex",
      methods: ["GET"],
      query: `
        query CompletedExpenditure {
          capital_expenditures(where: {_and: {status: {_eq: "Completed"},department: {_eq: "Manufacturing"}}}) {
            accumulated_depreciation
            approval_date
            net_book_value
            project_manager
            purchase_date
          }
        }
      `,
    },
  ],
};
  