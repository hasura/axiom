import express from 'express';
import axios from 'axios';
import yaml from "js-yaml";
import fs from "fs";
import swaggerUi from "swagger-ui-express";
import { loadConfig } from './config.js';

const app = express();
const port = 4050;
const config = loadConfig();
const yamlFilePath = "./events.openapi.yaml";
const swaggerDocument = yaml.load(fs.readFileSync(yamlFilePath, "utf8"));
app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

async function makeGraphQLRequest(query, variables) {
    try {
        const response = await axios.post(config.hasuraEndpoint, {
            query: query,
            variables: variables
        }, {
            headers: {
                'Content-Type': 'application/json',
                'x-hasura-admin-secret': config.hasuraSecret
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error making GraphQL request:', error);
        throw error;
    }
}

const simulateRandomDelayAndError = async (req, res, handler) => {
    const delay = Math.floor(Math.random() * 100) + 1; // Random delay between 1-100ms
    const shouldThrowError = Math.random() < 0.001; // 1/1000 chance of error

    setTimeout(() => {
        if (shouldThrowError) {
            res.status(500).send("Simulated Random Error");
        } else {
            handler();
        }
    }, delay);
};

const DELETE_OLD_RECORDS = `
    mutation DeleteOldRecords($dateLimit: timestamptz) {
        delete_calls(where: {timestamp: {_lt: $dateLimit}}) {
            affected_rows
        }
        delete_texts(where: {timestamp: {_lt: $dateLimit}}) {
            affected_rows
        }
    }
`;

const GET_LATEST_RECORDS = `
    query GetLatestRecords {
        calls(order_by: {callid: desc}, limit: 1) {
            callid
        }
        texts(order_by: {textid: desc}, limit: 1) {
            textid
        }
    }
`;

const getOneHourAgo = () => {
    let date = new Date();
    date.setHours(date.getHours() - 1);
    return date.toISOString();
};

app.get('/cron', (req, res) => {
    simulateRandomDelayAndError(req, res, async () => {
        try {
            const response = await makeGraphQLRequest(DELETE_OLD_RECORDS, { dateLimit: getOneHourAgo() });
            res.json(response);
        } catch (error) {
            res.status(500).send(error.toString());
        }
    });
});

app.get('/insert', (req, res) => {
    simulateRandomDelayAndError(req, res, async () => {
        try {
            const response = await makeGraphQLRequest(GET_LATEST_RECORDS, {});
            res.json(response);
        } catch (error) {
            res.status(500).send(error.toString());
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
