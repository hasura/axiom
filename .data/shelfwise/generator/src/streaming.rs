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

    // NOTE: customers, customer_addresses, and delivery_drivers are NOT streamed.
    // They are written once at the end of generate_daily_data() to avoid truncation bugs.
    // All customer/driver data is held in memory (self.customers, etc.) and written atomically.

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

        // NOTE: customers, customer_addresses, and delivery_drivers are NOT opened here.
        // They are written once at the end of generate_daily_data() to avoid truncation bugs.

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

            // NOTE: Customer and driver headers are written in generate_daily_data()
            // when the files are created at the end of processing.
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

    #[allow(dead_code)]
    pub fn write_shipment(&mut self, record: &SupplierShipment) -> Result<()> {
        self.shipments_batch.push(record.clone());
        if self.shipments_batch.len() >= self.batch_size {
            self.flush_shipments_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_waste(&mut self, record: &WasteSpoilage) -> Result<()> {
        self.waste_batch.push(record.clone());
        if self.waste_batch.len() >= self.batch_size {
            self.flush_waste_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_ticket(&mut self, record: &Ticket) -> Result<()> {
        self.tickets_batch.push(record.clone());
        if self.tickets_batch.len() >= self.batch_size {
            self.flush_tickets_batch()?;
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn write_price_change(&mut self, record: &PriceChange) -> Result<()> {
        self.price_changes_batch.push(record.clone());
        if self.price_changes_batch.len() >= self.batch_size {
            self.flush_price_changes_batch()?;
        }
        Ok(())
    }

    pub fn write_transaction(&mut self, record: Transaction) -> Result<()> {
        self.transactions_batch.push(record);
        if self.transactions_batch.len() >= self.batch_size {
            self.flush_transactions_batch()?;
        }
        Ok(())
    }

    pub fn write_transaction_line_item(&mut self, record: TransactionLineItem) -> Result<()> {
        self.transaction_line_items_batch.push(record);
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

    // NOTE: write_customer, write_customer_address, and write_delivery_driver have been removed.
    // These are written once at the end of generate_daily_data() to avoid truncation bugs.

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
        Ok(())
    }

    // Batch extend methods for parallel processing results
    // These are available for future use when switching to fully parallel batch processing
    #[allow(dead_code)]
    pub fn extend_sales(&mut self, records: Vec<SalesDaily>) -> Result<()> {
        for record in records {
            self.sales_batch.push(record);
            if self.sales_batch.len() >= self.batch_size {
                self.flush_sales_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_returns(&mut self, records: Vec<ReturnDaily>) -> Result<()> {
        for record in records {
            self.returns_batch.push(record);
            if self.returns_batch.len() >= self.batch_size {
                self.flush_returns_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_shipments(&mut self, records: Vec<SupplierShipment>) -> Result<()> {
        for record in records {
            self.shipments_batch.push(record);
            if self.shipments_batch.len() >= self.batch_size {
                self.flush_shipments_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_waste(&mut self, records: Vec<WasteSpoilage>) -> Result<()> {
        for record in records {
            self.waste_batch.push(record);
            if self.waste_batch.len() >= self.batch_size {
                self.flush_waste_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_tickets(&mut self, records: Vec<Ticket>) -> Result<()> {
        for record in records {
            self.tickets_batch.push(record);
            if self.tickets_batch.len() >= self.batch_size {
                self.flush_tickets_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_price_changes(&mut self, records: Vec<PriceChange>) -> Result<()> {
        for record in records {
            self.price_changes_batch.push(record);
            if self.price_changes_batch.len() >= self.batch_size {
                self.flush_price_changes_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_transactions(&mut self, records: Vec<Transaction>) -> Result<()> {
        for record in records {
            self.transactions_batch.push(record);
            if self.transactions_batch.len() >= self.batch_size {
                self.flush_transactions_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_transaction_line_items(&mut self, records: Vec<TransactionLineItem>) -> Result<()> {
        for record in records {
            self.transaction_line_items_batch.push(record);
            if self.transaction_line_items_batch.len() >= self.batch_size {
                self.flush_transaction_line_items_batch()?;
            }
        }
        Ok(())
    }

    #[allow(dead_code)]
    pub fn extend_delivery_assignments(&mut self, records: Vec<DeliveryAssignment>) -> Result<()> {
        for record in records {
            self.delivery_assignments_batch.push(record);
            if self.delivery_assignments_batch.len() >= self.batch_size {
                self.flush_delivery_assignments_batch()?;
            }
        }
        Ok(())
    }
}