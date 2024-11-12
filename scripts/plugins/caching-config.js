export const Config = {
  headers: { "hasura-m-auth": "zZkhKqFjqXR4g5MZCsJUZCnhCcoPyZ" },
  time_to_live: 600,
  redis_url: "redis://redis:6379",
  otel_endpoint: "http://jaeger:4318/v1/traces",
  otel_headers: {},

  queries_to_cache: [
    `
      query MyQuery {
        customers(where: {state: {_in: ["WA", "ACT"]}}) {
          firstName
          lastName
          postcode
          state
          country
          city
          address
        }
      }
    `
  ],
};
