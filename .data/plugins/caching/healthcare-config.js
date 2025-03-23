export const Config = {
  headers: { "hasura-m-auth": process.env.CACHING_PLUGIN_SECRET },
  redis_url: process.env.CACHING_PLUGIN_REDIS_URL,
  otel_endpoint: process.env.OTLP_ENDPOINT,
  otel_headers: {},

  queries_to_cache: [
    {
      query: `{drugReference {activeIngredientsInfo dosageFormName labelerName routeName substanceName proprietaryName productNdc nonproprietaryName}}`,
      time_to_live: 1800
    }
  ],
};
