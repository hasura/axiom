export const Config = {
  headers: { "hasura-m-auth": process.env.CACHING_PLUGIN_SECRET },
  time_to_live: 600,
  redis_url: process.env.CACHING_PLUGIN_REDIS_URL,
  otel_endpoint: process.env.OTLP_ENDPOINT,
  otel_headers: {},

  queries_to_cache: [
    `{customers(where: {state: {_in: ["WA", "ACT"]}}) {firstName lastName postcode state country city address}}`
    `{ usersById(id: 1) { email formatCreatedAtTimestamp } customers(limit: 1) { firstName lastName email segment customerLinks { customerPreferences { socialMedia { linkedin } } supportDB { supportHistory { date status } } } creditCards { maskCreditCard expiry cvv } billings { formatBillingDate paymentStatus totalAmount } } calls(limit: 1) { callid } cdr(limit: 1) { guid } documents(limit: 1) { uuid } }`,
    `{ customers(limit: 1) { customerId } }`
  ],
};
