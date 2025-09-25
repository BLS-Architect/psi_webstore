# PSi Interactive Catalog - URL Bridge Architecture
## Design Documentation & Implementation Guide v2.0
### January 2025

---

## 1. EXECUTIVE SUMMARY

### 1.1 Overview
A revolutionary approach to B2B catalog distribution that encodes the entire product catalog into a URL hash, eliminating attachment friction while maintaining offline capability and personalization.

### 1.2 Core Innovation
Instead of attaching HTML files to emails, we compress and encode the catalog data into the URL itself. Customers click a link, and the catalog appears instantly - no downloads, no attachments, no confusion.

### 1.3 Key Benefits
- **Zero friction**: Click link → See catalog (no download/save/open dance)
- **Works everywhere**: Mobile, desktop, all browsers
- **No backend required**: One static HTML file on CDN
- **Personalized**: Each customer gets unique pricing/products in their URL
- **Offline capable**: Caches locally after first visit
- **Analytics ready**: Track opens, products viewed, orders

### 1.4 Technical Achievement
- 150 products compress to ~35KB URL (works in all modern browsers)
- 50 products compress to ~12KB URL (works in ALL browsers including IE)
- Load time: <100ms (pure client-side)
- Compression ratio: 85-90% size reduction

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Salesforce    │────▶│     Email       │────▶│    Browser      │
│   Campaign      │     │   with Link     │     │  Loads Catalog  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
   Generate URL            psi.com/catalog         Decode & Display
   with Catalog              #compressed              Products
     Data                       data                     
```

### 2.2 Component Architecture

```javascript
// Component Structure
system = {
  emailGeneration: {
    platform: "Salesforce",
    process: "Merge fields → JSON → Compress → URL",
    output: "Personalized email with catalog link"
  },
  
  staticHTML: {
    location: "CDN (CloudFront/Cloudflare)",
    file: "catalog.html",
    size: "~50KB including all JS libraries",
    dependencies: "None (self-contained)"
  },
  
  clientSide: {
    decode: "URL hash → Decompress → JSON",
    display: "Dynamic DOM generation",
    storage: "localStorage for offline",
    export: "CSV/Email order submission"
  }
}
```

### 2.3 Data Flow

1. **Salesforce Campaign Execution**
   ```
   Customer Data → Product Selection → JSON Generation → Compression → URL Creation
   ```

2. **Email Delivery**
   ```
   HTML Email Template → Merge Fields → Catalog URL → Send
   ```

3. **Customer Experience**
   ```
   Open Email → Click Link → Browser Opens → Catalog Appears → Browse/Order → Export
   ```

### 2.4 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Email Platform | Salesforce Marketing Cloud | Campaign management |
| Compression | LZ-String | 85-90% size reduction |
| Encoding | Base64 URL-safe | Browser compatibility |
| Frontend | Vanilla JavaScript | Zero dependencies |
| Hosting | Static CDN | Global distribution |
| Storage | localStorage | Offline capability |

---

## 3. DATA ARCHITECTURE

### 3.1 URL Structure

```
https://psi.com/catalog#eyJjb21wYW55Ijp7Im5hbWUiOiJQU2kiLCJtaW5pbXVtT3Jk...
│                      │└──────────────────────────────────────────────────┘
│                      │                    Compressed Catalog Data
│                      └─ Hash delimiter (not sent to server)
└─ Static HTML page on CDN
```

### 3.2 Catalog Data Schema

```javascript
{
  // Metadata
  "version": "2.0",
  "generated": "2025-01-22T10:30:00Z",
  "expires": "2025-02-28T23:59:59Z",
  
  // Company Settings
  "company": {
    "name": "PSi",
    "minimumOrder": 850,
    "currency": "USD"
  },
  
  // Customer Personalization
  "customer": {
    "id": "CUS-12345",
    "name": "ABC Toys",
    "tier": "gold",
    "discount": 0.05,
    "creditLimit": 5000,
    "accountManager": {
      "name": "John Smith",
      "email": "jsmith@psi.com",
      "phone": "555-0100"
    }
  },
  
  // Product Catalog
  "products": [
    {
      "id": "IBCCOU1",
      "sku": "IBCCOU1",
      "title": "Coup",
      "price": 9.00,      // Customer-specific price
      "msrp": 16.99,
      "margin": 47.0,
      "category": "Strategy Games",
      "publisher": "Indie Boards & Cards",
      "minQty": 1,
      "caseQty": 6,
      "inStock": true,
      "featured": true
    }
    // ... more products
  ]
}
```

### 3.3 Compression Strategy

```javascript
// Compression Pipeline
function createCatalogURL(customerData, products) {
  // 1. Build catalog object
  const catalog = {
    version: CONFIG.VERSION,
    customer: customerData,
    products: products,
    expires: getExpirationDate()
  };
  
  // 2. Convert to JSON (minified)
  const json = JSON.stringify(catalog);
  // Size: ~170KB for 150 products
  
  // 3. Compress with LZ-String
  const compressed = LZString.compressToEncodedURIComponent(json);
  // Size: ~35KB for 150 products (80% reduction)
  
  // 4. Create final URL
  const url = `${CONFIG.BASE_URL}#${compressed}`;
  // Total URL length: ~35,000 characters
  
  return url;
}
```

### 3.4 Size Optimization Tiers

| Products | Uncompressed | Compressed | URL Length | Browser Support |
|----------|-------------|------------|------------|-----------------|
| 10 | 12KB | 2.5KB | 2,500 chars | All browsers |
| 50 | 60KB | 12KB | 12,000 chars | All modern browsers |
| 150 | 170KB | 35KB | 35,000 chars | Chrome, Firefox, Safari |
| 500 | 550KB | 110KB | 110,000 chars | Chrome only |

---

## 4. IMPLEMENTATION GUIDE

### 4.1 Phase 1: Static HTML Page (2 days)

#### 4.1.1 Create catalog.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PSi Catalog</title>
    <script src="https://cdn.jsdelivr.net/npm/lz-string@1.4.4/libs/lz-string.min.js"></script>
</head>
<body>
    <div id="app">Loading catalog...</div>
    
    <script>
    // Core functionality
    class CatalogApp {
        constructor() {
            this.catalog = null;
            this.cart = [];
            this.init();
        }
        
        async init() {
            // 1. Try to load from URL
            const urlData = this.loadFromURL();
            if (urlData) {
                this.catalog = urlData;
                this.saveToStorage(urlData);
            } 
            // 2. Fallback to localStorage
            else {
                this.catalog = this.loadFromStorage();
            }
            
            if (this.catalog) {
                this.render();
            } else {
                this.showError('No catalog data found');
            }
        }
        
        loadFromURL() {
            const hash = window.location.hash;
            if (!hash || !hash.startsWith('#')) return null;
            
            try {
                const compressed = hash.substring(1);
                const json = LZString.decompressFromEncodedURIComponent(compressed);
                return JSON.parse(json);
            } catch(e) {
                console.error('Failed to load from URL:', e);
                return null;
            }
        }
        
        saveToStorage(data) {
            try {
                localStorage.setItem('psi_catalog', JSON.stringify(data));
                localStorage.setItem('psi_catalog_date', new Date().toISOString());
            } catch(e) {
                console.warn('Could not save to localStorage:', e);
            }
        }
        
        loadFromStorage() {
            try {
                const stored = localStorage.getItem('psi_catalog');
                return stored ? JSON.parse(stored) : null;
            } catch(e) {
                return null;
            }
        }
        
        render() {
            // Implement catalog UI
            this.renderHeader();
            this.renderProducts();
            this.renderCart();
        }
    }
    
    // Initialize app
    new CatalogApp();
    </script>
</body>
</html>
```

#### 4.1.2 Deploy to CDN

```bash
# Upload to S3 + CloudFront
aws s3 cp catalog.html s3://psi-catalog/catalog.html \
  --cache-control "public, max-age=86400" \
  --content-type "text/html"

# Invalidate CDN cache
aws cloudfront create-invalidation \
  --distribution-id E1234567890 \
  --paths "/catalog.html"
```

### 4.2 Phase 2: Salesforce Integration (3 days)

#### 4.2.1 Email Template

```html
<!-- Salesforce Email Template -->
<messaging:emailTemplate subject="Your PSi Catalog is Ready">
    <messaging:htmlEmailBody>
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h1 style="color: #003F87;">Hi {!Contact.FirstName},</h1>
                
                <p>Your personalized catalog is ready with custom pricing for {!Account.Name}.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{!CatalogURL}" 
                       style="background: #003F87; 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 5px;
                              font-size: 18px;
                              display: inline-block;">
                        OPEN YOUR CATALOG
                    </a>
                </div>
                
                <p style="color: #666; font-size: 12px;">
                    This catalog works offline after first view. 
                    Bookmark it for easy reordering!
                </p>
            </div>
        </body>
        </html>
    </messaging:htmlEmailBody>
</messaging:emailTemplate>
```

#### 4.2.2 Apex Code for URL Generation

```java
public class CatalogURLGenerator {
    
    public static String generateCatalogURL(Id accountId) {
        // 1. Get account and products
        Account acc = [SELECT Id, Name, Pricing_Tier__c, 
                      Credit_Limit__c, Account_Manager__c 
                      FROM Account WHERE Id = :accountId];
        
        List<Product2> products = getProductsForAccount(acc);
        
        // 2. Build catalog JSON
        Map<String, Object> catalog = new Map<String, Object>{
            'version' => '2.0',
            'generated' => DateTime.now().formatGMT('yyyy-MM-dd\'T\'HH:mm:ss\'Z\''),
            'expires' => DateTime.now().addDays(30).formatGMT('yyyy-MM-dd\'T\'HH:mm:ss\'Z\''),
            'company' => new Map<String, Object>{
                'name' => 'PSi',
                'minimumOrder' => 850
            },
            'customer' => buildCustomerData(acc),
            'products' => buildProductList(products, acc)
        };
        
        // 3. Convert to JSON
        String json = JSON.serialize(catalog);
        
        // 4. Compress (using JavaScript via Visualforce)
        String compressed = compressData(json);
        
        // 5. Build URL
        return 'https://psi.com/catalog#' + compressed;
    }
    
    @RemoteAction
    public static String compressData(String data) {
        // Call out to compression service or use Visualforce JavaScript
        return LZStringCompressor.compress(data);
    }
}
```

### 4.3 Phase 3: Core Features (1 week)

#### 4.3.1 Product Display & Filtering

```javascript
class ProductGrid {
    constructor(products) {
        this.products = products;
        this.filters = {
            category: '',
            search: '',
            minPrice: 0,
            maxPrice: 1000
        };
    }
    
    renderProducts() {
        const filtered = this.applyFilters();
        const html = filtered.map(product => `
            <div class="product-card" data-id="${product.id}">
                <h3>${product.title}</h3>
                <p class="publisher">${product.publisher}</p>
                <div class="pricing">
                    <span class="cost">$${product.price.toFixed(2)}</span>
                    <span class="msrp">MSRP: $${product.msrp}</span>
                    <span class="margin">${product.margin}% margin</span>
                </div>
                <div class="controls">
                    <button onclick="app.addToCart('${product.id}')">
                        Add to Cart
                    </button>
                    <input type="number" 
                           id="qty-${product.id}" 
                           value="1" 
                           min="1" 
                           max="999">
                </div>
                <div class="hints">
                    Case qty: ${product.caseQty}
                </div>
            </div>
        `).join('');
        
        document.getElementById('products').innerHTML = html;
    }
    
    applyFilters() {
        return this.products.filter(product => {
            if (this.filters.category && product.category !== this.filters.category) {
                return false;
            }
            if (this.filters.search) {
                const search = this.filters.search.toLowerCase();
                const inTitle = product.title.toLowerCase().includes(search);
                const inPublisher = product.publisher.toLowerCase().includes(search);
                if (!inTitle && !inPublisher) return false;
            }
            if (product.price < this.filters.minPrice || 
                product.price > this.filters.maxPrice) {
                return false;
            }
            return true;
        });
    }
}
```

#### 4.3.2 Cart Management

```javascript
class CartManager {
    constructor(minimumOrder = 850) {
        this.items = [];
        this.minimumOrder = minimumOrder;
        this.loadFromStorage();
    }
    
    addToCart(productId, quantity = 1) {
        const product = app.catalog.products.find(p => p.id === productId);
        if (!product) return;
        
        const existingItem = this.items.find(item => item.productId === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            this.items.push({
                productId: productId,
                product: product,
                quantity: quantity
            });
        }
        
        this.save();
        this.render();
        this.showProfitAnimation(product, quantity);
    }
    
    getTotals() {
        const totals = this.items.reduce((acc, item) => {
            const lineTotal = item.product.price * item.quantity;
            const retailTotal = item.product.msrp * item.quantity;
            
            return {
                items: acc.items + item.quantity,
                subtotal: acc.subtotal + lineTotal,
                retailValue: acc.retailValue + retailTotal,
                profit: acc.profit + (retailTotal - lineTotal)
            };
        }, {items: 0, subtotal: 0, retailValue: 0, profit: 0});
        
        totals.marginPercent = totals.retailValue > 0 
            ? ((totals.profit / totals.retailValue) * 100).toFixed(1)
            : 0;
            
        return totals;
    }
    
    showProfitAnimation(product, quantity) {
        const profit = (product.msrp - product.price) * quantity;
        
        // Create floating profit indicator
        const indicator = document.createElement('div');
        indicator.className = 'profit-indicator';
        indicator.textContent = `+$${profit.toFixed(2)} profit!`;
        document.body.appendChild(indicator);
        
        // Animate and remove
        setTimeout(() => indicator.remove(), 2000);
    }
    
    exportOrder() {
        const totals = this.getTotals();
        
        // Check minimum
        if (totals.subtotal < this.minimumOrder) {
            alert(`Order minimum is $${this.minimumOrder}. Add $${(this.minimumOrder - totals.subtotal).toFixed(2)} more.`);
            return;
        }
        
        // Generate CSV
        const csv = this.generateCSV();
        
        // Download CSV
        const blob = new Blob([csv], {type: 'text/csv'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `psi_order_${Date.now()}.csv`;
        a.click();
        
        // Also prepare email
        this.sendViaEmail();
    }
    
    generateCSV() {
        const headers = ['SKU', 'Product', 'Quantity', 'Unit Price', 'Total', 'Profit'];
        const rows = this.items.map(item => [
            item.product.sku,
            item.product.title,
            item.quantity,
            item.product.price.toFixed(2),
            (item.product.price * item.quantity).toFixed(2),
            ((item.product.msrp - item.product.price) * item.quantity).toFixed(2)
        ]);
        
        return [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');
    }
}
```

#### 4.3.3 Offline Support

```javascript
class OfflineManager {
    constructor() {
        this.setupServiceWorker();
        this.setupOfflineDetection();
    }
    
    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js');
        }
    }
    
    setupOfflineDetection() {
        window.addEventListener('online', () => {
            this.syncData();
            this.showNotification('Back online! Checking for updates...');
        });
        
        window.addEventListener('offline', () => {
            this.showNotification('Working offline. Your cart is saved locally.');
        });
    }
    
    syncData() {
        // Check for catalog updates
        fetch('/api/catalog/version')
            .then(r => r.json())
            .then(data => {
                if (data.version > app.catalog.version) {
                    this.showUpdatePrompt();
                }
            })
            .catch(() => {
                // Fail silently
            });
    }
}
```

### 4.4 Phase 4: Advanced Features (1 week)

#### 4.4.1 Analytics Integration

```javascript
class Analytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.events = [];
    }
    
    track(event, data) {
        const eventData = {
            event: event,
            data: data,
            timestamp: Date.now(),
            sessionId: this.sessionId,
            catalogVersion: app.catalog.version,
            customerId: app.catalog.customer.id
        };
        
        this.events.push(eventData);
        
        // Send to analytics endpoint (fire and forget)
        fetch('/api/analytics', {
            method: 'POST',
            body: JSON.stringify(eventData),
            headers: {'Content-Type': 'application/json'}
        }).catch(() => {});
    }
    
    trackCatalogOpen() {
        this.track('catalog_opened', {
            source: document.referrer,
            productsCount: app.catalog.products.length,
            customerTier: app.catalog.customer.tier
        });
    }
    
    trackProductView(productId) {
        const product = app.catalog.products.find(p => p.id === productId);
        this.track('product_viewed', {
            productId: productId,
            price: product.price,
            margin: product.margin
        });
    }
    
    trackAddToCart(productId, quantity) {
        const product = app.catalog.products.find(p => p.id === productId);
        this.track('added_to_cart', {
            productId: productId,
            quantity: quantity,
            value: product.price * quantity,
            profit: (product.msrp - product.price) * quantity
        });
    }
    
    trackOrderSubmit(order) {
        this.track('order_submitted', {
            orderValue: order.totals.subtotal,
            profitValue: order.totals.profit,
            itemCount: order.totals.items,
            productCount: order.items.length
        });
    }
}
```

#### 4.4.2 Progressive Enhancement

```javascript
class ProgressiveLoader {
    constructor() {
        this.coreProducts = 50;  // In URL
        this.extendedProducts = null;  // Load separately
    }
    
    async loadExtendedCatalog() {
        // If we have core products from URL
        if (app.catalog && app.catalog.products.length === this.coreProducts) {
            try {
                // Load extended product set
                const response = await fetch('/products-extended.json');
                const extended = await response.json();
                
                // Merge with personalized pricing
                const merged = this.mergeProducts(app.catalog.products, extended);
                app.catalog.products = merged;
                
                // Re-render
                app.productGrid.renderProducts();
                
                // Save to storage
                app.saveToStorage();
                
            } catch(e) {
                console.log('Could not load extended catalog, using core only');
            }
        }
    }
    
    mergeProducts(core, extended) {
        // Core products have personalized pricing
        const coreMap = new Map(core.map(p => [p.id, p]));
        
        // Add extended products with default pricing
        extended.forEach(product => {
            if (!coreMap.has(product.id)) {
                // Apply customer tier discount
                const discount = app.catalog.customer.discount || 0;
                product.price = product.price * (1 - discount);
                coreMap.set(product.id, product);
            }
        });
        
        return Array.from(coreMap.values());
    }
}
```

---

## 5. SALESFORCE INTEGRATION DETAILS

### 5.1 Campaign Setup

```sql
-- Create campaign with custom fields
INSERT INTO Campaign (
    Name,
    Type,
    Status,
    Catalog_Version__c,
    Products_Count__c,
    Compression_Type__c
) VALUES (
    'Q1 2025 Catalog Distribution',
    'Email',
    'In Progress',
    '2.0',
    150,
    'LZString'
);
```

### 5.2 Merge Field Configuration

```xml
<!-- Custom merge fields for email template -->
<apex:page controller="CatalogController">
    <apex:variable var="catalogURL" value="{!generateCatalogURL(Contact.AccountId)}"/>
    
    <!-- Email body -->
    <messaging:emailTemplate>
        <p>Hi {!Contact.FirstName},</p>
        
        <p>Your catalog for {!Account.Name} is ready:</p>
        
        <a href="{!catalogURL}">Open Catalog</a>
        
        <!-- Personalization details -->
        <ul>
            <li>Your pricing tier: {!Account.Pricing_Tier__c}</li>
            <li>Credit limit: ${!Account.Credit_Limit__c}</li>
            <li>Account manager: {!Account.Account_Manager__r.Name}</li>
        </ul>
    </messaging:emailTemplate>
</apex:page>
```

### 5.3 Automation Flow

```yaml
trigger: AccountUpdated
conditions:
  - Pricing_Tier__c changed
  - OR Credit_Limit__c changed
  - OR Product_Access__c changed

actions:
  1. RegenerateCatalogURL:
      class: CatalogURLGenerator
      method: generateCatalogURL
      params: [accountId]
      
  2. UpdateCampaignMember:
      fields:
        Catalog_URL__c: "{!result}"
        URL_Generated_Date__c: NOW()
        
  3. SendEmail:
      template: Catalog_Updated_Notification
      recipient: Account.Primary_Contact__c
```

---

## 6. TESTING STRATEGY

### 6.1 Unit Tests

```javascript
describe('Catalog URL System', () => {
    test('Compression reduces size by >80%', () => {
        const catalog = generateTestCatalog(150);
        const json = JSON.stringify(catalog);
        const compressed = LZString.compressToEncodedURIComponent(json);
        
        const ratio = compressed.length / json.length;
        expect(ratio).toBeLessThan(0.2);
    });
    
    test('URL fits within browser limits', () => {
        const url = generateCatalogURL(testAccount, products);
        expect(url.length).toBeLessThan(65536); // Firefox limit
    });
    
    test('Decompression recovers exact data', () => {
        const original = generateTestCatalog(150);
        const compressed = compress(original);
        const decompressed = decompress(compressed);
        
        expect(decompressed).toEqual(original);
    });
});
```

### 6.2 Integration Tests

```javascript
describe('End-to-end flow', () => {
    test('Email link opens catalog', async () => {
        // Generate URL
        const url = await generateCatalogURL(testCustomer);
        
        // Simulate browser navigation
        await page.goto(url);
        
        // Verify catalog loads
        await page.waitForSelector('.product-grid');
        const products = await page.$$('.product-card');
        
        expect(products.length).toBeGreaterThan(0);
    });
    
    test('Cart persists across sessions', async () => {
        // Add items to cart
        await addToCart('PROD001', 5);
        
        // Reload page
        await page.reload();
        
        // Verify cart restored
        const cartItems = await getCartItems();
        expect(cartItems).toContainEqual({
            productId: 'PROD001',
            quantity: 5
        });
    });
});
```

### 6.3 Browser Compatibility Matrix

| Browser | Version | URL Length | Compression | localStorage | Status |
|---------|---------|------------|-------------|--------------|---------|
| Chrome | 90+ | 2MB | ✓ | ✓ | Full Support |
| Firefox | 88+ | 64KB | ✓ | ✓ | Full Support |
| Safari | 14+ | 80KB | ✓ | ✓ | Full Support |
| Edge | 90+ | 2MB | ✓ | ✓ | Full Support |
| IE 11 | - | 2KB | ✓ | ✓ | Limited (50 products max) |

---

## 7. DEPLOYMENT GUIDE

### 7.1 CDN Setup (CloudFront)

```bash
# Create S3 bucket
aws s3 mb s3://psi-catalog-static

# Upload static files
aws s3 cp catalog.html s3://psi-catalog-static/catalog.html \
  --content-type "text/html" \
  --cache-control "public, max-age=86400"

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name psi-catalog-static.s3.amazonaws.com \
  --default-root-object catalog.html
```

### 7.2 DNS Configuration

```
Type: CNAME
Name: catalog
Value: d123456789.cloudfront.net
TTL: 300
```

### 7.3 SSL Certificate

```bash
# Request certificate
aws acm request-certificate \
  --domain-name catalog.psi.com \
  --validation-method DNS

# Attach to CloudFront
aws cloudfront update-distribution \
  --id E1234567890 \
  --viewer-certificate AcmCertificateArn=arn:aws:acm:...
```

---

## 8. MONITORING & ANALYTICS

### 8.1 Key Metrics

```javascript
// Track these KPIs
const metrics = {
  // Engagement
  catalogOpens: 'COUNT(DISTINCT sessionId) WHERE event="catalog_opened"',
  avgTimeOnSite: 'AVG(sessionDuration)',
  productsViewed: 'AVG(COUNT(product_viewed) GROUP BY sessionId)',
  
  // Conversion  
  cartAddRate: 'COUNT(added_to_cart) / COUNT(catalog_opened)',
  orderSubmitRate: 'COUNT(order_submitted) / COUNT(catalog_opened)',
  avgOrderValue: 'AVG(orderValue) WHERE event="order_submitted"',
  
  // Technical
  loadTime: 'AVG(loadTime) WHERE event="catalog_loaded"',
  errorRate: 'COUNT(error) / COUNT(catalog_opened)',
  browserDistribution: 'COUNT(sessionId) GROUP BY browserType'
};
```

### 8.2 Error Tracking

```javascript
window.addEventListener('error', (e) => {
  // Log to analytics
  analytics.track('error', {
    message: e.message,
    stack: e.stack,
    url: window.location.href,
    catalog: app.catalog ? app.catalog.version : null
  });
});
```

### 8.3 A/B Testing

```javascript
class ABTest {
  constructor() {
    // Assign variant based on customer ID
    this.variant = this.hashCustomerId() % 2 === 0 ? 'A' : 'B';
  }
  
  applyVariant() {
    if (this.variant === 'A') {
      // Original: Show all products
      app.showAllProducts();
    } else {
      // Test: Show featured products first
      app.showFeaturedFirst();
    }
    
    // Track variant
    analytics.track('ab_test_assigned', {
      test: 'featured_products',
      variant: this.variant
    });
  }
}
```

---

## 9. MAINTENANCE & UPDATES

### 9.1 Version Management

```javascript
// Catalog versioning strategy
const versionCheck = async () => {
  const current = app.catalog.version;
  const latest = await fetch('/api/catalog/version').then(r => r.json());
  
  if (latest.version > current) {
    if (latest.breaking) {
      // Force reload with new URL
      alert('New catalog available. Click OK to update.');
      window.location.href = latest.url;
    } else {
      // Soft update
      const updates = await fetch('/api/catalog/updates?since=' + current);
      app.mergeUpdates(updates);
    }
  }
};
```

### 9.2 Cache Management

```javascript
// Clear old data periodically
const cleanupStorage = () => {
  const maxAge = 30 * 24 * 60 * 60 * 1000; // 30 days
  const stored = localStorage.getItem('psi_catalog_date');
  
  if (stored) {
    const age = Date.now() - new Date(stored).getTime();
    if (age > maxAge) {
      localStorage.removeItem('psi_catalog');
      localStorage.removeItem('psi_catalog_date');
      localStorage.removeItem('psi_cart');
    }
  }
};
```

---

## 10. ROLLOUT PLAN

### Phase 1: Pilot (Week 1)
- Deploy static HTML to CDN
- Test with 5 friendly retailers
- Monitor load times and errors
- Gather feedback

### Phase 2: Limited Release (Week 2-3)
- Roll out to 50 customers
- A/B test email subject lines
- Monitor conversion rates
- Optimize based on data

### Phase 3: Full Launch (Week 4)
- Deploy to all customers
- Enable analytics dashboard
- Set up automated monitoring
- Document lessons learned

### Success Criteria
- 80% email open rate
- 60% catalog click-through rate  
- 30% add-to-cart rate
- 15% order submission rate
- <2 second load time
- <1% error rate

---

## APPENDIX A: Complete Implementation Checklist

### Technical Setup
- [ ] Create static HTML file with LZ-String
- [ ] Deploy to CDN (CloudFront/Cloudflare)
- [ ] Configure custom domain (catalog.psi.com)
- [ ] Set up SSL certificate
- [ ] Test compression with 150 products
- [ ] Verify browser compatibility
- [ ] Implement localStorage fallback
- [ ] Add offline support

### Salesforce Integration  
- [ ] Create Apex class for URL generation
- [ ] Build email template with merge fields
- [ ] Set up campaign automation
- [ ] Test with sample accounts
- [ ] Configure analytics tracking
- [ ] Document merge field mappings

### Features
- [ ] Product grid with images
- [ ] Search and filter
- [ ] Cart management
- [ ] Minimum order enforcement
- [ ] Profit calculations
- [ ] Order export (CSV)
- [ ] Email order submission
- [ ] Offline capability

### Testing
- [ ] Unit tests for compression
- [ ] Integration tests for flow
- [ ] Browser compatibility testing
- [ ] Mobile device testing
- [ ] Load testing (1000 concurrent users)
- [ ] Error recovery testing

### Launch
- [ ] Pilot with 5 retailers
- [ ] Gather feedback
- [ ] Optimize based on metrics
- [ ] Full rollout
- [ ] Monitor analytics
- [ ] Iterate based on data

---

*End of Design Documentation v2.0*