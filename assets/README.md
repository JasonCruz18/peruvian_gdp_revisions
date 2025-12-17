# Project Assets

This directory contains visual assets for the Peru GDP Real-Time Dataset project.

---

## Logo

### Current Status
🎨 **Logo not yet created** - Using placeholder/text-only branding

### Where Logos Are Used

1. **Dashboard** (`dashboard/app.py`)
   - Location: `dashboard/assets/logo.png`
   - Recommended size: 200-400px width
   - Format: PNG with transparent background

2. **README.md** (Optional)
   - Can add banner at top of README
   - Recommended size: 1200x400px
   - Format: PNG or SVG

3. **Documentation** (Optional)
   - Can be used in PDF exports
   - Technical supplement header

---

## Creating a Logo

### Design Guidelines

**Brand Identity:**
- **Colors:** Professional blues/grays (or use dashboard theme colors)
- **Style:** Clean, modern, academic
- **Elements to consider:**
  - Peruvian flag colors (red/white) - optional
  - GDP growth chart/line graph
  - Real-time data visualization element
  - CIUP/Universidad del Pacífico branding (if permitted)

**Text to include:**
- "Peru GDP RTD" or
- "Peru GDP Real-Time Dataset" or
- "CIUP - Peru GDP Data"

### Logo Specifications

#### Dashboard Logo
- **File:** `dashboard/assets/logo.png`
- **Size:** 200-400px width, any height (maintains aspect ratio)
- **Format:** PNG with transparent background
- **DPI:** 72-150 DPI (web resolution)
- **Color mode:** RGB

#### README Banner (Optional)
- **File:** `assets/banner.png`
- **Size:** 1200x400px (3:1 ratio)
- **Format:** PNG or SVG
- **DPI:** 72-150 DPI
- **Content:** Logo + tagline

#### Favicon (Optional)
- **File:** `assets/favicon.ico`
- **Size:** 32x32px, 64x64px (multi-size ICO)
- **Use:** Browser tab icon for dashboard

---

## Design Tools

### Free Tools (No Design Skills Required)

1. **Canva** (https://www.canva.com/)
   - Free templates for logos
   - Easy drag-and-drop interface
   - Export as PNG with transparent background

2. **LogoMakr** (https://logomakr.com/)
   - Simple online logo maker
   - Free for personal/academic use

3. **Figma** (https://www.figma.com/)
   - Professional design tool
   - Free for individual use
   - Great for creating consistent branding

### Professional Tools

1. **Adobe Illustrator** (vector graphics)
2. **Inkscape** (free, open-source vector graphics)
3. **GIMP** (free, open-source raster graphics)

---

## Adding Your Logo

### Step 1: Create the Logo

1. Design your logo using one of the tools above
2. Export as **PNG with transparent background**
3. Recommended dimensions: 400x400px or 600x200px

### Step 2: Add to Dashboard

1. Save your logo as: `dashboard/assets/logo.png`
2. Open `dashboard/config.py`
3. Set:
   ```python
   USE_LOGO = True
   LOGO_WIDTH = 200  # Adjust as needed (100-400)
   ```
4. Run the dashboard: `streamlit run dashboard/app.py`
5. Your logo will appear at the top!

### Step 3: Add Banner to README (Optional)

1. Create a banner (1200x400px)
2. Save as: `assets/banner.png`
3. Edit `README.md` and add at the top:
   ```markdown
   ![Peru GDP RTD](assets/banner.png)

   # Peru GDP Real-Time Dataset Construction Pipeline
   ```

---

## Logo Ideas & Inspiration

### Concept 1: Minimalist Data Visualization
```
[Simple line chart going upward] + "Peru GDP RTD"
Colors: Blue gradient (#1f77b4 → #2ca02c)
```

### Concept 2: Flag-Inspired
```
Red/white elements + GDP chart
Text: "PERU GDP" in bold, "Real-Time Dataset" subtitle
```

### Concept 3: Academic/Institutional
```
Simple text logo with CIUP branding
Universidad del Pacífico colors
Professional serif font
```

### Concept 4: Modern Tech
```
Abstract data nodes/network
"RTD" large, "Peru GDP" smaller
Tech-inspired colors (blue/purple)
```

---

## Example Prompts for AI Logo Generators

If using AI tools (Canva AI, DALL-E, Midjourney, etc.):

**Prompt 1:**
```
Create a professional logo for an economic data analysis project called "Peru GDP RTD".
Include a simple line chart or data visualization element. Use blue and green colors.
Modern, clean design suitable for academic research. Transparent background.
```

**Prompt 2:**
```
Design a minimalist logo combining the Peruvian flag colors (red and white) with a
subtle GDP growth chart. Text: "Peru GDP Real-Time Dataset". Professional, academic style.
```

**Prompt 3:**
```
Logo for economic research dashboard. Abstract representation of real-time data flow.
Modern typography with "RTD" prominently displayed. Blue gradient colors. Square format.
```

---

## Current Placeholder

Until you create a logo, the dashboard uses:
- Text-only title: "Peru GDP Real-Time Dataset"
- Emoji icon: 📊 (optional, can be added to title)
- Theme-based colors from `dashboard/config.py`

**To add an emoji placeholder:**
Edit `dashboard/config.py`:
```python
PROJECT_NAME = "📊 Peru GDP Real-Time Dataset"
```

---

## Branding Checklist

Once you have a logo:

- [ ] Add to `dashboard/assets/logo.png`
- [ ] Enable in `dashboard/config.py` (USE_LOGO = True)
- [ ] Test dashboard appearance
- [ ] Optional: Add banner to README.md
- [ ] Optional: Create favicon
- [ ] Optional: Add to documentation PDFs
- [ ] Optional: Create social media graphics (1200x630px for OpenGraph)
- [ ] Ensure logo looks good on both light and dark backgrounds

---

## License Considerations

**Important:** Only use images you have the rights to use.

- **Your own design:** You own the copyright ✅
- **Free tools (Canva, LogoMakr):** Check their terms (usually OK for academic use) ✅
- **Purchased stock images:** Check license ✅
- **Copyrighted logos (e.g., CIUP logo):** Get permission first ⚠️
- **AI-generated:** Check the AI tool's terms (usually you own the output) ✅

If using institutional branding (CIUP, Universidad del Pacífico), get written permission first.

---

## Resources

- **Canva Logo Templates:** https://www.canva.com/logos/templates/
- **Free Icon Resources:**
  - https://www.flaticon.com/
  - https://fonts.google.com/icons (Material Icons)
  - https://heroicons.com/
- **Color Palette Generator:** https://coolors.co/
- **Logo Design Best Practices:** https://99designs.com/blog/tips/logo-design-tips/

---

## Questions?

If you need help with logo creation or have questions about branding:
- Open a GitHub issue
- Contact: jj.cruza@up.edu.pe

---

**Note:** The project is fully functional without a logo. This is purely cosmetic and can be added at any time.

**Last Updated:** December 16, 2025
