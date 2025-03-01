export interface SARFilingDetails {
  accountId: number;
  accountName: string;
  reason: string;
}

export interface AccountFreezeDetails {
  accountId: number;
  accountName: string;
  reason: string;
  freezeLevel: string;
  transactionThreshold?: number;
}

export interface TransactionHoldDetails {
  accountId: number;
  accountName: string;
  thresholdAmount: number;
  holdDuration: number;
  reason: string;
}

export interface SARFilingResponse {
  sar_id?: string;
  account_id: number;
  status: string;
}

export interface AccountFreezeResponse {
  freeze_id?: string;
  account_id: number;
  status: string;
}

export interface TransactionHoldResponse {
  hold_id?: string;
  account_id: number;
  status: string;
}

/**
 * **Description:**
 * This function places a temporary hold on transactions exceeding a specified threshold amount for a defined duration. It is designed to ensure that high-value transactions undergo additional scrutiny before being processed. By temporarily restricting transactions, this function helps prevent unauthorized access, mitigate fraud, and comply with regulatory requirements.
 *
 * **When to Call:**
 * - Before processing large withdrawals, wire transfers, or high-value purchases that require verification.
 * - When a customer requests a temporary spending limit as a security measure.
 * - As part of an automated fraud detection workflow to prevent potentially fraudulent transactions.
 *
 * @param details
 */
export async function holdTransactions(
  details: TransactionHoldDetails
): Promise<TransactionHoldResponse> {
  if (details.thresholdAmount <= 0) {
    throw new Error("Threshold amount must be positive");
  }
  if (details.holdDuration <= 0) {
    throw new Error("Hold duration must be positive");
  }

  return {
    hold_id: `hold_${Math.floor(Math.random() * 10000)}`,
    account_id: details.accountId,
    status: "hold placed",
  };
}

/**
 * **Description:**
 * This function fully or partially freezes an account to prevent unauthorized transactions. A full freeze blocks all transactions, while a partial freeze imposes specific restrictions based on transaction limits. This function is crucial for fraud mitigation, regulatory compliance, and safeguarding customer funds in cases of suspected account compromise.
 *
 * **When to Call:**
 * - Immediately after identifying suspicious activities indicative of account takeover or fraud.
 * - When law enforcement or regulatory agencies require an account freeze as part of an investigation.
 * - If a customer reports unauthorized access or requests a temporary block on their account.
 *
 * @param details
 */
export async function freezeAccount(
  details: AccountFreezeDetails
): Promise<AccountFreezeResponse> {
  if (details.freezeLevel === 'partial' && !details.transactionThreshold) {
    throw new Error("Transaction threshold required for partial freeze");
  }

  return {
    freeze_id: `freeze_${Math.floor(Math.random() * 10000)}`,
    account_id: details.accountId,
    status: details.freezeLevel === 'full' ? "fully frozen" : "partially frozen",
  };
}

/**
 * **Description:**
 * This function generates and files a Suspicious Activity Report (SAR) when a pattern of high-risk transactions or behaviors suggests potential financial crimes such as money laundering or fraud. The SAR filing provides documented evidence for compliance teams and regulatory bodies to review and take appropriate actions.
 *
 * **When to Call:**
 * - When an account exhibits transactions or behaviors consistent with known fraud patterns or money laundering schemes.
 * - If internal risk teams identify multiple suspicious transactions requiring formal documentation.
 * - When compliance regulations mandate the reporting of unusual account activities for further investigation.
 *
 * @param details
 */
export async function fileSAR(
  details: SARFilingDetails
): Promise<SARFilingResponse> {

  return {
    sar_id: `sar_${Math.floor(Math.random() * 10000)}`,
    account_id: details.accountId,
    status: "pending",
  };
}
