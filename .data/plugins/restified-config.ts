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
      "hasura-m-auth": "zZkhKqFjqXR4g5MZCsJUZCcoPyZ",
    },
    restifiedEndpoints: [
      {
        path: "/v1/api/rest/users/:limit/:offset",
        methods: ["GET"],
        query: `
          query UsersEndpoint($limit: Int = 10, $offset: Int = 0) {
            users(limit: $limit, offset: $offset) {
              id
              email
              password
              roles
              createdAt
              updatedAt
            }
          }
          `,
      },
      {
        path: "/v1/api/rest/users",
        methods: ["POST"],
        query: `
          mutation CreateUser($email: Auth_Varchar = "", $id: Auth_Int4 = "", $password: Auth_Varchar = "", $roles: Auth_Varchar = "") {
            InsertUsers(
              objects: {email: $email, id: $id, password: $password, roles: $roles}
              postCheck: {}
            ) {
              affectedRows
            }
          }
          `,
      },
      {
        path: "/v1/api/rest/users/:id/password",
        methods: ["PUT"],
        query: `
          mutation UpdateUserPassword($id: Auth_Int4!, $password: Auth_Varchar!) {
            UpdateUsersById(
              keyId: $id
              postCheck: {}
              preCheck: {}
              updateColumns: {password: {set: $password}}
            ) {
              affectedRows
            }
          }
          `,
      },
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
      },
    ],
  };
  