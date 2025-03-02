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
      path: "/v1/api/rest/cases",
      methods: ["GET"],
      query: `
        query UrgentCases($limit: Int = 10, $offset: Int = 0) {
          cases(where: {urgencyLevel: {_eq: "critical"}}, limit: $limit, offset: $offset) {
            caseId
            createdAt
            status
            urgencyLevel
            recommendedDate
            operatorId
          }
        }
        `,
    },
  ],
};
  