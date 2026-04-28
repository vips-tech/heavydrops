# Homepage Testing Guide

## Quick Test Checklist

### 1. Visual Inspection
Open `http://localhost:3000` in your browser and verify:

#### Header (Top of Page)
- [ ] Header is full-width (not floating)
- [ ] Header is fixed to the top (no gap)
- [ ] Logo is visible on the left
- [ ] Navigation links (HOME, HOW IT WORKS, ABOUT) are centered
- [ ] Gold rate badge shows: **₹6,479/g LIVE 22K**
- [ ] Filter button is visible on the right
- [ ] Header has clean border at bottom

#### Gold Rate Display
- [ ] Gold rate is visible in header
- [ ] Shows format: `₹6,479/g LIVE 22K`
- [ ] Has gold gradient background
- [ ] Icon is visible (sparkle/diamond icon)
- [ ] Updates every 30 seconds (watch for animation)

#### Jewelry Cards
- [ ] Each card shows category badge (e.g., "NECKLACE")
- [ ] Badge has gold background highlight
- [ ] Card title shows: "22K Gold [Category]" (e.g., "22K Gold Necklace")
- [ ] Tag pill shows category + occasion (e.g., "Necklace • Wedding")
- [ ] Images are centered and properly sized
- [ ] If image fails, placeholder shows category name
- [ ] Price breakdown is clear and readable

### 2. Responsive Testing

#### Desktop (>768px)
- [ ] Header shows full gold rate: "₹6,479/g LIVE 22K"
- [ ] Filter button shows text: "FILTERS"
- [ ] All navigation links visible
- [ ] Cards display in grid (3-4 columns)

#### Mobile (<768px)
- [ ] Header height reduces to 70px
- [ ] Gold rate shows: "₹6,479/g" (LIVE 22K hidden)
- [ ] Filter button shows icon only (text hidden)
- [ ] Logo size optimized (28px)
- [ ] Cards display in 2 columns
- [ ] Touch targets are adequate

### 3. Functionality Testing

#### Scroll Behavior
- [ ] Header stays fixed at top when scrolling
- [ ] Header adds shadow on scroll (after 50px)
- [ ] Smooth scroll animation
- [ ] No jumping or flickering

#### Gold Rate Updates
- [ ] Rate updates every 30 seconds
- [ ] Small animation on update
- [ ] Rate fluctuates slightly (±25 rupees)
- [ ] No console errors

#### Card Interactions
- [ ] Hover effect on cards (lift up)
- [ ] Like button works
- [ ] Click navigates to detail page
- [ ] Images load properly
- [ ] Fallback works if image fails

### 4. Browser Testing

Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile browsers (iOS/Android)

### 5. Console Check

Open browser DevTools (F12) and check:
- [ ] No JavaScript errors
- [ ] No CSS warnings
- [ ] Images loading correctly
- [ ] API calls successful
- [ ] Gold rate updates logging

## Expected Behavior

### Header Appearance
```
┌────────────────────────────────────────────────────────┐
│ 🏷️ HEAVY DROPS  HOME  HOW IT WORKS  ABOUT  [₹6,479/g LIVE 22K] [FILTERS] │
└────────────────────────────────────────────────────────┘
```

### Jewelry Card Appearance
```
┌─────────────────────┐
│ [Necklace • Wedding]│ ← Tag pill (top-left)
│                     │
│   [Gold Necklace]   │ ← Image centered
│                     │
├─────────────────────┤
│ ┌─────────────────┐ │
│ │  NECKLACE       │ │ ← Category badge (gold bg)
│ └─────────────────┘ │
│ 22K Gold Necklace   │ ← Descriptive title
│ 25g | Seller | City │
│                     │
│ Gold Value: ₹1,61,975│
│ Making + Tax: ₹5,000│
│ Total: ₹1,66,975    │
│                     │
│ [View Details]      │
└─────────────────────┘
```

## Common Issues & Fixes

### Issue: Gold rate not showing
**Fix:** Check if `enhanced-features.js` is loaded
```javascript
// In browser console:
console.log(window.heavyDropsEnhanced);
// Should show object, not undefined
```

### Issue: Header still floating
**Fix:** Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)

### Issue: Images not loading
**Fix:** Check if `jewelry-images.js` is loaded
```javascript
// In browser console:
console.log(window.JewelryImages);
// Should show object with getUniqueImage function
```

### Issue: Category names not showing
**Fix:** Check browser console for JavaScript errors

## Performance Metrics

Expected load times:
- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Time to Interactive:** < 3.5s
- **Cumulative Layout Shift:** < 0.1

## Accessibility Check

- [ ] Header has proper ARIA labels
- [ ] Navigation is keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA
- [ ] Images have alt text
- [ ] Buttons have aria-labels

## Final Verification

Run through this scenario:
1. Open homepage
2. Verify header is standard (not floating)
3. Check gold rate is visible and updating
4. Scroll down and verify header behavior
5. Check jewelry cards have proper names
6. Verify category badges are visible
7. Test on mobile device or responsive mode
8. Click a card to verify navigation works

---

**All checks passed?** ✅ Homepage improvements are complete!

**Issues found?** Check the console logs and refer to the fixes above.
