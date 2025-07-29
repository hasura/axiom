import * as sdk from "@hasura/ndc-lambda-sdk";
import { GoogleGenerativeAI, DynamicRetrievalMode, HarmCategory, HarmBlockThreshold, GenerateContentResult as GeminiGenerateContentResult } from "@google/generative-ai";
import { searchBrave, SearchResult, queryGemini, GeminiSearchResponse, PerplexityResponse, PerplexityAPIResponse } from "./search";

// Environment setup
if (!process.env.GEMINI_API_KEY) {
  throw new Error('GEMINI_API_KEY is not defined in environment variables');
}

const BRAVE_API_KEY = process.env.BRAVE_API_KEY;
const PERPLEXITY_API_KEY = process.env.PERPLEXITY_API_KEY;
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

/******************************* SEARCH ************************************* */
/**
 * Make a web search with brave, returns 10 results
 * @param query Search query string
 * @returns Search results
 * @readonly
 * @hml
 */
export async function braveSearch(query: string): Promise<SearchResult[]> {
  const API_KEY = BRAVE_API_KEY!;
  try {
    const results = await searchBrave(query, API_KEY, {
      count: 10,
      language: "en",
      country: "US",
      safeSearch: "moderate",
    });
    results.forEach((result) => {
      console.log(`Title: ${result.title}`);
      console.log(`URL: ${result.link}`);
      console.log(`Description: ${result.description}`);
      console.log("---");
    });
    return results;
  } catch (error) {
    console.error("Search failed:", error);
    throw new sdk.UnprocessableContent(
      "Search failed: " + JSON.stringify(error)
    );
  }
}

/**
 * @readonly Exposes the function as an NDC function (the function should only query data without making modifications)
 * This function takes in a URL and extracts the raw HTML of the given URL, passes the HTML to AgentQL to extract structured data and return as a response.
 */
export async function searchWithPerplexity(query: string): Promise<PerplexityResponse> {
  const BASE_URL = 'https://api.perplexity.ai/chat/completions';
  
  if (!PERPLEXITY_API_KEY) {
    throw new Error('Perplexity API key not found in environment variables');
  }

  try {
    const requestBody = {
      model: "sonar-pro",
      messages: [
        {
          role: "system",
          content: "You are a helpful search assistant. Be precise."
        },
        {
          role: "user",
          content: query
        }
      ],
      max_tokens: 1024,
      temperature: 0.2,
      top_p: 0.9,
      search_domain_filter: null,
      return_images: false,
      return_related_questions: false,
      search_recency_filter: null,
      top_k: 0,
      stream: false,
      presence_penalty: 0,
      frequency_penalty: 1,
      response_format: null
    };

    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${PERPLEXITY_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('API Error Response:', errorText);
      throw new Error(`Perplexity API error (${response.status}): ${errorText}`);
    }

    const data = await response.json() as PerplexityAPIResponse;
    
    return {
      text: data.choices[0].message.content,
      references: data.citations
    };
  } catch (error) {
    console.error('Perplexity API Error:', error);
    throw new Error(
      `Failed to perform Perplexity search: ${error instanceof Error ? error.message : 'Unknown error'}`
    );
  }
}


/**
 * @readonly Exposes the function as an NDC function (the function should only query data without making modifications)
 * This function takes in a URL and extracts the raw HTML of the given URL, passes the HTML to AgentQL to extract structured data and return as a response.
 */
export async function geminiSearch(query: string): Promise<GeminiSearchResponse> {
  try {
    const apiKey = GEMINI_API_KEY;
    const response = await queryGemini(query, apiKey);
    if (!response) {
      throw new Error(`HTTP error! status: ${response}`);
    }
    
    // Extract the answer from the response
    const answer = response.candidates[0]?.content.parts[0]?.text;
    console.log('Answer:', answer);
    return { response: answer };
    
  } catch (error) {
    console.error('Error:', error);
    throw new sdk.UnprocessableContent(
      "Search failed: " + JSON.stringify(error)
    );
  }
}