export const Config = {
  headers: { "hasura-m-auth": process.env.CACHING_PLUGIN_SECRET },
  redis_url: process.env.CACHING_PLUGIN_REDIS_URL,
  otel_endpoint: process.env.OTLP_ENDPOINT,
  otel_headers: {},

  queries_to_cache: [
    {
      query: `{accounts {annual_revenue contacts {campaign_members {campaign {name type} net_new_lead_c} ddn_signup_date_c} opportunities {amount close_date} became_customer_date_c annual_revenue account_tier_c}}`,
      time_to_live: 300
    }
  ],
};
