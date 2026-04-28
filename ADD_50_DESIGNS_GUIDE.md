# Add 50+ Jewelry Designs Guide

## 🎯 Goal
Add at least 40-60 high-quality gold jewelry designs to display:
- **4 cards per row** on desktop
- **10+ rows** of jewelry
- **Unique images** for each design
- **Proper product names** and descriptions

---

## 🚀 Quick Start (One Command)

### Option 1: Reset and Seed (Recommended)
This clears old demo data and adds 60 fresh designs:

```bash
python reset_and_seed.py
```

### Option 2: Add to Existing Data
This keeps existing designs and adds 60 more:

```bash
python seed_50_designs.py
```

---

## 📊 What You'll Get

### Design Distribution:
- **Necklaces:** 12 designs
- **Rings:** 12 designs
- **Bangles:** 12 designs
- **Earrings:** 12 designs
- **Bracelets:** 12 designs
- **Total:** 60 designs = **15 rows** of 4 cards

### Grid Layout:
```
Desktop (>1400px):  4 cards per row
Tablet (1024-1400): 3 cards per row
Mobile (640-1024):  2 cards per row
Small Mobile (<640): 2 cards per row
```

---

## 🎨 Image Quality

All images are:
- ✅ High-resolution (800x800px)
- ✅ Quality 90 (Unsplash)
- ✅ Properly cropped and fitted
- ✅ Real gold jewelry photos
- ✅ Unique for each design

### Image Sources:
- Professional jewelry photography from Unsplash
- Curated collection of gold jewelry
- Different angles and styles
- Consistent quality across all categories

---

## 📝 Product Details

Each design includes:

### Basic Info:
- **Category:** Necklace, Ring, Bangle, Earring, Bracelet
- **Purity:** 18K or 22K gold (mostly 22K)
- **Weight:** Realistic weight ranges per category
- **Occasion Tag:** Wedding, Engagement, Festive, Traditional, Party, Daily Wear

### Pricing:
- **Gold Rate:** ₹6,479/gram (real 22K rate)
- **Making Charge:** ₹800-₹2,500 (realistic range)
- **GST:** 3% calculated automatically
- **Total Price:** Transparent breakdown

### Display Name Format:
```
"22K Gold Necklace"
"18K Gold Ring"
"22K Gold Bangle"
```

---

## 🔧 Technical Details

### Files Created:

1. **seed_50_designs.py**
   - Main seeding script
   - Creates 60 jewelry designs
   - Assigns unique images
   - Sets realistic pricing

2. **reset_and_seed.py**
   - Clears old demo data
   - Runs seed_50_designs.py
   - Provides progress feedback

### Database Changes:

```sql
-- Designs table populated with:
- seller_id (random from existing sellers)
- category (Necklace, Rings, Bangle, Earrings, Bracelet)
- purity (18K or 22K)
- weight (category-specific ranges)
- gold_rate_snapshot (6479)
- making_charge_snapshot (800-2500)
- gst (3% calculated)
- occasion_tag (Wedding, Festive, etc.)
- is_demo (true)

-- Design_media table populated with:
- design_id (linked to design)
- uri (high-quality image URL)
- media_type (image)
- shot_type (master and closeup)
- status (approved)
- is_demo (true)
```

### CSS Changes:

Updated `public/css/components-enhanced.css`:

```css
/* Desktop: 4 cards per row */
.design-grid {
  grid-template-columns: repeat(4, 1fr);
}

/* Tablet: 3 cards per row */
@media (max-width: 1400px) {
  .design-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Mobile: 2 cards per row */
@media (max-width: 1024px) {
  .design-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

---

## 📋 Step-by-Step Instructions

### Step 1: Backup (Optional but Recommended)
```bash
# Backup your current database
copy platform.sqlite platform.sqlite.backup
```

### Step 2: Run the Seed Script
```bash
# Option A: Reset and seed (clears old data)
python reset_and_seed.py

# Option B: Add to existing data
python seed_50_designs.py
```

### Step 3: Start the Server
```bash
python app.py
```

### Step 4: View Results
Open your browser:
```
http://localhost:3000
```

---

## ✅ Verification Checklist

After seeding, verify:

### Homepage:
- [ ] At least 40 jewelry cards visible
- [ ] 4 cards per row on desktop
- [ ] Each card has a unique image
- [ ] Product names show: "22K Gold [Category]"
- [ ] Category badges visible (gold background)
- [ ] Prices calculated correctly
- [ ] Occasion tags showing

### Responsive:
- [ ] Desktop (>1400px): 4 cards per row
- [ ] Tablet (1024-1400px): 3 cards per row
- [ ] Mobile (<1024px): 2 cards per row
- [ ] All images load properly
- [ ] No layout issues

### Image Quality:
- [ ] Images are clear and high-resolution
- [ ] No broken images
- [ ] Consistent aspect ratio
- [ ] Proper cropping
- [ ] Fast loading

---

## 🎯 Expected Result

### Before:
```
┌────┬────┬────┐
│ 1  │ 2  │ 3  │  ← Only 3 cards per row
├────┼────┼────┤
│ 4  │ 5  │ 6  │
└────┴────┴────┘
Limited designs
```

### After:
```
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │  ← 4 cards per row
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │
├────┼────┼────┼────┤
│ 9  │ 10 │ 11 │ 12 │
├────┼────┼────┼────┤
│ ... (15 rows total) │
└────┴────┴────┴────┘
60 unique designs
```

---

## 🐛 Troubleshooting

### Issue: "No sellers found"
**Solution:**
```bash
# Run the main seed script first
python -c "from src.database.seeds.seed_curated_data import seed_all; seed_all()"
```

### Issue: Images not loading
**Solution:**
- Check internet connection (images from Unsplash)
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors

### Issue: Still showing 3 cards per row
**Solution:**
- Clear browser cache
- Check screen width (need >1400px for 4 cards)
- Verify CSS file was updated

### Issue: Duplicate images
**Solution:**
- Each design should have unique image
- Check `jewelry-images.js` is loaded
- Verify design IDs are sequential

---

## 📊 Weight Ranges by Category

Realistic weight ranges used:

| Category  | Min Weight | Max Weight | Typical |
|-----------|------------|------------|---------|
| Necklace  | 15g        | 55g        | 30g     |
| Rings     | 3g         | 12g        | 6g      |
| Bangle    | 8g         | 30g        | 18g     |
| Earrings  | 4g         | 18g        | 10g     |
| Bracelet  | 6g         | 25g        | 15g     |

---

## 💰 Pricing Examples

Based on ₹6,479/gram for 22K gold:

| Weight | Gold Value | Making | GST (3%) | Total    |
|--------|------------|--------|----------|----------|
| 10g    | ₹64,790    | ₹1,500 | ₹1,989   | ₹68,279  |
| 25g    | ₹1,61,975  | ₹2,000 | ₹4,919   | ₹1,68,894|
| 50g    | ₹3,23,950  | ₹2,500 | ₹9,794   | ₹3,36,244|

---

## 🎉 Success Criteria

You'll know it worked when:

1. ✅ Homepage shows 60 jewelry cards
2. ✅ Desktop displays 4 cards per row
3. ✅ 15 rows of jewelry visible
4. ✅ Each card has unique image
5. ✅ Product names are descriptive
6. ✅ Prices are realistic
7. ✅ No broken images
8. ✅ Responsive on all devices

---

## 📚 Additional Resources

- **Image Source:** Unsplash (https://unsplash.com)
- **Gold Rate:** Based on real 22K Indian market rate
- **Design Inspiration:** Traditional and modern Indian jewelry

---

## 🔄 To Add More Designs Later

Edit `seed_50_designs.py` and change:
```python
# Change this number to create more designs per category
for i in range(12):  # Change 12 to 20 for 100 total designs
```

Then run:
```bash
python seed_50_designs.py
```

---

**Status:** Ready to use!
**Run:** `python reset_and_seed.py`
**View:** `http://localhost:3000`
