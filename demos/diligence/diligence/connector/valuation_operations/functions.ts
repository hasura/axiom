export interface FinancialInconsistencyResponse {
  flag_id?: string;
  account_id: number;
  transaction_date: string;
  status: string;
  severity: string;
  assigned_to?: string;
}

export interface AdjustmentScenarioResponse {
  scenario_id?: string;
  account_id: number;
  adjustment_amount: number;
  adjustment_type: string;
  status: string;
  impact_on_valuation?: number;
}

export interface FindingResponse {
  finding_id?: string;
  workstream: string;
  severity: string;
  status: string;
  assigned_to?: string;
}

/**
 * **Description:**
 * This function flags financial inconsistencies in the company's data for further investigation. It creates a record of the potential issue, assigns it a severity level, and tracks its investigation status. This function is essential for identifying accounting irregularities, data discrepancies, or suspicious financial patterns during due diligence.
 *
 * **When to Call:**
 * - When discovering a mismatch between financial statements and general ledger entries
 * - Upon identifying unusual accounting treatments or questionable revenue recognition
 * - When transaction patterns deviate significantly from historical norms
 * - If financial ratios suggest potential manipulation or reporting issues
 *
 * @param details
 */
export async function flagFinancialInconsistency(
  accountId: number,
  accountName: string,
  transactionDate: string,
  amount: number,
  description: string,
  severity: string,
  assignedAnalyst?: string
): Promise<FinancialInconsistencyResponse> {
  if (amount <= 0) {
    throw new Error("Amount must be positive");
  }
  
  // Validate date format
  if (!/^\d{4}-\d{2}-\d{2}$/.test(transactionDate)) {
    throw new Error("Transaction date must be in YYYY-MM-DD format");
  }

  return {
    flag_id: `flag_${Math.floor(Math.random() * 10000)}`,
    account_id: accountId,
    transaction_date: transactionDate,
    status: "open",
    severity: severity,
    assigned_to: assignedAnalyst
  };
}

/**
 * **Description:**
 * This function creates financial adjustment scenarios to normalize the company's financial data. It documents adjustments needed for accurate valuation, such as one-time expenses, non-recurring revenue, or working capital normalization. The function calculates the impact on valuation multiples and allows for comparison across different adjustment scenarios.
 *
 * **When to Call:**
 * - When normalizing EBITDA by removing non-recurring items
 * - To adjust for owner-related expenses that won't continue post-acquisition
 * - When standardizing accounting treatments for comparability
 * - To model "what-if" scenarios for different valuation approaches
 *
 * @param details
 */
export async function createAdjustmentScenario(
  accountId: number,
  accountName: string,
  adjustmentAmount: number,
  adjustmentType: string,
  description: string,
  justification: string,
  fiscalYear: number,
  fiscalPeriod?: number,
  enterpriseValue?: number,
  ebitdaMultiple?: number
): Promise<AdjustmentScenarioResponse> {
  // Validate inputs
  if (fiscalYear < 2020 || fiscalYear > 2030) {
    throw new Error("Fiscal year must be between 2020 and 2030");
  }
  
  if (fiscalPeriod && (fiscalPeriod < 1 || fiscalPeriod > 12)) {
    throw new Error("Fiscal period must be between 1 and 12");
  }
  
  // Calculate impact on valuation if enterprise value and EBITDA multiple are provided
  let valuationImpact = undefined;
  if (enterpriseValue && ebitdaMultiple) {
    valuationImpact = adjustmentAmount * ebitdaMultiple;
  }

  return {
    scenario_id: `adj_${Math.floor(Math.random() * 10000)}`,
    account_id: accountId,
    adjustment_amount: adjustmentAmount,
    adjustment_type: adjustmentType,
    status: "draft",
    impact_on_valuation: valuationImpact
  };
}

/**
 * **Description:**
 * This function creates and manages findings during the due diligence process. It documents key issues discovered, categorizes them by severity and workstream, and tracks their resolution status. The findings register serves as a comprehensive record of all identified issues that may impact transaction terms, purchase price, or post-acquisition integration.
 *
 * **When to Call:**
 * - When identifying material risks that could affect deal valuation
 * - Upon discovering compliance or regulatory issues
 * - When uncovering operational inefficiencies or process weaknesses
 * - To document quality of earnings observations that support valuation adjustments
 *
 * @param details
 */
export async function createFinding(
  workstream: string,
  title: string,
  description: string,
  severity: string,
  impact: string,
  recommendation: string,
  supportingEvidence: string[],
  assignedAnalyst?: string
): Promise<FindingResponse> {
  // Validate inputs
  if (!title || title.length < 5) {
    throw new Error("Title must be at least 5 characters");
  }
  
  if (!description || description.length < 10) {
    throw new Error("Description must be at least 10 characters");
  }
  
  if (!supportingEvidence || supportingEvidence.length === 0) {
    throw new Error("At least one piece of supporting evidence is required");
  }

  return {
    finding_id: `find_${Math.floor(Math.random() * 10000)}`,
    workstream: workstream,
    severity: severity,
    status: "open",
    assigned_to: assignedAnalyst
  };
}