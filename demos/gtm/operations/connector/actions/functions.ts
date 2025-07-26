interface ActionResponse {
  success: boolean;
  message: string;
}

/**
 * Adds a contact to a sequence (mock)
 */
export async function addContactToSequence(
  contactId: string,
  sequenceId: number
): Promise<ActionResponse> {
  // Pretend we added the contact
  return {
    success: true,
    message: `Contact ${contactId} added to sequence ${sequenceId}`,
  };
}

/**
 * Updates the stage of an opportunity (mock)
 */
export async function updateOpportunityStage(
  opportunityId: string,
  stage: string
): Promise<ActionResponse> {
  // Pretend we updated the stage
  return {
    success: true,
    message: `Opportunity ${opportunityId} stage updated to ${stage}`,
  };
}

/**
 * Updates the forecast for an opportunity (mock)
 */
export async function updateForecast(
  opportunityId: string,
  forecastAmount: number,
  probability: number
): Promise<ActionResponse> {
  // Pretend we updated the forecast
  return {
    success: true,
    message: `Forecast updated for opportunity ${opportunityId} with amount ${forecastAmount} and probability ${probability}%`,
  };
}

/**
 * Creates a new sequence (mock)
 */
export async function createSequence(
  name: string,
  description?: string,
  created_by?: string
): Promise<ActionResponse> {
  // Generate a fake sequence ID for the mock
  const sequenceId = Math.floor(Math.random() * 100000);
  return {
    success: true,
    message: `Sequence "${name}" created successfully with ID ${sequenceId}`,
  };
}

/**
 * Updates Salesforce MEDDPICC fields based on call transcript analysis
 */
export async function updateMeddpicc(
  opportunityId: string,
  metrics?: string,
  economicBuyer?: string,
  decisionCriteria?: string,
  decisionProcess?: string,
  paperProcess?: string,
  identifiedPain?: string,
  champion?: string,
  competition?: string
): Promise<ActionResponse> {
  const updatedFields = [];
  
  if (metrics) updatedFields.push('Metrics');
  if (economicBuyer) updatedFields.push('Economic Buyer');
  if (decisionCriteria) updatedFields.push('Decision Criteria');
  if (decisionProcess) updatedFields.push('Decision Process');
  if (paperProcess) updatedFields.push('Paper Process');
  if (identifiedPain) updatedFields.push('Identified Pain');
  if (champion) updatedFields.push('Champion');
  if (competition) updatedFields.push('Competition');
  
  return {
    success: true,
    message: updatedFields.length > 0
      ? `MEDDPICC fields updated for opportunity ${opportunityId} based on call transcript analysis. Updated fields: ${updatedFields.join(', ')}.`
      : `No MEDDPICC fields were updated for opportunity ${opportunityId}.`,
  };
}
