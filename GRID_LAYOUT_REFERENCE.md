# Grid Layout Reference - 4 Cards Per Row

## 🎯 New Grid Layout

### Desktop View (>1400px) - 4 Cards Per Row
```
┌─────────────────────────────────────────────────────────────────┐
│                         HOMEPAGE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Necklace │  │ Necklace │  │ Necklace │  │ Necklace │  Row 1│
│  │ 22K Gold │  │ 22K Gold │  │ 22K Gold │  │ 18K Gold │      │
│  │ ₹1,68,894│  │ ₹2,15,432│  │ ₹1,95,678│  │ ₹1,45,890│      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Ring    │  │  Ring    │  │  Ring    │  │  Ring    │  Row 2│
│  │ 22K Gold │  │ 22K Gold │  │ 18K Gold │  │ 22K Gold │      │
│  │ ₹45,678  │  │ ₹52,340  │  │ ₹38,900  │  │ ₹48,765  │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Bangle  │  │  Bangle  │  │  Bangle  │  │  Bangle  │  Row 3│
│  │ 22K Gold │  │ 22K Gold │  │ 22K Gold │  │ 18K Gold │      │
│  │ ₹1,25,890│  │ ₹1,45,678│  │ ₹1,35,432│  │ ₹98,765  │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                 │
│  ... (continues for 15 rows total)                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tablet View (1024-1400px) - 3 Cards Per Row
```
┌──────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Necklace │  │ Necklace │  │ Necklace │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Ring    │  │  Ring    │  │  Ring    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└──────────────────────────────────────────────┘
```

### Mobile View (<1024px) - 2 Cards Per Row
```
┌────────────────────────────┐
│  ┌──────┐    ┌──────┐     │
│  │Neckl.│    │Neckl.│     │
│  └──────┘    └──────┘     │
│                            │
│  ┌──────┐    ┌──────┐     │
│  │ Ring │    │ Ring │     │
│  └──────┘    └──────┘     │
└────────────────────────────┘
```

---

## 📊 Design Distribution

### 60 Total Designs:

```
Category      | Count | Rows (4 per row)
--------------|-------|------------------
Necklaces     |  12   |  3 rows
Rings         |  12   |  3 rows
Bangles       |  12   |  3 rows
Earrings      |  12   |  3 rows
Bracelets     |  12   |  3 rows
--------------|-------|------------------
TOTAL         |  60   |  15 rows
```

---

## 🎨 Card Layout

Each card displays:

```
┌─────────────────────────┐
│ [Wedding]               │ ← Occasion tag
│                         │
│    [Gold Necklace]      │ ← High-quality image
│                         │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │    NECKLACE         │ │ ← Category badge (gold bg)
│ └─────────────────────┘ │
│ 22K Gold Necklace       │ ← Descriptive name
│                         │
│ ⚖ 25g  👤 Seller  📍City│ ← Specs
│                         │
│ Gold Value: ₹1,61,975   │ ← Price breakdown
│ Making + Tax: ₹7,000    │
│ ─────────────────────   │
│ Total: ₹1,68,975        │ ← Total price
│                         │
│ [View Details]          │ ← CTA button
└─────────────────────────┘
```

---

## 🖼️ Image Quality

All images are:
- **Resolution:** 800x800px
- **Quality:** 90 (Unsplash)
- **Format:** JPEG optimized
- **Aspect Ratio:** 4:5 (portrait)
- **Source:** Professional jewelry photography

### Image URLs Format:
```
https://images.unsplash.com/photo-[ID]?w=800&h=800&fit=crop&q=90
```

---

## 📐 Spacing & Sizing

### Desktop (4 cards):
- **Card Width:** ~25% of container
- **Gap:** 2rem (32px)
- **Container Max:** 1400px
- **Card Height:** Auto (maintains aspect ratio)

### Tablet (3 cards):
- **Card Width:** ~33% of container
- **Gap:** 1.5rem (24px)

### Mobile (2 cards):
- **Card Width:** ~50% of container
- **Gap:** 1rem (16px)

---

## 🎯 Visual Hierarchy

```
1. Image (Largest, most prominent)
   ↓
2. Category Badge (Gold background)
   ↓
3. Product Name (22K Gold Necklace)
   ↓
4. Specifications (Weight, Seller, Location)
   ↓
5. Price Breakdown (Transparent pricing)
   ↓
6. CTA Button (View Details)
```

---

## 🌈 Color Scheme

- **Category Badge:** Gold background (rgba(212, 175, 55, 0.1))
- **Tag Pill:** Dark background (rgba(10, 10, 10, 0.9))
- **Price Text:** Dark gray (#2A2A2A)
- **Total Price:** Bold black (#0A0A0A)
- **Button:** Black with hover effect

---

## 📱 Responsive Breakpoints

```css
/* Desktop: 4 cards */
@media (min-width: 1400px) {
  grid-template-columns: repeat(4, 1fr);
}

/* Large Tablet: 3 cards */
@media (max-width: 1400px) {
  grid-template-columns: repeat(3, 1fr);
}

/* Tablet/Mobile: 2 cards */
@media (max-width: 1024px) {
  grid-template-columns: repeat(2, 1fr);
}

/* Small Mobile: 2 cards (compact) */
@media (max-width: 640px) {
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
```

---

## ✅ Quality Checklist

Each card should have:
- [x] Unique high-quality image
- [x] Descriptive product name
- [x] Category badge with gold background
- [x] Occasion tag (Wedding, Festive, etc.)
- [x] Weight, seller, and location info
- [x] Transparent price breakdown
- [x] Live gold rate calculation
- [x] Hover effects
- [x] Like button
- [x] View Details button

---

## 🎉 Final Result

**60 jewelry designs** displayed as:
- **Desktop:** 15 rows × 4 cards = 60 cards
- **Tablet:** 20 rows × 3 cards = 60 cards
- **Mobile:** 30 rows × 2 cards = 60 cards

All with:
✅ Unique images
✅ Proper names
✅ Realistic pricing
✅ Professional layout
✅ Responsive design

---

**Ready to see it?**
Run: `python reset_and_seed.py`
View: `http://localhost:3000`
