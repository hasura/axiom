/** 
Functions for supply chain demos are include below
please note that all functions must return complex values
*/

/** Begin ShipmentRequest */
/**
 * Creates a new Warehouse Shipment Request
 * @param shipmentData Data for the new product
 * @returns Created shipment request object
 */
interface ShipmentRequest {
  name: string;
  units: number;
  destination: string;
}
export async function createShipmentRequest(shipmentData: {
  product_name: string;
  unit_quantity: number;
  warehouse_destination: string;
}): 
  Promise<ShipmentRequest> {
  // Do a thing
  return {
    name: shipmentData.product_name,
    units: shipmentData.unit_quantity,
    destination: shipmentData.warehouse_destination
  }
}
/** End ShipmentRequest */

/** Begin LoyaltyRewardsRequest */
/**
 * Creates a new Loyalty Reward Request
 * @param rewardData Data for a customer
 * @returns Created reward request object
 */
interface LoyaltyRewardsRequest {
  name: string;
  amount: number;
  message: string;
}
export async function createLoyaltyRewardsRequest(rewardData: {
  customer_name: string;
  reward_amount: number;
  reward_message: string;
}): 
  Promise<LoyaltyRewardsRequest> {
  // Do a thing
  return {
    name: rewardData.customer_name,
    amount: rewardData.reward_amount,
    message: rewardData.reward_message
  }
}
/** End LoyaltyRewardsRequest */

