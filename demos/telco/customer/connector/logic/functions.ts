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