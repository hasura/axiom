const axios = require('axios');

// Define the project IDs and endpoints
const endpoints = [
  { id: '45d179ba-c61f-458a-9440-442e9cc17b16', url: 'https://axiom-au.ddn.hasura.app/graphql' },
  { id: 'fde1ee6a-8645-4676-9300-39a6169e67a8', url: 'https://axiom-eu.ddn.hasura.app/graphql' },
  { id: '5b117fde-9ad4-4f35-aa52-d43e0b42c506', url: 'https://axiom-us-west.ddn.hasura.app/graphql' },
  { id: 'afcd5be8-38f1-48f7-a799-ede267cfd4d7', url: 'https://axiom-us-east.ddn.hasura.app/graphql' },
  { id: '4e254a45-0347-4cf6-82bf-1daf40e40e20', url: 'https://axiom-sg.ddn.hasura.app/graphql' },
  { id: '14494b6c-22ee-4037-ba1d-5ee62032c148', url: 'https://axiom-test.ddn.hasura.app/graphql' }
];

// Token storage for each project ID
let tokens = {};

const pat = process.env.PAT;
const controlPlane = 'https://auth.pro.hasura.io';

// Define the GraphQL queries
const mainQuery = {
  query: `
    query buildUserDashboard {
      usersById(id: 1) {
        email
        formatCreatedAtTimestamp
      }
      customers(limit: 1) {
        firstName
        lastName
        email
        segment
        customerLinks {
          customerPreferences {
            socialMedia { linkedin }
          }
          supportDB {
            supportHistory { date status }
          }
        }
        creditCards { maskCreditCard expiry cvv }
        billings { formatBillingDate paymentStatus totalAmount }
      }
      calls(limit: 1) { callid }
      cdr(limit: 1) { guid }
      documents(limit: 1) { uuid }
    }
  `,
  operationName: 'buildUserDashboard'
};

const testQuery = {
  query: `
    query simpleUserRetrieval {
      customers(limit: 1) { customerId }
    }
  `,
  operationName: 'simpleUserRetrieval'
};

// Function to check if a token is valid for a given endpoint
const isTokenValid = async (endpoint) => {
  const projectId = endpoint.id;
  console.log(`Checking token validity for ${projectId}`);

  if (!tokens[projectId]) {
    console.log(`Token invalid or missing for ${projectId}`);
    return false;
  }

  console.log(`Token valid for ${projectId}`);
  return true;
};

// Function to retrieve a token for a given endpoint and store it
const retrieveTokens = async (endpoint) => {
  const projectId = endpoint.id;
  console.log(`Retrieving token for ${projectId}`);

  try {
    const response = await axios.get(`${controlPlane}/ddn/project/token`, {
      headers: {
        'Authorization': `pat ${pat}`,
        'X-Hasura-Project-Id': projectId
      }
    });
    
    // Store the retrieved token by projectId
    tokens[projectId] = response.data.token;
    
    console.log(`Token retrieved and stored for ${projectId}`);
    return response.data.token;
  } catch (error) {
    console.error(`Error retrieving token for ${projectId}: ${error.message}`);
  }
};

// Function to query a GraphQL endpoint with the current token
const queryEndpoint = async (endpoint, query) => {
  const token = tokens[endpoint.id];
  try {
    const response = await axios.post(endpoint.url, query, {
      headers: {
        'Content-Type': 'application/json',
        'X-Hasura-DDN-Token': token
      }
    });
    
    console.log(`Response from ${endpoint.url}:`, response.data);
  } catch (error) {
    console.error(`Error querying ${endpoint.url}: ${error.message}`);
  }
};

// Main function to run queries periodically
const main = async () => {
  setInterval(async () => {
    await Promise.all(endpoints.map(async (endpoint) => {
      console.log(`Checking ${endpoint.id}`);

      // Ensure token is valid or retrieve a new one
      if (!await isTokenValid(endpoint)) {
        console.log(`Token invalid, retrieving for ${endpoint.id}`);
        await retrieveTokens(endpoint);
      }

      console.log(`Proceeding with ${endpoint.id}`);
      const query = endpoint.id === '14494b6c-22ee-4037-ba1d-5ee62032c148' ? testQuery : mainQuery;

      // Query the endpoint
      await queryEndpoint(endpoint, query);
    }));
  }, 60000); // Run every 60 seconds
};

main();
