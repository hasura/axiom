use crate::models::*;
use anyhow::Result;
use csv::Writer;
use std::fs::File;
use std::path::Path;

pub struct StreamingWriters {
    pub sales: Writer<File>,
    pub inventory: Writer<File>,
    pub returns: Writer<File>,
    pub shipments: Writer<File>,
    pub waste: Writer<File>,
    pub tickets: Writer<File>,
    pub price_changes: Writer<File>,
    pub transactions: Writer<File>,
}

impl StreamingWriters {
    pub fn new(output_dir: &str, continue_mode: bool) -> Result<Self> {
        std::fs::create_dir_all(output_dir)?;
        
        let open_file = |path: std::path::PathBuf| -> Result<File> {
            if continue_mode {
                Ok(std::fs::OpenOptions::new().append(true).open(path)?)
            } else {
                Ok(File::create(path)?)
            }
        };

        let mut sales = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("sales_daily.csv"))?);
        let mut inventory = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("inventory_daily.csv"))?);
        let mut returns = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("returns_daily.csv"))?);
        let mut shipments = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("supplier_shipments.csv"))?);
        let mut waste = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("waste_spoilage.csv"))?);
        let mut tickets = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("tickets.csv"))?);
        let mut price_changes = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("price_changes.csv"))?);
        let mut transactions = csv::WriterBuilder::new().has_headers(false).from_writer(open_file(Path::new(output_dir).join("transactions.csv"))?);

        if !continue_mode {
            sales.write_record(&["date", "store_id", "sku", "units_sold", "gross_revenue", "promo_id",
                "regular_price", "net_price", "revenue", "supplier_rebate_amt", "spoilage_cost",
                "promo_funding_received", "gross_margin_pct", "discount_pct", "cogs_c", "cogs_s",
                "sales_date", "posting_date"])?;
            
            inventory.write_record(&["date", "store_id", "sku", "on_hand", "on_order", "in_transit",
                "safety_stock", "last_scan_ts", "system_on_hand", "available_to_promise",
                "open_hours", "in_stock_hours", "dc_allocated_qty", "quarantine_hold"])?;
            
            returns.write_record(&["date", "store_id", "sku", "units_returned", "reason_code", "refund_value"])?;
            
            shipments.write_record(&["shipment_id", "shipment_date", "delivery_date", "store_id", "sku",
                "quantity_shipped", "quantity_received", "supplier_name", "po_number", "shipment_status"])?;
            
            waste.write_record(&["waste_id", "date", "store_id", "sku", "quantity_wasted",
                "waste_reason", "waste_value", "recorded_by"])?;
            
            tickets.write_record(&["ticket_id", "created_at", "resolved_at", "store_id", "sku",
                "issue_type", "description", "root_cause", "resolved"])?;
            
            price_changes.write_record(&["change_id", "date", "store_id", "sku", "new_regular_price", "reason"])?;
            
            transactions.write_record(&["transaction_id", "date", "store_id", "timestamp", "total_items",
                "payment_method", "customer_type", "total_amount"])?;
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
        })
    }

    pub fn write_sales(&mut self, record: &SalesDaily) -> Result<()> {
        self.sales.serialize(record)?;
        Ok(())
    }

    pub fn write_inventory(&mut self, record: &InventoryDaily) -> Result<()> {
        self.inventory.serialize(record)?;
        Ok(())
    }

    pub fn write_return(&mut self, record: &ReturnDaily) -> Result<()> {
        self.returns.serialize(record)?;
        Ok(())
    }

    pub fn write_shipment(&mut self, record: &SupplierShipment) -> Result<()> {
        self.shipments.serialize(record)?;
        Ok(())
    }

    pub fn write_waste(&mut self, record: &WasteSpoilage) -> Result<()> {
        self.waste.serialize(record)?;
        Ok(())
    }

    pub fn write_ticket(&mut self, record: &Ticket) -> Result<()> {
        self.tickets.serialize(record)?;
        Ok(())
    }

    pub fn write_price_change(&mut self, record: &PriceChange) -> Result<()> {
        self.price_changes.serialize(record)?;
        Ok(())
    }

    pub fn write_transaction(&mut self, record: &Transaction) -> Result<()> {
        self.transactions.serialize(record)?;
        Ok(())
    }

    pub fn flush_all(&mut self) -> Result<()> {
        self.sales.flush()?;
        self.inventory.flush()?;
        self.returns.flush()?;
        self.shipments.flush()?;
        self.waste.flush()?;
        self.tickets.flush()?;
        self.price_changes.flush()?;
        self.transactions.flush()?;
        Ok(())
    }
}