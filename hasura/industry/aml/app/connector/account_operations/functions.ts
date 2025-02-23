export interface SARFilingDetails {
  accountId: number;
  accountName: string;
  reason: string;
  suspiciousTransactions: {
    date: string;
    amount: number;
    beneficiary: string;
  }[];
  riskFactors: string[];
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

export async function fileSAR(
  details: SARFilingDetails
): Promise<SARFilingResponse> {
  if (!details.suspiciousTransactions?.length) {
    throw new Error("Suspicious transactions must be provided");
  }
  if (!details.riskFactors?.length) {
    throw new Error("Risk factors must be provided");
  }

  return {
    sar_id: `sar_${Math.floor(Math.random() * 10000)}`,
    account_id: details.accountId,
    status: "pending",
  };
}
