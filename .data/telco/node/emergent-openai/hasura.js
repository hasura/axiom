import axios from 'axios';
import { loadConfig } from './config.js';

async function executeGraphQLQuery(query, variables) {
    const config = loadConfig();
    try {
        const response = await axios.post(
            config.hasuraEndpoint, 
            { query, variables }, 
            { headers: { 'x-hasura-admin-secret': config.hasuraSecret } }
        );
        if (config.debug) console.log(response.data);
        return response.data;
    } catch (error) {
        console.error('Error executing GraphQL query:', error);
        throw error;
    }
}

export async function updateEmbeddingsInDB(documentUuid, embeddings) {
    const mutation = `
        mutation UpdateEmbeddings($documentUuid: uuid!, $embeddings: vector!) {
            insert_document_embeddings_one(
                object: {document_uuid: $documentUuid, embeddings: $embeddings},
                on_conflict: {
                    constraint: document_embeddings_pkey,
                    update_columns: [embeddings]
                }
            ) {
                document_uuid
            }
        }
    `;
    return executeGraphQLQuery(mutation, { documentUuid, embeddings });
}

export async function getDocumentByUUID(documentUuid) {
    const query = `
        query GetDocumentByUUID($uuid: uuid!) {
            documents_by_pk(uuid: $uuid) {
                uuid
                title
                body
                created_at
                updated_at
                status
                language
                view_count
                rating
                tags
            }
        }
    `;
    const data = await executeGraphQLQuery(query, { uuid: documentUuid });
    
    return data.data.documents_by_pk;
}

export async function getAllDocuments() {
    const query = `
        query GetAllDocuments {
            documents {
                uuid
                title
                body
                created_at
                updated_at
                status
                language
                view_count
                rating
                tags
            }
        }
    `;
    const data = await executeGraphQLQuery(query, {});
    return data.data.documents;
}

export async function searchDocuments(embedding, limit = 5) {
    const query = `
        query SearchDocuments($embedding: String!, $limit: Int!) {
            searchByEmbedding(args: {embedding: $embedding, limit: $limit}) {
                document_uuid
            }
        }
    `;
    const data = await executeGraphQLQuery(query, { embedding, limit });
    return data.data.searchByEmbedding;
}

