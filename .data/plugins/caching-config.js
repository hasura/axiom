export const Config = {
  headers: { "hasura-m-auth": process.env.CACHING_PLUGIN_SECRET },
  time_to_live: 600,
  redis_url: process.env.CACHING_PLUGIN_REDIS_URL,
  otel_endpoint: process.env.OTLP_ENDPOINT,
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
