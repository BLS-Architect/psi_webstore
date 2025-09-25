# PSi Brand Colors & UI Styling Guide
## Updated with Actual Brand Colors

---

## OFFICIAL PSi COLOR PALETTE

### Primary Colors (From Website)
```css
:root {
    /* PSi Brand Colors */
    --psi-red: #F14C32;        /* Primary brand orange/red */
    --psi-black: #231F20;      /* Brand black */
    
    /* UI Application Colors */
    --primary: #F14C32;        /* Buttons, links, accents */
    --text-dark: #231F20;      /* Main text */
    --text-light: #666666;     /* Secondary text */
    
    /* Functional Colors */
    --success: #28A745;        /* Profit indicators, positive margins */
    --warning: #FFC107;        /* Minimum order warnings, case qty hints */
    --error: #DC3545;          /* Out of stock, errors */
    --info: #17A2B8;           /* Information, tips */
    
    /* Backgrounds */
    --bg-white: #FFFFFF;       /* Cards, panels */
    --bg-light: #F8F9FA;       /* Page background */
    --bg-gray: #E9ECEF;        /* Alternate rows, disabled */
    
    /* Borders */
    --border-light: #DEE2E6;   /* Subtle borders */
    --border-medium: #CED4DA;  /* Form inputs */
    --border-dark: #231F20;    /* Strong dividers */
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(35, 31, 32, 0.1);
    --shadow-md: 0 4px 6px rgba(35, 31, 32, 0.1);
    --shadow-lg: 0 10px 15px rgba(35, 31, 32, 0.1);
    --shadow-hover: 0 6px 12px rgba(241, 76, 50, 0.15);
}
```

---

## CSS IMPLEMENTATION

### Header Styling (Matching Website)
```css
.header {
    background: #FFFFFF;
    border-bottom: 3px solid #F14C32;
    padding: 1rem 0;
}

.logo {
    color: #231F20;
    font-weight: bold;
    font-size: 1.5rem;
}

.logo .highlight {
    color: #F14C32;
}

/* Tagline styling */
.tagline {
    color: #F14C32;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.mission {
    color: #231F20;
    line-height: 1.6;
}
```

### Button Styles
```css
/* Primary Button - PSi Red */
.btn-primary {
    background: #F14C32;
    color: #FFFFFF;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}

.btn-primary:hover {
    background: #D43A22;  /* Darker shade */
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(241, 76, 50, 0.3);
}

.btn-primary:disabled {
    background: #CED4DA;
    cursor: not-allowed;
}

/* Secondary Button */
.btn-secondary {
    background: #FFFFFF;
    color: #231F20;
    border: 2px solid #231F20;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
}

.btn-secondary:hover {
    background: #231F20;
    color: #FFFFFF;
}
```

### Product Card Styling
```css
.product-card {
    background: #FFFFFF;
    border: 1px solid #DEE2E6;
    border-radius: 8px;
    padding: 1rem;
    transition: all 0.3s ease;
}

.product-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(241, 76, 50, 0.15);
    border-color: #F14C32;
}

.product-card.featured {
    border: 2px solid #F14C32;
}

.product-card.featured::before {
    content: "FEATURED";
    position: absolute;
    top: -10px;
    right: 10px;
    background: #F14C32;
    color: #FFFFFF;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: bold;
}

.product-title {
    color: #231F20;
    font-weight: bold;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.product-price {
    color: #F14C32;
    font-size: 1.3rem;
    font-weight: bold;
    margin: 0.5rem 0;
}

.product-msrp {
    color: #666666;
    font-size: 0.9rem;
}

.product-margin {
    display: inline-block;
    background: #28A745;
    color: #FFFFFF;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}
```

### Cart Panel Styling
```css
.cart-panel {
    background: #FFFFFF;
    border: 2px solid #F14C32;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px rgba(35, 31, 32, 0.1);
}

.cart-header {
    border-bottom: 2px solid #F14C32;
    padding-bottom: 1rem;
    margin-bottom: 1rem;
}

.cart-title {
    color: #231F20;
    font-size: 1.3rem;
    font-weight: bold;
}

.profit-display {
    background: linear-gradient(135deg, #F14C32, #FF6B55);
    color: #FFFFFF;
    padding: 1rem;
    border-radius: 6px;
    text-align: center;
    margin: 1rem 0;
}

.profit-amount {
    font-size: 2rem;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.minimum-warning {
    background: #FFF3E0;
    border-left: 4px solid #FFC107;
    color: #856404;
    padding: 0.75rem;
    margin: 1rem 0;
}
```

### Form Elements
```css
input[type="text"],
input[type="number"],
select {
    border: 1px solid #CED4DA;
    padding: 0.5rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}

input:focus,
select:focus {
    border-color: #F14C32;
    outline: none;
    box-shadow: 0 0 0 3px rgba(241, 76, 50, 0.1);
}

/* Quantity Controls */
.qty-controls {
    display: flex;
    align-items: center;
    border: 1px solid #CED4DA;
    border-radius: 4px;
    overflow: hidden;
}

.qty-btn {
    background: #F8F9FA;
    border: none;
    padding: 0.5rem 0.75rem;
    cursor: pointer;
    transition: background 0.2s;
}

.qty-btn:hover {
    background: #F14C32;
    color: #FFFFFF;
}

.qty-input {
    border: none;
    text-align: center;
    width: 50px;
    padding: 0.5rem;
}
```

---

## TYPOGRAPHY

### Font Stack
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                 'Helvetica Neue', Arial, sans-serif;
    color: #231F20;
    line-height: 1.6;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #231F20;
    font-weight: 600;
    line-height: 1.2;
}

h1 { font-size: 2rem; }
h2 { font-size: 1.5rem; }
h3 { font-size: 1.25rem; }

/* Links */
a {
    color: #F14C32;
    text-decoration: none;
    transition: color 0.3s ease;
}

a:hover {
    color: #D43A22;
    text-decoration: underline;
}
```

---

## RESPONSIVE BREAKPOINTS

```css
/* Mobile First Approach */
/* Small devices (phones, 576px and down) */
@media (max-width: 576px) {
    .products-grid {
        grid-template-columns: 1fr;
    }
}

/* Medium devices (tablets, 768px and up) */
@media (min-width: 768px) {
    .products-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Large devices (desktops, 992px and up) */
@media (min-width: 992px) {
    .products-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Extra large devices (large desktops, 1200px and up) */
@media (min-width: 1200px) {
    .products-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}
```

---

## LOADING & ANIMATION STATES

```css
/* Loading Spinner */
.spinner {
    border: 3px solid #F8F9FA;
    border-top: 3px solid #F14C32;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Pulse Animation for Profit Updates */
@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(241, 76, 50, 0.7);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(241, 76, 50, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(241, 76, 50, 0);
    }
}

.profit-update {
    animation: pulse 2s infinite;
}
```

---

## IMPLEMENTATION NOTES FOR IDE AGENT

1. **Replace all blue colors** (#003F87) with PSi red (#F14C32)
2. **Update text colors** to use brand black (#231F20)
3. **Keep functional colors** (success green for profit, warning yellow for minimums)
4. **Maintain clean, professional B2B aesthetic** matching the website
5. **Use white backgrounds** with subtle gray accents
6. **Apply PSi red strategically** for CTAs and important UI elements

---

## HTML STRUCTURE WITH BRANDING

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PSi Retail Services - Interactive Catalog</title>
    <style>
        /* Include all CSS variables and styles from above */
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                PSi <span class="highlight">RETAIL SERVICES</span>
            </div>
            <p class="tagline">Inspiring Play. Powering Growth.</p>
        </div>
    </header>
    
    <!-- Rest of catalog implementation -->
</body>
</html>
```

---

This color scheme matches your actual PSi branding and maintains the professional B2B aesthetic while incorporating the vibrant red/orange accent color effectively.