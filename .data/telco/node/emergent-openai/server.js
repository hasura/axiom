import express from "express";
import yaml from "js-yaml";
import fs from "fs";
import swaggerUi from "swagger-ui-express";
import { loadConfig } from "./config.js";
import { generateEmbeddings } from "./openai.js";
import {
    getAllDocuments,
    getDocumentByUUID,
    searchDocuments,
    updateEmbeddingsInDB,
} from "./hasura.js";

const app = express();
app.use(express.json());

const config = loadConfig();
if (config.debug) console.log("Config:", config);

const yamlFilePath = "./openai.openapi.yaml";
const swaggerDocument = yaml.load(fs.readFileSync(yamlFilePath, "utf8"));
app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.post("/generate-embeddings", async (req, res) => {
    try {
        const { uuid } = req.body;
        if (!uuid) {
            return res.status(400).send({ error: "UUID is required" });
        }

        const document = await getDocumentByUUID(uuid);
        const documentString = `UUID: ${document.uuid}, Title: ${document.title}, Body: ${document.body}, Created At: ${document.created_at}, Updated At: ${document.updated_at}, Status: ${document.status}, Language: ${document.language}, View Count: ${document.view_count}, Rating: ${document.rating}, Tags: ${document.tags}`;

        const embeddings = await generateEmbeddings(documentString);
        await updateEmbeddingsInDB(uuid, embeddings);

        res.send({ message: "Embeddings updated" });
    } catch (error) {
        res.status(500).send({ error: error.message });
    }
});

app.post("/update-embeddings", async (req, res) => {
    try {
        const documents = await getAllDocuments();

        for (const document of documents) {
            const documentString =
                `UUID: ${document.uuid}, Title: ${document.title}, Body: ${document.body}`;
            const embeddings = await generateEmbeddings(documentString);
            await updateEmbeddingsInDB(document.uuid, embeddings);
        }

        res.send({ message: "Embeddings updated for all documents" });
    } catch (error) {
        res.status(500).send({ error: error.message });
    }
});

app.post("/search", async (req, res) => {
    try {
        const { search, limit } = req.body;
        if (!search) {
            return res.status(400).send({ error: "Search string is required" });
        }

        let effectiveLimit = 5;
        if (typeof limit === 'string' && !isNaN(limit) && limit !== 'null') {
            effectiveLimit = parseInt(limit, 10);
        } else if (typeof limit === 'number') {
            effectiveLimit = limit;
        }

        const embeddings = await generateEmbeddings(search);
        const searchResult = await searchDocuments(embeddings, effectiveLimit);

        res.send({ searchResult });
    } catch (error) {
        res.status(500).send({ error: error.message });
    }
});

const port = process.env.PORT || 4027;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
