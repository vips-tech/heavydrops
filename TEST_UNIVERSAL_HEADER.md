# 🧪 Test Universal Header - Quick Guide

## ✅ What to Test

All pages should now have the **exact same header** as the homepage.

---

## 🚀 Quick Test Steps

### Step 1: Test Homepage
```
URL: http://localhost:5001/
```
**Check:**
- [ ] Gold rate ticker visible (₹6,479/g)
- [ ] Filter button present
- [ ] Hamburger menu on mobile
- [ ] HOME link highlighted in gold

### Step 2: Test About Page
```
URL: http://localhost:5001/about
```
**Check:**
- [ ] Same header as homepage
- [ ] Gold rate ticker visible
- [ ] Filter button present
- [ ] ABOUT link highlighted in gold

### Step 3: Test How It Works
```
URL: http://localhost:5001/how-it-works
```
**Check:**
- [ ] Same header as homepage
- [ ] Gold rate ticker visible
- [ ] Filter button present
- [ ] HOW IT WORKS link highlighted

### Step 4: Test Mobile View
1. Press **F12** (DevTools)
2. Press **Ctrl+Shift+M** (Mobile view)
3. Select **iPhone 12 Pro**

**Check on ANY page:**
- [ ] Hamburger menu (☰) visible
- [ ] Gold rate compact (₹6.5k)
- [ ] Filter button icon only
- [ ] Click hamburger → menu opens
- [ ] Menu items left-aligned
- [ ] Click outside → menu closes

---

## 📱 Visual Comparison

### Desktop Header (All Pages)
```
┌────────────────────────────────────────────────────────┐
│                                                         │
│  [LOGO]  HOME  HOW IT WORKS  ABOUT  [₹6,479/g] [FILT] │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Mobile Header (All Pages)
```
┌─────────────────────────────────┐
│                                 │
│ [LOGO]    [₹6.5k] [🔍] [☰]    │
│                                 │
└─────────────────────────────────┘
```

### Mobile Menu Open (All Pages)
```
┌─────────────────────────────────┐
│ [LOGO]    [₹6.5k] [🔍] [✕]    │
├─────────────────────────────────┤
│ HOME                            │
│ ─────────────────────────────── │
│ HOW IT WORKS                    │
│ ─────────────────────────────── │
│ ABOUT                           │
├─────────────────────────────────┤
│ [Dark overlay]                  │
└─────────────────────────────────┘
```

---

## ✅ Success Indicators

### Header Elements Present:
- ✅ Logo (Heavy Drops)
- ✅ Navigation links (HOME, HOW IT WORKS, ABOUT)
- ✅ Gold rate ticker (₹6,479/g or ₹6.5k on mobile)
- ✅ Filter button (with icon)
- ✅ Hamburger menu (mobile only)

### Functionality Working:
- ✅ Active page highlighted in gold
- ✅ Gold rate loads from API
- ✅ Filter button opens sidebar
- ✅ Hamburger menu opens/closes
- ✅ Click outside closes menu
- ✅ Click link closes menu and navigates

---

## 🎯 Test These Pages

Quick test on 5 key pages:

1. **Homepage**: http://localhost:5001/
2. **About**: http://localhost:5001/about
3. **How It Works**: http://localhost:5001/how-it-works
4. **Terms**: http://localhost:5001/terms
5. **Philosophy**: http://localhost:5001/philosophy

**All should have identical headers!**

---

## 🔍 What to Look For

### ✅ GOOD (Correct)
```
Every page has:
- Same logo position
- Same navigation links
- Gold rate ticker in same spot
- Filter button in same spot
- Hamburger menu (mobile)
- Active link highlighted
```

### ❌ BAD (Incorrect)
```
If you see:
- Different header layouts
- Missing gold rate ticker
- No filter button
- No hamburger menu on mobile
- Active link not highlighted
→ Report the page name
```

---

## 🐛 Troubleshooting

### Gold Rate Not Showing?
1. Check browser console (F12)
2. Look for API errors
3. Verify `/api/health/config` is accessible

### Hamburger Menu Not Working?
1. Check if `mobile-menu.js` is loaded
2. Check if `universal-header.js` is loaded
3. Look for JavaScript errors in console

### Filter Button Not Working?
1. Check if `toggleFilters()` function exists
2. Verify filter sidebar HTML is present
3. Check for JavaScript errors

### Active Link Not Highlighted?
1. Verify URL matches link href
2. Check if `setActiveNavLink()` is called
3. Look for CSS class 'active' on link

---

## 📊 Quick Checklist

Test each page and mark:

| Page | Header | Gold Rate | Filter | Hamburger | Active Link |
|------|--------|-----------|--------|-----------|-------------|
| / | ☐ | ☐ | ☐ | ☐ | ☐ |
| /about | ☐ | ☐ | ☐ | ☐ | ☐ |
| /how-it-works | ☐ | ☐ | ☐ | ☐ | ☐ |
| /problem | ☐ | ☐ | ☐ | ☐ | ☐ |
| /philosophy | ☐ | ☐ | ☐ | ☐ | ☐ |
| /terms | ☐ | ☐ | ☐ | ☐ | ☐ |
| /privacy-policy | ☐ | ☐ | ☐ | ☐ | ☐ |
| /security | ☐ | ☐ | ☐ | ☐ | ☐ |
| /collection | ☐ | ☐ | ☐ | ☐ | ☐ |
| /login | ☐ | ☐ | ☐ | ☐ | ☐ |

---

## 🎨 Expected Behavior

### Desktop (> 768px)
1. Full navigation visible
2. Gold rate shows "₹6,479/g 22K"
3. Filter button shows "FILTERS" text
4. No hamburger menu
5. Active link has gold background

### Tablet (768px)
1. Navigation becomes hamburger menu
2. Gold rate shows "₹6,479/g"
3. Filter button shows icon only
4. Hamburger menu appears
5. Active link highlighted in menu

### Mobile (< 768px)
1. Navigation is hamburger menu
2. Gold rate shows "₹6.5k"
3. Filter button icon only
4. Hamburger menu visible
5. Menu slides down when clicked

---

## 💻 Browser Console Test

Open console (F12) and run:

```javascript
// Check if functions exist
console.log(typeof toggleMobileMenu);  // Should be "function"
console.log(typeof toggleFilters);     // Should be "function"
console.log(typeof initGoldRateTicker); // Should be "function"

// Check if elements exist
console.log(document.getElementById('mainNav'));      // Should be <nav>
console.log(document.getElementById('navCenter'));    // Should be <div>
console.log(document.getElementById('filterSidebar')); // Should be <div>
```

All should return valid results!

---

## ✅ Final Verification

If all pages have:
- ✅ Same header layout
- ✅ Gold rate ticker
- ✅ Filter button
- ✅ Working hamburger menu
- ✅ Active page highlighting

**Then the universal header is working perfectly!**

---

**Test URL**: http://localhost:5001
**All 22 pages should be identical**

Date: May 9, 2026
