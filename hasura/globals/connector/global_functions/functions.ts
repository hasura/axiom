
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
 * Converts data from GB to MB.
 *
 * @param dataInGB The data in GB.
 * @returns The data usage in MB.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function convertDataToMB(dataInGB: number): number {
  return dataInGB * 1024; // Convert GB to MB
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
