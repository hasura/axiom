export interface PromotionCreationResponse {
  promotion_id?: string;
  product_id: number;
  retailer_id: number;
  status: string;
}

export interface PricingUpdateResponse {
  update_id?: string;
  product_id: number;
  retailer_id: number;
  status: string;
}

export interface InventoryAllocationResponse {
  allocation_id?: string;
  product_id: number;
  warehouse_id: number;
  status: string;
}

/**
 * **Description:**
 * This function creates a new promotional campaign for specific products at targeted retailers. It establishes the promotion parameters including discount type, value, and duration. The function helps CPG companies drive sales, increase market share, and manage product lifecycle through strategic promotional activities. It automatically validates promotion parameters and ensures compliance with trade spending policies.
 *
 * **When to Call:**
 * - When launching new products to drive trial and awareness in the market.
 * - During seasonal peaks to maximize sales opportunities and market presence.
 * - To counter competitive activities and protect market share in key retailers.
 * - For inventory management of products approaching expiration or discontinuation.
 *
 * @param details
 */
export function createPromotion(
  productId: number,
  productName: string,
  retailerId: number,
  discountType: string,
  discountValue: number,
  startDate: string,
  endDate: string,
  minPurchaseQty?: number
): PromotionCreationResponse {
  if (discountValue <= 0) {
    throw new Error("Discount value must be positive");
  }
  
  if (new Date(startDate) >= new Date(endDate)) {
    throw new Error("End date must be after start date");
  }
  
  if (discountType !== "Percentage Off" && discountType !== "Dollar Off" && discountType !== "BOGO") {
    throw new Error("Invalid discount type. Must be 'Percentage Off', 'Dollar Off', or 'BOGO'");
  }

  return {
    promotion_id: `promo_${Math.floor(Math.random() * 10000)}`,
    product_id: productId,
    retailer_id: retailerId,
    status: "active",
  };
}

/**
 * **Description:**
 * This function updates product pricing across specified retail channels. It can adjust MSRP, wholesale pricing, or promotional pricing based on market conditions, competitive landscape, or strategic initiatives. The function ensures pricing consistency across channels while allowing for retailer-specific adjustments. It automatically validates pricing against margin thresholds and competitive positioning guidelines.
 *
 * **When to Call:**
 * - When raw material or production costs change requiring price adjustments.
 * - During competitive pricing pressures that require strategic responses.
 * - For implementing tiered pricing strategies across different retail channels.
 * - When executing planned price increases as part of product lifecycle management.
 *
 * @param details
 */
export function updateProductPricing(
  productId: number,
  productName: string,
  retailerId: number,
  newWholesalePrice: number,
  newMsrp: number,
  effectiveDate: string,
  reason: string
): PricingUpdateResponse {
  if (newWholesalePrice <= 0 || newMsrp <= 0) {
    throw new Error("Prices must be positive values");
  }
  
  if (newMsrp <= newWholesalePrice) {
    throw new Error("MSRP must be greater than wholesale price");
  }
  
  if (new Date(effectiveDate) < new Date()) {
    throw new Error("Effective date must be in the future");
  }

  return {
    update_id: `price_${Math.floor(Math.random() * 10000)}`,
    product_id: productId,
    retailer_id: retailerId,
    status: "scheduled",
  };
}

/**
 * **Description:**
 * This function manages inventory allocation across warehouses and retailers based on demand forecasts, promotional activities, and supply constraints. It optimizes product distribution to maximize availability while minimizing logistics costs and inventory holding. The function can prioritize allocation based on retailer tier, promotional commitments, or regional demand patterns.
 *
 * **When to Call:**
 * - During supply constraints when inventory must be strategically allocated.
 * - Before major promotional events to ensure sufficient stock at participating retailers.
 * - When implementing new distribution strategies or entering new markets.
 * - For seasonal products requiring specialized allocation patterns.
 *
 * @param details
 */
export function allocateInventory(
  productId: number,
  productName: string,
  warehouseId: number,
  retailerId: number,
  allocationQuantity: number,
  priorityLevel: string,
  reason: string
): InventoryAllocationResponse {
  if (allocationQuantity <= 0) {
    throw new Error("Allocation quantity must be positive");
  }
  
  if (priorityLevel !== "High" && priorityLevel !== "Medium" && priorityLevel !== "Low") {
    throw new Error("Priority level must be 'High', 'Medium', or 'Low'");
  }

  return {
    allocation_id: `alloc_${Math.floor(Math.random() * 10000)}`,
    product_id: productId,
    warehouse_id: warehouseId,
    status: "allocated",
  };
}
