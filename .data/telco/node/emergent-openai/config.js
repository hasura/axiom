import dotenv from 'dotenv';
dotenv.config();

export function loadConfig() {
    const isRunningInDocker = process.env.RUNNING_IN_DOCKER === 'true';
    const HASURA_SECRET = process.env.HASURA_GRAPHQL_ADMIN_SECRET;
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

    if (!HASURA_SECRET) {
        throw new Error("HASURA_GRAPHQL_ADMIN_SECRET environment variable not set.");
    }

    if (!OPENAI_API_KEY) {
        throw new Error("OPENAI_API_KEY environment variable not set.");
    }

    return {
        hasuraEndpoint: isRunningInDocker ? 'http://hasura:8080/v1/graphql' : 'http://127.0.0.1:18080/v1/graphql',
        hasuraSecret: HASURA_SECRET,
        openaiKey: OPENAI_API_KEY,
        debug: process.env.DEBUG === 'true'
    };
}