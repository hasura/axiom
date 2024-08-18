
/**
 * Formats a date string to a human-readable format.
 *
 * @param date The date string to format.
 * @returns The formatted date string.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function toDateString(date?: string): string {
  console.log("date", date);
  if (!date) {
    return "Invalid date";
  }
  try {
    return new Date(date).toDateString();
  } catch (error) {
    console.error("Error formatting date:", error);
    return "Invalid date";
  }
}

type SupportTicket = {
  ticketId: string;
  status: string;
  resolutionNotes: string;
  issue: string;
  date: string;
}

type UsageStats = {
  dataUsage: {
    currentMonth: string;
    total: string;
  };
  callStats: {
    totalMinutes: number;
    internationalMinutes: number;
  };
  appUsage: {
    usage: string;
    name: string;
  }[];
}

// const parseUsageString = (usage: string): number => {
//   const units = {
//     'KB': 1 / (1024 * 1024),
//     'MB': 1 / 1024,
//     'GB': 1,
//     'TB': 1024
//   };

//   const match = usage.match(/(\d+(\.\d+)?)([a-zA-Z]+)/);
//   if (!match) return 0;

//   const value = parseFloat(match[1]);
//   const unit = match[3].toUpperCase();

//   return value * (units[unit] || 0);
// };

/**
 * Calculates support score based on support history and open tickets.
 *
 * @param supportHistory The support history of the user.
 * @returns The calculated support score.
 * @readonly This function should only query data without making modifications
 * @allowrelaxedtypes
 * @paralleldegree 5
 */
export function calculateSupportScore(supportHistory: SupportTicket[], usageStats: UsageStats): number {
  let weightedScore = 1;

  // // Calculate support ticket score
  // supportHistory.forEach(ticket => {
  //   if (ticket.status === "Open") {
  //     weightedScore += 1.5; // Apply a weighting of 1.5 for open tickets
  //   } else {
  //     weightedScore += 1; // Normal weight for other statuses
  //   }
  // });

  // Calculate usage score
  // const dataUsageCurrentMonth = parseUsageString(usageStats.dataUsage.currentMonth);
  // const dataUsageTotal = parseUsageString(usageStats.dataUsage.total);
  // const totalCallMinutes = usageStats.callStats.totalMinutes;
  // const internationalCallMinutes = usageStats.callStats.internationalMinutes;

  // let appUsageTotal = 0;
  // usageStats.appUsage.forEach(app => {
  //   appUsageTotal += parseUsageString(app.usage);
  // });

  // Define weights for different usage components
  // const dataUsageWeight = 0.5;
  // const callMinutesWeight = 0.3;
  // const appUsageWeight = 0.2;

  // Calculate the usage score with the weights
  // const usageScore = (dataUsageCurrentMonth * dataUsageWeight) +
  //                    (totalCallMinutes * callMinutesWeight) +
  //                    (appUsageTotal * appUsageWeight);

  // weightedScore += usageScore;

  return weightedScore;
}

/**
 * Calculates engagement score based on user preferences and support history.
 *
 * @param emailUpdates The email updates setting of the user.
 * @param smsNotifications The sms notification setting of the user.
 * @param supportHistory The support history of the user.
 * @returns The calculated engagement score.
 * @readonly This function should only query data without making modifications
 * @allowrelaxedtypes
 * @paralleldegree 5
 */
export function calculateEngagementScore(emailUpdates: boolean, smsNotifications: boolean, appNotifications: any[]): number {
  let score = 0;
  if (emailUpdates) score += 10;
  if (smsNotifications) score += 10;
  if (Array.isArray(appNotifications) && appNotifications.some(notification => notification.enabled)) {
    score += 10;
  }

  return score;
}

/**
 * Formats a date string to ISO 8601 format.
 *
 * @param dateString The date string to format.
 * @returns The formatted date string in ISO 8601 format.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function formatDateToISO(dateString?: string): string {
  if (!dateString) {
    return "Invalid date";
  }
  try {
    return new Date(dateString).toISOString();
  } catch (error) {
    console.error("Error formatting date:", error);
    return "Invalid date";
  }
}

/**
 * Converts data usage from GB to MB.
 *
 * @param usageInGB The data usage in GB.
 * @returns The data usage in MB.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function convertDataUsageToMB(usageInGB: number): number {
  return usageInGB * 1024; // Convert GB to MB
}

/**
 * Converts currency amount to the target currency.
 *
 * @param amount The amount to convert.
 * @param currentCurrency The current currency of the amount.
 * @param targetCurrency The target currency to convert to.
 * @returns The converted amount in the target currency.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function convertCurrency(amount: number, currentCurrency: string, targetCurrency: string): number {
  const conversionRates: { [key: string]: { [key: string]: number } } = {
    'USD': { 'AUD': 1.3 },
    'AUD': { 'USD': 0.77 }
  };

  if (
    !conversionRates[currentCurrency] ||
    !conversionRates[currentCurrency][targetCurrency]
  ) {
    console.error(`Conversion rate not found for ${currentCurrency} to ${targetCurrency}`);
    return NaN;
  }

  const rate = conversionRates[currentCurrency][targetCurrency];
  return amount * rate;
}
