use crate::models::*;
use anyhow::Result;
use csv::Writer;
use std::fs::File;
use std::io::BufWriter;
use std::path::Path;

// Increased buffer size for better I/O performance (16MB per writer)
const BUFFER_SIZE: usize = 16 * 1024 * 1024;

pub struct StreamingWriters {
    pub sales: Writer<BufWriter<File>>,
    pub inventory: Writer<BufWriter<File>>,
    pub returns: Writer<BufWriter<File>>,
    pub shipments: Writer<BufWriter<File>>,
    pub waste: Writer<BufWriter<File>>,
    pub tickets: Writer<BufWriter<File>>,
    pub price_changes: Writer<BufWriter<File>>,
    pub transactions: Writer<BufWriter<File>>,
    pub transaction_line_items: Writer<BufWriter<File>>,

    // Delivery writers
    pub delivery_assignments: Writer<BufWriter<File>>,

    // Customer writers (for incremental growth)
    pub customers: Writer<BufWriter<File>>,
    pub customer_addresses: Writer<BufWriter<File>>,

    // Driver writers (for incremental hiring)
    pub delivery_drivers: Writer<BufWriter<File>>,

    // Batch buffers for reduced write calls
    sales_batch: Vec<SalesDaily>,
    inventory_batch: Vec<InventoryDaily>,
    returns_batch: Vec<ReturnDaily>,
    shipments_batch: Vec<SupplierShipment>,
    waste_batch: Vec<WasteSpoilage>,
    tickets_batch: Vec<Ticket>,
    price_changes_batch: Vec<PriceChange>,
    transactions_batch: Vec<Transaction>,
    transaction_line_items_batch: Vec<TransactionLineItem>,
    delivery_assignments_batch: Vec<DeliveryAssignment>,
    customers_batch: Vec<Customer>,
    customer_addresses_batch: Vec<CustomerAddress>,
    delivery_drivers_batch: Vec<DeliveryDriver>,

    batch_size: usize,
}

impl StreamingWriters {
    pub fn with_batch_size(output_dir: &str, continue_mode: bool, batch_size: usize) -> Result<Self> {
        std::fs::create_dir_all(output_dir)?;

        let open_file = |path: std::path::PathBuf| -> Result<BufWriter<File>> {
            let file = if continue_mode {
                // In continue mode, create the file if it doesn't exist, then append
                // This allows continue-mode to work both when files exist (normal append)
                // and when they don't (e.g., after nightly cleanup between dates)
                std::fs::OpenOptions::new()
                    .append(true)
                    .create(true)
                    .open(path)?
            } else {
                File::create(path)?
            };
            Ok(BufWriter::with_capacity(BUFFER_SIZE, file))
        };

        let mut sales = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(512 * 1024)  // Increased CSV internal buffer
            .from_writer(open_file(Path::new(output_dir).join("sales_daily.csv"))?);
        let mut inventory = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(512 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("inventory_daily.csv"))?);
        let mut returns = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("returns_daily.csv"))?);
        let mut shipments = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("supplier_shipments.csv"))?);
        let mut waste = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(128 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("waste_spoilage.csv"))?);
        let mut tickets = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(128 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("tickets.csv"))?);
        let mut price_changes = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(128 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("price_changes.csv"))?);
        let mut transactions = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(512 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("transactions.csv"))?);
        let mut transaction_line_items = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(512 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("transaction_line_items.csv"))?);

        // Delivery writers
        let mut delivery_assignments = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("delivery_assignments.csv"))?);

        // Customer writers (for incremental growth)
        let mut customers = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("customers.csv"))?);
        let mut customer_addresses = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("customer_addresses.csv"))?);

        // Driver writers (for incremental hiring)
        let mut delivery_drivers = csv::WriterBuilder::new()
            .has_headers(false)
            .buffer_capacity(256 * 1024)
            .from_writer(open_file(Path::new(output_dir).join("delivery_drivers.csv"))?);

        if !continue_mode {
            sales.write_record(["date", "store_id", "sku", "units_sold", "gross_revenue", "promo_id",
                "regular_price", "net_price", "revenue", "supplier_rebate_amt", "spoilage_cost",
                "promo_funding_received", "gross_margin_pct", "discount_pct", "cogs_c", "cogs_s",
                "sales_date", "posting_date"])?;

            inventory.write_record(["date", "store_id", "sku", "on_hand", "on_order", "in_transit",
                "safety_stock", "last_scan_ts", "system_on_hand", "available_to_promise",
                "open_hours", "in_stock_hours", "dc_allocated_qty", "quarantine_hold"])?;

            returns.write_record(["date", "store_id", "sku", "units_returned", "reason_code", "refund_value",
                "transaction_id", "line_number"])?;

            shipments.write_record(["shipment_id", "shipment_date", "delivery_date", "store_id", "sku",
                "quantity_shipped", "quantity_received", "supplier_name", "po_number", "shipment_status"])?;

            waste.write_record(["waste_id", "date", "store_id", "sku", "quantity_wasted",
                "waste_reason", "waste_value", "recorded_by"])?;

            tickets.write_record(["ticket_id", "created_at", "resolved_at", "store_id", "sku",
                "issue_type", "description", "root_cause", "resolved"])?;

            price_changes.write_record(["change_id", "date", "store_id", "sku", "new_regular_price", "reason"])?;

            transactions.write_record(["transaction_id", "date", "store_id", "timestamp", "total_items",
                "payment_method", "customer_type", "total_amount", "customer_id", "is_loyalty_transaction",
                "loyalty_points_earned", "loyalty_points_redeemed", "fulfillment_type", "order_status",
                "fulfillment_store_id", "delivery_address_id", "delivery_fee", "tip_amount",
                "delivery_instructions", "requested_delivery_time", "actual_delivery_time"])?;

            transaction_line_items.write_record(["transaction_id", "line_number", "sku", "quantity",
                "unit_price", "line_total", "promo_id", "discount_amount"])?;

            // Delivery headers
            delivery_assignments.write_record(["assignment_id", "transaction_id", "driver_id",
                "assigned_at", "accepted_at", "picked_up_at", "delivered_at", "cancelled_at",
                "assignment_status", "cancellation_reason", "pickup_store_id", "estimated_pickup_time",
                "actual_pickup_time", "estimated_delivery_time", "actual_delivery_time",
                "distance_miles", "estimated_duration_minutes", "actual_duration_minutes",
                "driver_pay", "driver_tip", "driver_total_earnings", "customer_rating",
                "driver_notes", "customer_feedback"])?;

            // Customer headers
            customers.write_record(["customer_id", "email", "phone", "first_name", "last_name",
                "age_bracket", "household_size", "income_bracket", "primary_store_id", "primary_city",
                "home_latitude", "home_longitude", "loyalty_member", "loyalty_tier", "loyalty_join_date",
                "loyalty_points", "preferred_shopping_time", "avg_basket_size", "price_sensitivity",
                "customer_segment", "created_date", "has_online_account", "prefers_online"])?;

            customer_addresses.write_record(["address_id", "customer_id", "address_type", "is_default",
                "street_address", "apartment_unit", "city", "state", "zip_code", "latitude", "longitude",
                "delivery_instructions", "has_doorman", "requires_signature", "created_at"])?;

            // Driver headers
            delivery_drivers.write_record(["driver_id", "first_name", "last_name", "phone", "email",
                "driver_type", "employment_status", "primary_store_id", "service_radius_miles", "service_cities",
                "vehicle_type", "vehicle_capacity_items", "has_insulated_bags", "total_deliveries", "avg_rating",
                "on_time_delivery_pct", "acceptance_rate", "cancellation_rate", "is_available",
                "current_latitude", "current_longitude", "last_location_update", "hire_date", "last_delivery_date",
                "base_pay_per_delivery", "mileage_rate", "avg_tips_per_delivery"])?;
        }

        Ok(Self {
            sales,
            inventory,
            returns,
            shipments,
            waste,
            tickets,
            price_changes,
            transactions,
            transaction_line_items,
            delivery_assignments,
            customers,
            customer_addresses,
            delivery_drivers,
            sales_batch: Vec::with_capacity(batch_size),
            inventory_batch: Vec::with_capacity(batch_size),
            returns_batch: Vec::with_capacity(batch_size),
            shipments_batch: Vec::with_capacity(batch_size),
            waste_batch: Vec::with_capacity(batch_size),
            tickets_batch: Vec::with_capacity(batch_size),
            price_changes_batch: Vec::with_capacity(batch_size),
            transactions_batch: Vec::with_capacity(batch_size),
            transaction_line_items_batch: Vec::with_capacity(batch_size),
            delivery_assignments_batch: Vec::with_capacity(batch_size),
            customers_batch: Vec::with_capacity(batch_size),
            customer_addresses_batch: Vec::with_capacity(batch_size),
            delivery_drivers_batch: Vec::with_capacity(batch_size),
            batch_size,
        })
    }

    pub fn write_sales(&mut self, record: &SalesDaily) -> Result<()> {
        self.sales_batch.push(record.clone());
        if self.sales_batch.len() >= self.batch_size {
            self.flush_sales_batch()?;
        }
        Ok(())
    }

    pub fn write_inventory(&mut self, record: &InventoryDaily) -> Result<()> {
        self.inventory_batch.push(record.clone());
        if self.inventory_batch.len() >= self.batch_size {
            self.flush_inventory_batch()?;
        }
        Ok(())
    }

    pub fn write_return(&mut self, record: &ReturnDaily) -> Result<()> {
        self.returns_batch.push(record.clone());
        if self.returns_batch.len() >= self.batch_size {
            self.flush_returns_batch()?;
        }
        Ok(())
    }

    pub fn write_shipment(&mut self, record: &SupplierShipment) -> Result<()> {
        self.shipments_batch.push(record.clone());
        if self.shipments_batch.len() >= self.batch_size {
            self.flush_shipments_batch()?;
        }
        Ok(())
    }

    pub fn write_waste(&mut self, record: &WasteSpoilage) -> Result<()> {
        self.waste_batch.push(record.clone());
        if self.waste_batch.len() >= self.batch_size {
            self.flush_waste_batch()?;
        }
        Ok(())
    }

    pub fn write_ticket(&mut self, record: &Ticket) -> Result<()> {
        self.tickets_batch.push(record.clone());
        if self.tickets_batch.len() >= self.batch_size {
            self.flush_tickets_batch()?;
        }
        Ok(())
    }

    pub fn write_price_change(&mut self, record: &PriceChange) -> Result<()> {
        self.price_changes_batch.push(record.clone());
        if self.price_changes_batch.len() >= self.batch_size {
            self.flush_price_changes_batch()?;
        }
        Ok(())
    }

    pub fn write_transaction(&mut self, record: &Transaction) -> Result<()> {
        self.transactions_batch.push(record.clone());
        if self.transactions_batch.len() >= self.batch_size {
            self.flush_transactions_batch()?;
        }
        Ok(())
    }

    pub fn write_transaction_line_item(&mut self, record: &TransactionLineItem) -> Result<()> {
        self.transaction_line_items_batch.push(record.clone());
        if self.transaction_line_items_batch.len() >= self.batch_size {
            self.flush_transaction_line_items_batch()?;
        }
        Ok(())
    }

    pub fn write_delivery_assignment(&mut self, record: &DeliveryAssignment) -> Result<()> {
        self.delivery_assignments_batch.push(record.clone());
        if self.delivery_assignments_batch.len() >= self.batch_size {
            self.flush_delivery_assignments_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_customer(&mut self, record: &Customer) -> Result<()> {
        self.customers_batch.push(record.clone());
        if self.customers_batch.len() >= self.batch_size {
            self.flush_customers_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_customer_address(&mut self, record: &CustomerAddress) -> Result<()> {
        self.customer_addresses_batch.push(record.clone());
        if self.customer_addresses_batch.len() >= self.batch_size {
            self.flush_customer_addresses_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_delivery_driver(&mut self, record: &DeliveryDriver) -> Result<()> {
        self.delivery_drivers_batch.push(record.clone());
        if self.delivery_drivers_batch.len() >= self.batch_size {
            self.flush_delivery_drivers_batch()?;
        }
        Ok(())
    }

    fn flush_sales_batch(&mut self) -> Result<()> {
        for record in self.sales_batch.drain(..) {
            self.sales.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_inventory_batch(&mut self) -> Result<()> {
        for record in self.inventory_batch.drain(..) {
            self.inventory.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_returns_batch(&mut self) -> Result<()> {
        for record in self.returns_batch.drain(..) {
            self.returns.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_shipments_batch(&mut self) -> Result<()> {
        for record in self.shipments_batch.drain(..) {
            self.shipments.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_waste_batch(&mut self) -> Result<()> {
        for record in self.waste_batch.drain(..) {
            self.waste.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_tickets_batch(&mut self) -> Result<()> {
        for record in self.tickets_batch.drain(..) {
            self.tickets.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_price_changes_batch(&mut self) -> Result<()> {
        for record in self.price_changes_batch.drain(..) {
            self.price_changes.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_transactions_batch(&mut self) -> Result<()> {
        for record in self.transactions_batch.drain(..) {
            self.transactions.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_transaction_line_items_batch(&mut self) -> Result<()> {
        for record in self.transaction_line_items_batch.drain(..) {
            self.transaction_line_items.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_delivery_assignments_batch(&mut self) -> Result<()> {
        for record in self.delivery_assignments_batch.drain(..) {
            self.delivery_assignments.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_customers_batch(&mut self) -> Result<()> {
        for record in self.customers_batch.drain(..) {
            self.customers.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_customer_addresses_batch(&mut self) -> Result<()> {
        for record in self.customer_addresses_batch.drain(..) {
            self.customer_addresses.serialize(&record)?;
        }
        Ok(())
    }

    fn flush_delivery_drivers_batch(&mut self) -> Result<()> {
        for record in self.delivery_drivers_batch.drain(..) {
            self.delivery_drivers.serialize(&record)?;
        }
        Ok(())
    }

    pub fn flush_all(&mut self) -> Result<()> {
        // Flush all batches first
        self.flush_sales_batch()?;
        self.flush_inventory_batch()?;
        self.flush_returns_batch()?;
        self.flush_shipments_batch()?;
        self.flush_waste_batch()?;
        self.flush_tickets_batch()?;
        self.flush_price_changes_batch()?;
        self.flush_transactions_batch()?;
        self.flush_transaction_line_items_batch()?;
        self.flush_delivery_assignments_batch()?;
        self.flush_customers_batch()?;
        self.flush_customer_addresses_batch()?;
        self.flush_delivery_drivers_batch()?;

        // Then flush the writers
        self.sales.flush()?;
        self.inventory.flush()?;
        self.returns.flush()?;
        self.shipments.flush()?;
        self.waste.flush()?;
        self.tickets.flush()?;
        self.price_changes.flush()?;
        self.transactions.flush()?;
        self.transaction_line_items.flush()?;
        self.delivery_assignments.flush()?;
        self.customers.flush()?;
        self.customer_addresses.flush()?;
        self.delivery_drivers.flush()?;
        Ok(())
    }
}