# Product Expiry Alert Manager
## Real-World Test & Practice Guide

**Scenario:** You are the Warehouse Manager at **NutriVita Distributors Pvt Ltd** — a food supplement and health product distributor. You stock Vitamin tablets, Protein powders, and Omega-3 capsules. Your warehouse frequently receives complaints about near-expiry stock being shipped to customers. This module will fix that.

---

## Company & Scenario Overview

| Field | Value |
|-------|-------|
| **Company** | NutriVita Distributors Pvt Ltd |
| **Industry** | Food Supplements / Health Products |
| **Warehouse** | NutriVita Main Warehouse |
| **Problem** | Expired stock being picked, customer complaints, financial loss |
| **Solution** | Product Expiry Alert Manager — automated monitoring & alerts |

**Products we will use:**
| Product | Category | Unit |
|---------|----------|------|
| Vitamin D3 Tablets 60s | Vitamins | Box |
| Omega-3 Fish Oil Capsules | Supplements | Bottle |
| Whey Protein Powder 1kg | Sports Nutrition | Bag |

---

## PHASE 1 — Setup (One-Time Configuration)

### Step 1.1 — Enable Lot Tracking in Inventory Settings

1. Go to **Inventory → Configuration → Settings**
2. Scroll to the **Traceability** section
3. Enable ✅ **Lots & Serial Numbers**
4. Click **Save**

> **Why:** The module tracks expiry dates per lot. Without lot tracking, no expiry dates can be recorded.

---

### Step 1.2 — Create the Clearance Location

This is where near-expiry stock will be moved automatically.

1. Go to **Inventory → Configuration → Locations**
2. Click **New**
3. Fill in:

| Field | Value |
|-------|-------|
| **Name** | Clearance Zone |
| **Parent Location** | NutriVita Main Warehouse |
| **Location Type** | Internal Location |
| **Short Name** | CLEAR |

4. Click **Save**

> **Why:** When a lot hits RED status (≤ 7 days), the module auto-creates a draft transfer moving stock here for quarantine.

---

### Step 1.3 — Create Product: Vitamin D3 Tablets

1. Go to **Inventory → Products → Products**
2. Click **New**
3. Fill in:

| Field | Value |
|-------|-------|
| **Product Name** | Vitamin D3 Tablets 60s |
| **Product Type** | Storable Product |
| **Unit of Measure** | Box |
| **Sales Price** | 12.50 |
| **Cost** | 7.00 |

4. Go to the **Inventory** tab:

| Field | Value |
|-------|-------|
| **Tracking** | By Lots |
| **Use Expiration Dates** | ✅ Enabled |
| **Expiration Time** | 730 (days from manufacture = 2 years) |
| **Best Before Time** | 700 |
| **Removal Date** | 710 |
| **Alert Date** | 700 |

5. Click **Save**

---

### Step 1.4 — Create Product: Omega-3 Fish Oil Capsules

1. Click **New** again
2. Fill in:

| Field | Value |
|-------|-------|
| **Product Name** | Omega-3 Fish Oil Capsules 90s |
| **Product Type** | Storable Product |
| **Unit of Measure** | Bottle |
| **Sales Price** | 18.00 |
| **Cost** | 10.00 |

3. **Inventory** tab:

| Field | Value |
|-------|-------|
| **Tracking** | By Lots |
| **Use Expiration Dates** | ✅ Enabled |
| **Expiration Time** | 548 (1.5 years) |

4. Click **Save**

---

### Step 1.5 — Create Product: Whey Protein Powder

1. Click **New**
2. Fill in:

| Field | Value |
|-------|-------|
| **Product Name** | Whey Protein Powder 1kg |
| **Product Type** | Storable Product |
| **Unit of Measure** | Bag |
| **Sales Price** | 45.00 |
| **Cost** | 28.00 |

3. **Inventory** tab:

| Field | Value |
|-------|-------|
| **Tracking** | By Lots |
| **Use Expiration Dates** | ✅ Enabled |
| **Expiration Time** | 365 (1 year) |

4. Click **Save**

---

### Step 1.6 — Configure Expiry Alert Settings

1. Go to **Inventory → Expiry Alerts → Settings**
2. Fill in every tab:

**Thresholds tab:**

| Field | Value | Meaning |
|-------|-------|---------|
| Green Threshold | 30 | > 30 days = SAFE |
| Yellow Threshold | 15 | 15–30 days = WARNING |
| Red Threshold | 7 | ≤ 7 days = CRITICAL |
| Alert 1 - Days Before Expiry | 30 | First email at 30 days |
| Alert 2 - Days Before Expiry | 15 | Second email at 15 days |
| Alert 3 - Days Before Expiry | 7 | Third email at 7 days |
| Alert 4 - Days Before Expiry | 3 | Urgent email at 3 days |
| Alert 5 - Days Before Expiry | 1 | Final email at 1 day |

**Auto Transfer tab:**

| Field | Value |
|-------|-------|
| Auto-create Clearance Transfer | ✅ Enabled |
| Clearance Location | NutriVita Main Warehouse / Clearance Zone |

**Recipients tab:**

| Field | Value |
|-------|-------|
| Alert Recipients | Administrator (your user) |
| Weekly Digest Recipients | Administrator (your user) |

3. Click **Save**

---

## PHASE 2 — Receive Stock (Create Test Lots)

We will create one receipt with **6 lots across 3 products**, each expiring at a different timeline to test all status tiers.

### Step 2.1 — Create a Purchase Receipt

1. Go to **Inventory → Operations → Receipts**
2. Click **New**
3. Fill in:

| Field | Value |
|-------|-------|
| **Operation Type** | Receipts |
| **Receive From** | Create vendor: HealthPlus Imports Ltd |
| **Scheduled Date** | Today |

4. Click **Add a line** and add these 6 lines:

| Product | Quantity | Lot Name | Expiry Date (from today) |
|---------|----------|----------|--------------------------|
| Vitamin D3 Tablets 60s | 200 Box | VD3-2026-001 | Today + **35 days** |
| Vitamin D3 Tablets 60s | 150 Box | VD3-2026-002 | Today + **12 days** |
| Omega-3 Fish Oil Capsules 90s | 100 Bottle | OMG-2026-001 | Today + **6 days** |
| Omega-3 Fish Oil Capsules 90s | 80 Bottle | OMG-2026-002 | Today + **2 days** |
| Whey Protein Powder 1kg | 60 Bag | WPP-2026-001 | Today + **20 days** |
| Whey Protein Powder 1kg | 40 Bag | WPP-2026-EXP | **Yesterday** (already expired) |

> **How to enter lot + expiry:** Click the detail icon (≡) on each line → enter Lot number → enter Expiry Date

5. Click **Validate** → confirm with **Immediate Transfer**

> **Expected Result:** All 6 lots are now in stock with expiry dates recorded. You can verify by going to **Inventory → Products → Lots/Serial Numbers**.

---

## PHASE 3 — Test Feature by Feature

---

### TEST 1 — Run Status Computation Cron

**Purpose:** Compute the expiry_status (GREEN/YELLOW/RED/EXPIRED) for all lots.

1. Go to **Settings → Technical → Scheduled Actions**
2. Find **"Stock Expiry: Compute Status & Auto Transfers"**
3. Click **▶ Run Manually** (the play button in the top toolbar)
4. Wait for the confirmation message

**Expected Results:**

| Lot | Days | Expected Status |
|-----|------|----------------|
| VD3-2026-001 | +35 | 🟢 GREEN |
| VD3-2026-002 | +12 | 🟡 YELLOW |
| WPP-2026-001 | +20 | 🟡 YELLOW |
| OMG-2026-001 | +6 | 🔴 RED |
| OMG-2026-002 | +2 | 🔴 RED |
| WPP-2026-EXP | -1 | ⬛ EXPIRED |

✅ **Verify:** Go to **Inventory → Expiry Alerts → Expiring Lots** → confirm status column shows correct values.

---

### TEST 2 — Expiry Dashboard (Kanban Board)

**Purpose:** See the traffic-light visual overview of all stock.

1. Go to **Inventory → Expiry Alerts → Dashboard**
2. The view opens as a **Kanban board grouped by status**

**Expected Result:**
- **GREEN column:** VD3-2026-001 (200 boxes, 35 days)
- **YELLOW column:** VD3-2026-002 (12 days), WPP-2026-001 (20 days)
- **RED column:** OMG-2026-001 (6 days), OMG-2026-002 (2 days)
- **EXPIRED column:** WPP-2026-EXP (-1 day)

Each card shows:
- Lot name and Product name
- Days remaining badge (CRITICAL / WARNING / SAFE / EXPIRED)
- Quantity on hand
- Expiry date
- Cost at risk

✅ **Verify:** You can see all 6 lots in the correct columns with correct information.

---

### TEST 3 — Auto Clearance Transfer

**Purpose:** Verify that a draft transfer was automatically created for RED lots.

1. Go to **Inventory → Operations → Transfers**
2. Search for transfers with **Origin** containing "Expiry Alert"

**Expected Result:** Two draft transfers should exist:
- Transfer for **OMG-2026-001** → Clearance Zone (6 days remaining)
- Transfer for **OMG-2026-002** → Clearance Zone (2 days remaining)

Each transfer shows:
- Source: WH/Stock (or wherever the lot was stored)
- Destination: NutriVita Main Warehouse / Clearance Zone
- Product and lot detail
- Status: Draft (ready to process)

✅ **Verify:** Open one transfer → confirm lot name, quantity, and destination location.

> **Note:** Auto-transfer only creates **once** per lot (field `auto_transfer_created = True` prevents duplicates).

---

### TEST 4 — Send Daily Alerts Email

**Purpose:** Send tiered email alerts for expiring lots.

1. Go to **Settings → Technical → Scheduled Actions**
2. Find **"Stock Expiry: Send Daily Alerts"**
3. Click **▶ Run Manually**

**Expected Result:**
- Emails sent to your configured recipients for lots within alert windows (30/15/7/3/1 days)
- Each email has different styling based on urgency level

✅ **Verify:**
- Go to **Settings → Technical → Email → Emails**
- You should see outgoing emails with subjects like:
  - `⚠️ Expiry Notice (30 days): Vitamin D3 Tablets 60s — Lot VD3-2026-001`
  - `🔴 CRITICAL Expiry (7 days): Omega-3 Fish Oil Capsules — Lot OMG-2026-001`
  - `🆘 EXPIRES TOMORROW: Omega-3 Fish Oil Capsules — Lot OMG-2026-002`

---

### TEST 5 — Alert History Log

**Purpose:** Verify that every alert sent is recorded in the audit trail.

1. Go to **Inventory → Expiry Alerts → Alert History**

**Expected Result:** Records exist for:
- Each email alert sent (one per lot per level)
- Each auto-transfer created (type = "Auto Transfer Created")
- Each row shows: Alert Date, Lot, Product, Status, Days to Expiry, Alert Type, Transfer link

✅ **Verify:** Click any record → see full detail including recipient list.

---

### TEST 6 — Lot Form: Expiry Alerts Tab

**Purpose:** See expiry information and history directly on a lot.

1. Go to **Inventory → Products → Lots/Serial Numbers**
2. Open lot **OMG-2026-001**

**Expected Result on the form:**
- A **RED banner** at the top: "This lot is CRITICAL — expires in 6 days"
- **Smart buttons** at top right:
  - Bell icon showing alert count (e.g. "1 Alert")
  - Envelope icon "Send Alert" button
- **Expiry Alerts tab** showing:
  - Status: Red
  - Days to Expiry: 6
  - Estimated Cost: 100 bottles × $10 = $1,000
  - Alerts Sent: 1
  - Alert history table showing all past alerts

✅ **Verify:** Check that VD3-2026-001 shows a GREEN status (no banner), WPP-2026-EXP shows "EXPIRED" banner.

---

### TEST 7 — Manual Alert (Send Now Wizard)

**Purpose:** Send an alert for any lot on-demand.

1. Open lot **WPP-2026-EXP** (the expired lot)
2. Click the **"Send Alert"** smart button (envelope icon)
3. The wizard opens:

| Field | Value |
|-------|-------|
| Lots | WPP-2026-EXP (pre-filled) |
| Alert Channel | Email + Inbox |
| Recipients | Administrator |
| Custom Message | "This batch is expired — please quarantine immediately and inform QA team." |

4. Click **Send Alert**

**Expected Result:**
- Email sent immediately with your custom message
- Odoo Discuss notification appears for the recipient
- Alert count on the lot increases by 1
- New record appears in Alert History with type "Manual"

✅ **Verify:** Open the lot again → alert count incremented. Check Discuss (chat icon) for inbox notification.

---

### TEST 8 — FIFO Sort on Delivery Order

**Purpose:** Test that picking lines are auto-sorted oldest-expiry-first.

1. Go to **Inventory → Operations → Delivery Orders**
2. Click **New**
3. Fill in:

| Field | Value |
|-------|-------|
| Deliver To | Create customer: HealthFirst Pharmacy |
| Scheduled Date | Today |

4. Add a product line:
   - Product: **Vitamin D3 Tablets 60s**
   - Quantity: 50

5. Click **Check Availability** → lines should populate with both lots (VD3-2026-001 and VD3-2026-002)

6. Click **"Sort FIFO"** button (in the header, before Validate)

**Expected Result:**
- VD3-2026-002 (expiry: 12 days) appears **FIRST** in the lines
- VD3-2026-001 (expiry: 35 days) appears **SECOND**
- A success notification: "Move lines have been sorted oldest-expiry-first"

✅ **Verify:** The line with the earlier expiry date (VD3-2026-002) is now at the top.

---

### TEST 9 — Expired Lot Validation Block

**Purpose:** Verify that the system PREVENTS validating a delivery with an expired lot.

1. Create a new **Delivery Order**
2. Add product: **Whey Protein Powder 1kg**
3. Manually set Lot to: **WPP-2026-EXP** (the expired one)
4. Click **Validate**

**Expected Result:**
- A **red banner** warning appears on the form: "Expiry Warning: This transfer contains lots that are critical or expired."
- When you click Validate, an **error dialog** appears:
  ```
  The following lots are EXPIRED and cannot be shipped:
  WPP-2026-EXP
  ```
- Validation is **blocked**

✅ **Verify:** The system protects customers from receiving expired stock — validation is not possible.

---

### TEST 10 — Bulk Clearance Transfer Wizard

**Purpose:** Move all RED and EXPIRED lots to clearance in one action.

1. Go to **Inventory → Expiry Alerts → Dashboard**
2. Click **Action** menu → **Bulk Clearance Transfer**
   *(Or navigate via Settings → Technical → Actions)*

3. The wizard opens. Fill in:

| Field | Value |
|-------|-------|
| Move Lots With Status | RED + EXPIRED |
| Clearance Location | NutriVita Main Warehouse / Clearance Zone |

4. Observe the preview:
   - **Lots to Move:** 3 (OMG-2026-001, OMG-2026-002, WPP-2026-EXP)
   - **Total Cost at Risk:** approximately $1,920 (80 + 80 + 40 × costs)

5. Click **Create Transfers**

**Expected Result:**
- Draft internal transfers created for all 3 RED/EXPIRED lots
- System redirects you to a list of the created transfers
- Each transfer shows correct product, lot, quantity, and destination

✅ **Verify:** All 3 transfers visible → open each → confirm lot details correct.

---

### TEST 11 — Cost at Risk Report

**Purpose:** See the financial value of stock at each expiry tier.

1. Go to **Inventory → Expiry Alerts → Cost at Risk**

**Expected Result (List View):**

| Date | Tier | Lots | Products | Qty | Total Cost |
|------|------|------|---------|-----|-----------|
| Today | GREEN | 1 | 1 | 200 | $1,400 |
| Today | YELLOW | 2 | 2 | 230 | $2,176 |
| Today | RED | 2 | 1 | 180 | $1,800 |
| Today | EXPIRED | 1 | 1 | 40 | $1,120 |

2. Click the **Graph** view icon → you see a bar chart comparing cost by tier
3. Click the **Pivot** view → rotate/drill into data by date and tier

✅ **Verify:** Total cost across all tiers reflects your test product quantities × standard prices.

---

### TEST 12 — Export Report (PDF)

**Purpose:** Generate a PDF report of expiring lots for management.

1. Open any lot (e.g., **OMG-2026-001**)
2. Click **Print** button → **Expiry Report**

**Expected Result:**
- PDF opens/downloads with:
  - Company header
  - RED status badge
  - Lot details table (product, expiry date, days remaining, qty, cost)
  - Alert history table

✅ **Verify:** PDF is readable, correct lot name and status appear.

---

### TEST 13 — Export Report (XLSX)

**Purpose:** Export filtered expiry data to Excel for analysis.

1. Go to **Inventory → Expiry Alerts → Expiring Lots**
2. Click **Action** → **Export Expiry Report**
3. Fill in:

| Field | Value |
|-------|-------|
| Export Format | Excel (XLSX) |
| Filter by Status | YELLOW + RED |
| Expiry Date From | (leave blank) |
| Expiry Date To | (leave blank) |

4. Click **Export**
5. Click the **Download** button that appears

**Expected Result:**
- Excel file downloads with columns:
  - Lot/Serial, Product, Status, Days to Expiry, Expiry Date, Qty on Hand, Estimated Cost, Location
- RED rows highlighted in red, YELLOW rows in yellow
- Data sorted oldest-expiry-first

✅ **Verify:** Open the Excel file — 4 rows visible (2 YELLOW + 2 RED) with colour coding.

---

### TEST 14 — Weekly Digest Email

**Purpose:** Receive a summary of the full expiry situation every Monday.

1. Go to **Settings → Technical → Scheduled Actions**
2. Find **"Stock Expiry: Weekly Digest"**
3. Click **▶ Run Manually**

**Expected Result:**
- HTML email arrives at configured digest recipient addresses
- Email shows a summary table:

```
Tier              | Lots | Value
EXPIRED           |  1   | -
CRITICAL (RED)    |  2   | -
WARNING (YELLOW)  |  2   | -
SAFE (GREEN)      |  1   | -
```

- Clean formatted HTML with color-coded rows
- Footer shows auto-generation info

✅ **Verify:** Check your email inbox or Settings → Technical → Emails.

---

### TEST 15 — Snooze Alert on a Lot

**Purpose:** Suppress alerts for a lot that you are already handling.

1. Open lot **OMG-2026-001**
2. Go to the **Expiry Alerts** tab
3. Set **Snooze Alerts Until:** today + 3 days

4. Run the Daily Alerts cron again (Step → TEST 4)

**Expected Result:**
- OMG-2026-001 is **skipped** in the alert run for the next 3 days
- Other lots still get alerts as normal
- Useful when you are already in the process of returning stock and don't want noise

✅ **Verify:** Alert History has no new entry for OMG-2026-001 after running the cron again.

---

### TEST 16 — Access Control (Non-Manager User)

**Purpose:** Confirm that warehouse staff cannot access Settings.

1. Go to **Settings → Users**
2. Create a test user:

| Field | Value |
|-------|-------|
| Name | Ravi Kumar |
| Email | ravi@nutrivita.com |
| Job Position | Warehouse Staff |
| Inventory Access | User (not Manager) |

3. Log in as Ravi Kumar
4. Go to **Inventory → Expiry Alerts**

**Expected Result:**
- Ravi can see: **Dashboard**, **Expiring Lots**, **Alert History**, **Cost at Risk**
- Ravi **CANNOT see**: **Settings** menu item (hidden for non-managers)
- Ravi **CANNOT edit** Alert History records (read-only)

✅ **Verify:** Settings menu is absent for Ravi. Dashboard and lots are visible.

---

## Summary: Full Feature Coverage

| Feature | Test | Status |
|---------|------|--------|
| Status computation (GREEN/YELLOW/RED/EXPIRED) | TEST 1 | |
| Traffic-light Kanban Dashboard | TEST 2 | |
| Auto clearance transfer at RED | TEST 3 | |
| Daily tiered email alerts | TEST 4 | |
| Audit trail / Alert History | TEST 5 | |
| Lot form: Expiry tab + banners | TEST 6 | |
| Manual alert wizard | TEST 7 | |
| FIFO sort on picking | TEST 8 | |
| Expired lot validation block | TEST 9 | |
| Bulk clearance wizard | TEST 10 | |
| Cost at Risk report | TEST 11 | |
| PDF export | TEST 12 | |
| XLSX export | TEST 13 | |
| Weekly digest email | TEST 14 | |
| Snooze alerts | TEST 15 | |
| Access control (manager vs staff) | TEST 16 | |

**All 16 tests passed = Module fully functional ✅**

---

## Real-World Business Value Demonstrated

By completing these tests with NutriVita Distributors, you have proven:

1. **No expired stock ships** — TEST 9 blocks delivery validation
2. **Early warnings work** — TEST 4 sends emails 30 days before expiry
3. **Stock is automatically quarantined** — TEST 3 creates clearance transfers
4. **FIFO is enforced** — TEST 8 sorts oldest-first to consume before newer stock
5. **Finance has visibility** — TEST 11 shows cost at risk per tier
6. **Full audit trail** — TEST 5 proves every action is logged
7. **Management gets weekly overview** — TEST 14 sends Monday digest

**Estimated ROI:** For a distributor with 100 SKUs moving ₹50L stock monthly, preventing even 2% expiry loss = ₹1L/month saved.

---

## Troubleshooting Quick Reference

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Lots show no expiry_status | Cron not run | Run "Compute Status" cron manually |
| No email received | Email server not configured | Settings → Technical → Outgoing Mail Server |
| Auto transfer not created | Clearance location not set | Settings → Expiry Alerts → Auto Transfer tab |
| FIFO button not visible | Picking already done/cancelled | Only visible in draft/confirmed state |
| Status shows False | Product has no "Use Expiration Dates" | Enable on Product → Inventory tab |
| Cost shows 0 | Standard price not set on product | Set Cost field on product form |

---

*Guide version: 19.0.1.0.0 | NutriVita Distributors scenario | All product names are fictional for demonstration*
