import dotenv from 'dotenv';
dotenv.config();

export function loadConfig() {
    const isRunningInDocker = process.env.RUNNING_IN_DOCKER === 'true';
    const HASURA_SECRET = process.env.HASURA_GRAPHQL_ADMIN_SECRET;

    if (!HASURA_SECRET) {
        throw new Error("HASURA_GRAPHQL_ADMIN_SECRET environment variable not set.");
    }

    return {
        hasuraEndpoint: isRunningInDocker ? 'http://hasura:8080/v1/graphql' : 'http://127.0.0.1:18080/v1/graphql',
        hasuraSecret: HASURA_SECRET,
        debug: process.env.DEBUG === 'true'
    };
}
