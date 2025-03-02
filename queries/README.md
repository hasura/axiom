# Queries Directory

This directory contains example queries for the Hasura GraphQL API and REST endpoints.

## Structure

- `graphql/` - GraphQL query examples
- `rest/` - REST API request examples

## GraphQL Queries

The GraphQL queries are intended for use within the `telco` demo and showcase different examples of how DDN can retrieve, join, filter, sort, and limit information across multiple different backend data sources.

Use the inbuilt GraphiQL editor within Hasura DDN to test these queries.

## REST API Requests

RESTified endpoints are added in as a plugin in the globals subgraph. Configuration of RESTified endpoints is first in Hasura at `hasura/globals/plugin-config.hml` and secondly in the plugin itself.

The plugins define the REST endpoints and the graphql query they correspond to. These are both defined in the `.data/plugins/restified` directory:

- `telco.http` - Uses endpoints defined in `.data/plugins/restified/telco-config.ts`
- `aml.http` - Uses endpoints defined in `.data/plugins/restified/aml-config.ts`
- `healthcare.http` - Uses endpoints defined in `.data/plugins/restified/healthcare-config.ts`

Each config file maps REST endpoints to GraphQL operations. For example, in telco-config.ts:

```typescript
{
  path: "/v1/api/rest/users/:id",
  methods: ["DELETE"],
  query: `
    mutation DeleteUser($id: Auth_Int4!) {
      DeleteUsersById(
        keyId: $id
        preCheck: {}
      ) {
        affectedRows
      }
    }
  `,
}
```

This defines a DELETE endpoint at `/v1/api/rest/users/:id` that executes the DeleteUser mutation.

The HTTP files in the `rest/` directory provide examples of calling these endpoints:

```
DELETE http://localhost:3280/v1/api/rest/users/101
Content-Type: application/json
hasura-m-auth: your-auth-token