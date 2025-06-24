interface DeviceActionResponse {
  activation_id?: string;
  deactivation_id?: string;
  device_id?: string;
  status: string;
}

async function processDeviceAction(
  action: "activate" | "deactivate",
  email: string,
  customer_id: string,
  device_id: string
): Promise<DeviceActionResponse> {
  const idKey = action === "activate" ? "activation_id" : "deactivation_id";

  return {
    [idKey]: `${action}_${Math.floor(Math.random() * 10000)}`,
    device_id,
    status: action === "activate" ? "activated" : "deactivated",
  };
}

interface CreateCampaignObj {
  campaignId?: string;
  budget?: string;
  campaignName?: string;
  channel: string;
  endDate: Date,
  offerDetails: string,
  targetSegment: string
}

export function CreateCampaign(camp: CreateCampaignObj): CreateCampaignObj {
  camp.campaignId = `${Math.floor(Math.random() * 10000)}`;
  return camp;
}

export async function activateDevice(
  email: string,
  customer_id: string,
  device_id: string
): Promise<DeviceActionResponse> {
  return processDeviceAction("activate", email, customer_id, device_id);
}

export async function deactivateDevice(
  email: string,
  customer_id: string,
  device_id: string
): Promise<DeviceActionResponse> {
  return processDeviceAction("deactivate", email, customer_id, device_id);
}

/**
 * Masks a credit card number to hide all but the last four digits.
 *
 * @param cardNumber The credit card number to mask.
 * @returns The masked credit card number.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function maskCardNumber(cardNumber?: string): string {
  if (!cardNumber) {
    return "Invalid card number";
  }
  try {
    // Ensure only digits are processed, remove any spaces or dashes
    const sanitized = cardNumber.replace(/[\s\-]/g, '');
    // Check if the sanitized input is a valid credit card number (only digits and correct length)
    if (!/^\d{13,19}$/.test(sanitized)) {
      return "Invalid card number";
    }
    // Mask all digits except the last four
    return sanitized.slice(0, -4).replace(/\d/g, '*') + sanitized.slice(-4);
  } catch (error) {
    console.error("Error masking card number:", error);
    return "Invalid card number";
  }
}

// TypeScript interfaces for the Churn Prediction API

export interface CustomerData {
  customerId: number;
  satisfactionScore: number; // 1-10
  segment: string; // Business, Family, Premium, Standard, Student
  dataAllocationGb: number;
  dataUsedGb: number;
  totalAmount: number;
  paymentStatus: string; // Paid, Pending, Overdue, Late
  downloadSpeed: number;
  uploadSpeed: number;
  latency: number;
  serviceInteractionCount: number;
  avgResolutionTime?: number; // Optional, defaults to 0.0
  feedbackRating?: number; // Optional, defaults to 3.0
  callDurationMinutes?: number; // Optional, defaults to 0.0
}

export interface ChurnPrediction {
  customerId: number;
  churnProbability: number; // 0.0 to 1.0
  churnRisk: string; // Low, Medium, High
  riskFactors: string[];
  recommendations: string[];
}

export interface PredictChurnRequest {
  customer_data: CustomerData;
}

export interface ApiError {
  detail: string | Array<{
    type: string;
    loc: (string | number)[];
    msg: string;
    input: any;
    url?: string;
  }>;
}

/**
 * Function to call the churn prediction endpoint
 *
 * @readonly This function should only query data without making modifications
 */
export async function predictChurn(
  customer_data: CustomerData,
): Promise<ChurnPrediction> {
  const baseUrl = `http://host.docker.internal:8000`;
  try {
    const response = await fetch(`${baseUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(customer_data), // Extract customer_data from request
    });

    if (!response.ok) {
      const errorData = await response.json() as ApiError;
      throw new Error(`API Error (${response.status}): ${JSON.stringify(errorData.detail)}`);
    }

    const prediction = await response.json() as ChurnPrediction;
    return prediction;
  } catch (error) {
    if (error instanceof Error) {
      throw error;
    }
    throw new Error(`Network error: ${String(error)}`);
  }
}


