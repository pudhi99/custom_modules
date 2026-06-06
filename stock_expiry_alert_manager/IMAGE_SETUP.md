# Image Setup for App Listing

## Current Status

✅ **Manifest updated:** `'application': True` — module now displays in Odoo Apps  
✅ **Images referenced:** All 3 image paths in manifest  
⚠️ **Image files exist** but may not be at optimal marketplace resolution

---

## Required Image Specifications

Replace the images in `static/description/` with these exact sizes:

| File | Size | Purpose |
|------|------|---------|
| **icon.png** | **128×128 px** | App icon in Odoo Apps listing |
| **banner.png** | **1280×1493 px** | Marketplace preview banner |
| **feature_overview.png** | **1200×630 px** | Social media / feature card |

---

## How to Generate Images

### Option 1: ChatGPT / DALL·E (Recommended)

Use the prompts in `generate_images_prompt.md`:

```bash
# Open generate_images_prompt.md
# Copy each prompt into ChatGPT (DALL·E)
# Download at specified resolution
# Save to static/description/
```

### Option 2: Canva (Free)

1. Go to **canva.com**
2. Create new design → select dimension (128×128, 1280×1493, 1200×630)
3. Design with:
   - **Icon:** Shield + clock + traffic-light colors
   - **Banner:** Dark gradient, UI mockups, feature list
   - **Overview:** Green/yellow/red Kanban preview
4. Download as PNG
5. Save to `static/description/`

### Option 3: Online Image Editor (Resize current images)

If current images look good, just resize them:

```bash
# Using Python + Pillow:
python -c "
from PIL import Image

# Icon
img = Image.open('icon.png').resize((128, 128))
img.save('icon.png')

# Banner
img = Image.open('banner.png').resize((1280, 1493))
img.save('banner.png')

# Overview
img = Image.open('feature_overview.png').resize((1200, 630))
img.save('feature_overview.png')
"
```

---

## Verification

After adding images, restart Odoo and check:

1. Go to **Apps** (top menu)
2. Search for **"Product Expiry Alert Manager"**
3. Verify:
   - ✅ Icon displays correctly
   - ✅ Summary text visible
   - ✅ "Install" button shows
   - ✅ Click to see banner + details

---

## App Display Checklist

- [x] `'application': True` in manifest
- [x] `'images': [...]` lists all 3 files
- [x] `static/description/` directory exists
- [ ] **icon.png** — 128×128 px (REPLACE WITH PROPER IMAGE)
- [ ] **banner.png** — 1280×1493 px (REPLACE WITH PROPER IMAGE)
- [ ] **feature_overview.png** — 1200×630 px (REPLACE WITH PROPER IMAGE)

Once images are at correct size, the module will display professionally in Odoo Apps marketplace.
