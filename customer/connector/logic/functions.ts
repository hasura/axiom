
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
 * Masks a credit card number to hide all but the last four digits.
 *
 * @param cardNumber The credit card number to mask.
 * @returns The masked credit card number.
 * @readonly This function should only query data without making modifications
 * @paralleldegree 5
 */
export function maskCardNumber(cardNumber?: string): string {
  console.log("cardNumber", cardNumber);
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

