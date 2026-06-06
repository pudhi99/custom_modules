# Product Expiry Alert Manager
### Odoo 19 Community Edition Module

**Technical Name:** `stock_expiry_alert_manager`  
**Version:** 19.0.1.0.0  
**License:** LGPL-3  
**Price:** $14.99  

---

## What Does This Module Do?

Product Expiry Alert Manager is a **proactive stock expiry monitoring system** for Odoo 19 CE. It continuously watches your lot/serial number expiry dates and automatically alerts the right people at the right time — **before** products expire, not after.

### Key Features

| Feature | Description |
|---------|-------------|
| **Traffic-Light Dashboard** | Colour-coded Kanban: 🟢 GREEN / 🟡 YELLOW / 🔴 RED / ⬛ EXPIRED |
| **Tiered Email Alerts** | 5-level escalating emails at 30/15/7/3/1 days before expiry |
| **Auto Clearance Transfer** | Draft internal transfer to clearance location at RED threshold |
| **FIFO Sort Button** | One-click re-sort picking lines oldest-expiry-first |
| **Weekly Digest** | Monday 08:00 HTML email with value-at-risk summary |
| **Cost-at-Risk Report** | $ value of stock at each expiry tier, with graph/pivot |
| **Bulk Clearance Wizard** | Move multiple RED/EXPIRED lots to clearance in one action |
| **Manual Alert Wizard** | Send alert for any lot on-demand via Email or Odoo Inbox |
| **Export Wizard** | PDF or XLSX export of expiry data filtered by status/date |
| **Full Audit Trail** | Every alert, transfer, and digest logged in Alert History |

---

## Dependencies

- `stock` — Core stock management
- `product_expiry` — Adds expiration_date, use_date, removal_date, alert_date fields to stock.lot
- `mail` — Email and Odoo Inbox notifications

---

## Installation

1. Copy `stock_expiry_alert_manager/` to your Odoo addons path
2. Restart the Odoo server
3. Go to **Apps** → search `stock_expiry_alert_manager` → **Install**

---

## Configuration (after install)

1. **Enable lot tracking on products:**  
   `Inventory → Products → [Product] → Tracking = "By Lots"`

2. **Enable expiry dates on products:**  
   `Inventory → Products → [Product] → Inventory tab → Use Expiration Dates = ✓`

3. **Create a Clearance Location:**  
   `Inventory → Configuration → Locations → New`  
   Name: "Clearance" | Type: Internal

4. **Configure Expiry Alert Settings:**  
   `Inventory → Expiry Alerts → Settings`
   - Set threshold days (default: 30/15/7)
   - Set alert recipient users
   - Enable Auto Transfer + select clearance location
   - Optionally filter by product category or location

---

## Beginner Testing Guide

Follow these steps in sequence to verify every feature works correctly.

### Step 1 — Install and verify

- Go to **Apps**, search `stock_expiry_alert_manager`, click **Install**
- After install, navigate to **Inventory** in the main menu
- You should see **"Expiry Alerts"** in the Inventory menu

---

### Step 2 — Enable lot tracking on a test product

1. Go to `Inventory → Products → [any storable product]`
2. Set **Tracking** to `By Lots`
3. Go to the **Inventory tab** → enable `Use Expiration Dates`
4. Save

---

### Step 3 — Configure settings

1. `Inventory → Expiry Alerts → Settings`
2. Set thresholds: Green=30, Yellow=15, Red=7
3. Add your own user as an Alert Recipient
4. Enable **Auto-create Clearance Transfer**
5. Create a location first (Step 4), then return here to select it

---

### Step 4 — Create a clearance location

1. `Inventory → Configuration → Locations → New`
2. Name: `Clearance Zone` | Type: `Internal`
3. Save, then go back to Settings and select this as Clearance Location

---

### Step 5 — Create test lots with different expiry dates

Create a receipt for your test product. Create these lots:

| Lot Name | Expiry Date | Expected Status |
|----------|-------------|-----------------|
| LOT-SAFE | Today + 35 days | 🟢 GREEN |
| LOT-WARN | Today + 20 days | 🟡 YELLOW |
| LOT-WARN2 | Today + 10 days | 🟡 YELLOW |
| LOT-CRIT | Today + 5 days | 🔴 RED |
| LOT-CRIT2 | Today + 2 days | 🔴 RED |
| LOT-EXP | Yesterday | ⬛ EXPIRED |

Validate the receipt to put stock on hand.

---

### Step 6 — Run Cron 1: Compute Status

1. Go to `Settings → Technical → Scheduled Actions`
2. Find **"Stock Expiry: Compute Status & Auto Transfers"**
3. Click **Run Now** (button in the top toolbar)
4. Expected result:
   - All lots should have `expiry_status` computed
   - A draft internal transfer should appear for LOT-CRIT and LOT-CRIT2

---

### Step 7 — Verify the Dashboard

1. `Inventory → Expiry Alerts → Dashboard`
2. You should see a Kanban board with 4 columns: GREEN / YELLOW / RED / EXPIRED
3. Each lot card shows: Days remaining, Qty, Expiry date, Cost at Risk
4. Colour-coded borders match the status

---

### Step 8 — Run Cron 2: Daily Alerts

1. `Settings → Technical → Scheduled Actions`
2. Find **"Stock Expiry: Send Daily Alerts"** → **Run Now**
3. Go to `Settings → Technical → Email → Emails` → verify alert emails sent

---

### Step 9 — Check Alert History

1. `Inventory → Expiry Alerts → Alert History`
2. You should see records for each alert sent
3. Auto-transfers also appear in history

---

### Step 10 — Verify Auto Transfer

1. `Inventory → Transfers`
2. Filter by `Origin = "Expiry Alert"` or search for your lot name
3. You should see draft transfers for RED lots

---

### Step 11 — Test FIFO Sort

1. Create a delivery order with 2+ lots of the same product
2. Open the delivery → click **"Sort FIFO"** button
3. Move lines should reorder: oldest expiry date first

---

### Step 12 — Test Bulk Clearance Wizard

1. `Inventory → Expiry Alerts → Dashboard`
2. Click `Action → Bulk Clearance Transfer` (or via Technical menu)
3. Set Filter = "RED (Critical) only", select clearance location
4. Click **Create Transfers** → transfers appear

---

### Step 13 — Test Manual Alert

1. Open any lot with an expiry date
2. Click the **"Send Alert"** smart button (envelope icon)
3. Select recipients, choose Email or Inbox
4. Click **Send Alert**
5. Check email inbox / Odoo Discuss

---

### Step 14 — Test Export

1. Open any lot → click **Print** → **Expiry Report** (PDF)
2. Or go to `Action → Export Expiry Report` → choose XLSX

---

### Step 15 — Run Weekly Digest

1. `Settings → Technical → Scheduled Actions`
2. Find **"Stock Expiry: Weekly Digest"** → **Run Now**
3. Check email — you should receive an HTML digest with lot counts per tier

---

### Step 16 — Test Expired Lot Blocking

1. Create a delivery order and add LOT-EXP to the move lines
2. Click **Validate**
3. Expected: An error dialog preventing validation with an EXPIRED lot

---

### Step 17 — Cost at Risk Report

1. `Inventory → Expiry Alerts → Cost at Risk`
2. You should see rows for each tier with lot count and total cost
3. Switch to Graph view to see the bar chart

---

### Step 18 — Access Control

1. Log in as a non-manager warehouse user
2. You should NOT see the **Settings** menu under Expiry Alerts
3. You SHOULD see Dashboard, Expiring Lots, and Alert History

---

## Scheduled Jobs Summary

| Job | Schedule | Purpose |
|-----|----------|---------|
| Stock Expiry: Compute Status | Daily 07:00 | Updates expiry_status on all lots, creates clearance transfers |
| Stock Expiry: Send Daily Alerts | Daily 08:00 | Sends tiered emails to configured recipients |
| Stock Expiry: Weekly Digest | Monday 08:00 | Sends HTML digest with value-at-risk summary |

---

## Module Structure

```
stock_expiry_alert_manager/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── expiry_config.py        # Singleton settings model
│   ├── expiry_history.py       # Audit log model
│   ├── expiry_cost_report.py   # Cost-at-risk report model
│   ├── stock_lot.py            # Extends stock.lot (8 fields + 3 cron methods)
│   └── stock_picking.py        # Extends stock.picking (FIFO sort + expired block)
├── wizard/
│   ├── expiry_bulk_transfer.py # Bulk clearance wizard
│   ├── expiry_send_alert.py    # Manual alert wizard
│   └── expiry_export.py        # PDF/XLSX export wizard
├── views/                      # All XML view definitions
├── data/                       # Mail templates, cron jobs, default config
├── security/                   # Access rules and record rules
├── reports/                    # QWeb PDF report
└── static/description/         # icon.png, banner.png, feature_overview.png
```

---

## Support

**Author:** Prudhvi Inumarthi  
**Email:** prudhvi.inumarthi99@gmail.com  
**GitHub:** https://github.com/pudhi99
