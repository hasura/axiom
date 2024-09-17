import axios from 'axios';
import { loadConfig } from './config.js';

export async function generateEmbeddings(text) {
    const config = loadConfig();
    try {
        const response = await axios.post('https://api.openai.com/v1/embeddings',
        {
            input: text,
            model: "text-embedding-ada-002",
            encoding_format: "float"
        },
        {
            headers: {
                'Authorization': `Bearer ${config.openaiKey}`,
                'Content-Type': 'application/json'
            }
        });

        return JSON.stringify(response.data.data.map(item => item.embedding).flat());

    } catch (error) {
        console.error('Error generating embeddings:', error);
        throw error;
    }
}
