import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

function loadConfig() {
    const isRunningInDocker = process.env.RUNNING_IN_DOCKER === 'true';
    const HASURA_SECRET = process.env.HASURA_GRAPHQL_ADMIN_SECRET;
    const DELAY = process.env.EMULATOR_DELAY || 1000;

    if (!HASURA_SECRET) {
        throw new Error("HASURA_GRAPHQL_ADMIN_SECRET environment variable not set.");
    }

    return {
        hasuraEndpoint: isRunningInDocker
            ? 'http://hasura:8080/v1/graphql'
            : 'http://127.0.0.1:18080/v1/graphql',
        hasuraSecret: HASURA_SECRET,
        debug: process.env.DEBUG === 'true',
        delay: DELAY
    };
}

try {
    const config = loadConfig();
    if (config.debug) console.log("Config:", config);

    const generateAUPhoneNumber = () => {
        const prefixes = ['02', '03', '04', '05'];
        const suffix = Math.floor(Math.random() * 90000000 + 10000000);
        return `${prefixes[Math.floor(Math.random() * prefixes.length)]}${suffix}`;
    };

    const generateCustomerID = () => Math.floor(Math.random() * 100 + 1);
    const generateDeviceID = () => Math.floor(Math.random() * 100 + 1);
    const generateDuration = () => Math.floor(Math.random() * 3600);
    const generateCallType = () => ['Local', 'International'][Math.floor(Math.random() * 2)];
    const generateMessageType = () => ['SMS', 'MMS'][Math.floor(Math.random() * 2)];
    const generateNodeId = () => Math.floor(Math.random() * 1000 + 1);

    const getCurrentTimestamp = () => {
        return new Date().toISOString();
    };

    const performGraphQLMutation = async (query, variables) => {
        try {
            const response = await fetch(config.hasuraEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-hasura-admin-secret': config.hasuraSecret
                },
                body: JSON.stringify({
                    query,
                    variables
                })
            });

            const responseData = await response.json();
            if (config.debug) console.log("GraphQL Response:", responseData);
        } catch (err) {
            if (config.debug) console.error("Error performing GraphQL mutation: ", err);
        }
    };

    const insertCall = async () => {
        const mutation = `
        mutation InsertCall($customerId: Int!, $deviceId: Int!, $duration: Int!, $callType: String!, $receiverNumber: String!, $nodeId: Int!, $timestamp: timestamptz!) {
            insert_calls_one(object: {customerid: $customerId, deviceid: $deviceId, duration: $duration, calltype: $callType, receivernumber: $receiverNumber, nodeid: $nodeId, timestamp: $timestamp}) {
                callid
            }
        }
    `;
        await performGraphQLMutation(mutation, {
            customerId: generateCustomerID(),
            deviceId: generateDeviceID(),
            duration: generateDuration(),
            callType: generateCallType(),
            receiverNumber: generateAUPhoneNumber(),
            nodeId: generateNodeId(),
            timestamp: getCurrentTimestamp()
        });
    };

    const insertText = async () => {
        const mutation = `
        mutation InsertText($customerId: Int!, $deviceId: Int!, $messageType: String!, $receiverNumber: String!, $nodeId: Int!, $timestamp: timestamptz!) {
            insert_texts_one(object: {customerid: $customerId, deviceid: $deviceId, messagetype: $messageType, receivernumber: $receiverNumber, nodeid: $nodeId, timestamp: $timestamp}) {
                textid
            }
        }
    `;
        await performGraphQLMutation(mutation, {
            customerId: generateCustomerID(),
            deviceId: generateDeviceID(),
            messageType: generateMessageType(),
            receiverNumber: generateAUPhoneNumber(),
            nodeId: generateNodeId(),
            timestamp: getCurrentTimestamp(),
        });
    };

    const textRandomInterval = () => Math.floor(Math.random() * config.delay + 10);
    const callRandomInterval = () => Math.floor(Math.random() * 5 * config.delay + 100);

    const initiateCallInsertion = () => {
        insertCall();
        setTimeout(initiateCallInsertion, callRandomInterval());
    };

    const initiateTextInsertion = () => {
        insertText();
        setTimeout(initiateTextInsertion, textRandomInterval());
    };

    initiateCallInsertion();
    initiateTextInsertion();

} catch (error) {
    console.error(error.message);
    process.exit(1);
}
