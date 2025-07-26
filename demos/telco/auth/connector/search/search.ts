export interface SearchResult {
  title: string;
  link: string;
  description: string;
  published?: string;
}

export interface BraveSearchResponse {
  web: {
    results: Array<{
      title: string;
      url: string;
      description: string;
      published?: string;
    }>;
    total?: number;
  };
}

export interface GeminiResponse {
  candidates: {
    content: {
      parts: {
        text: string;
      }[];
      role: string;
    };
  }[];
}

export interface GeminiSearchResponse {
  response: string;
}

interface GeminiRequest {
  contents: {
    parts: {
      text: string;
    }[];
  }[];
  tools: {
    google_search: Record<string, unknown>;
  }[];
}

export interface PerplexityResponse {
  text: string;
  references: Array<string>;
};

export interface PerplexityAPIResponse {
  id: string;
  model: string;
  created: number;
  citations: Array<string>;
  choices: Array<{
    message: {
      content: string;
      role: string;
    };
    index: number;
    finish_reason: string;
  }>;
}

export async function searchBrave(
  query: string,
  apiKey: string,
  options: {
    count?: number;
    offset?: number;
    language?: string;
    country?: string;
    safeSearch?: "strict" | "moderate" | "off";
  } = {}
): Promise<SearchResult[]> {
  const BASE_URL = "https://api.search.brave.com/res/v1/web/search";

  const params = new URLSearchParams({
    q: query,
    ...(options.count && { count: options.count.toString() }),
    ...(options.offset && { offset: options.offset.toString() }),
    ...(options.language && { language: options.language }),
    ...(options.country && { country: options.country }),
    ...(options.safeSearch && { safe: options.safeSearch }),
  });

  try {
    const response = await fetch(`${BASE_URL}?${params.toString()}`, {
      headers: {
        Accept: "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json() as BraveSearchResponse;

    return data.web.results.map((result) => ({
      title: result.title,
      link: result.url,
      description: result.description,
      published: result.published,
    }));
  } catch (error) {
    console.error("Error fetching search results:", error);
    throw error;
  }
}

export async function queryGemini(
  query: string, 
  apiKey: string
): Promise<GeminiResponse> {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
  
  const requestBody: GeminiRequest = {
    contents: [
      {
        parts: [
          { text: query }
        ]
      }
    ],
    tools: [
      {
        google_search: {}
      }
    ]
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody)
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json() as GeminiResponse;
  console.log('Gemini response:', JSON.stringify(data));
  return data;
}
