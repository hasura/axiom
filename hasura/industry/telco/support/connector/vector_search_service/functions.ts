import { OpenAI } from 'openai';

/**
 * Interface for text embedding response
 */
export interface TextEmbeddingResponse {
  text: string;
  embedding: number[];
}

/**
 * Interface for document embedding response
 */
export interface DocumentEmbeddingResponse {
  document_uuid: string;
  embeddings: number[];
}

/**
 * Interface for document metadata
 */
export interface DocumentMetadata {
  uuid: string;
  title: string;
  body: string;
  tags?: string;
  language?: string;
  updated_at?: string;
  created_at?: string;
  status?: string;
  view_count?: number;
  rating?: number;
}

/**
 * Generate embeddings for a collection of documents
 *
 * @param text String input for converting into embedding
 * @returns TextEmbeddingResponse
 * @readonly This function should only analyze data without making modifications
 */
export async function generateEmbedding(text: string): Promise<TextEmbeddingResponse> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });
  const response = await openai.embeddings.create({
    model: "text-embedding-ada-002",
    input: text,
  });
  
  return {
    text,
    embedding: response.data[0].embedding
  };
}

/**
 * Generate embeddings for a collection of documents
 *
 * @param documents Array of document metadata
 * @returns Array of document UUIDs and their corresponding embeddings
 * @readonly This function should only analyze data without making modifications
 */
export async function generateDocumentEmbeddings(
  documents: DocumentMetadata[]
): Promise<DocumentEmbeddingResponse[]> {
  const results: DocumentEmbeddingResponse[] = [];
  
  for (const doc of documents) {
    // Create a combined text representation focusing on the most important fields
    const combinedText = [
      doc.title,
      doc.title, // Weight title more by including it twice
      doc.body,
      doc.tags || ""
    ].join(" ");
    
    // Generate the embedding
    const embeddingResponse = await generateEmbedding(combinedText);
    
    results.push({
      document_uuid: doc.uuid,
      embeddings: embeddingResponse.embedding
    });
  }
  
  return results;
}