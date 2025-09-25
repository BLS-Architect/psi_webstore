from pathlib import Path

path = Path('catalog.html')
text = path.read_text()

# Update product-image container
original_block = "        .product-image {\n            background: var(--bg-light);\n            padding: 20px;\n            display: flex;\n            justify-content: center;\n            align-items: center;\n            height: 220px;\n        }"
updated_block = "        .product-image {\n            background: var(--bg-light);\n            padding: 20px;\n            display: flex;\n            justify-content: center;\n            align-items: center;\n            height: 220px;\n            position: relative;\n            overflow: hidden;\n        }"
if original_block in text:
    text = text.replace(original_block, updated_block)

# Update product-image img block
img_block = "        .product-image img {\n            max-width: 100%;\n            max-height: 100%;\n            object-fit: contain;\n        }"
img_updated = "        .product-image img {\n            max-width: 100%;\n            max-height: 100%;\n            object-fit: contain;\n            transition: opacity 0.3s ease;\n        }"
if img_block in text:
    text = text.replace(img_block, img_updated)

carousel_css = """
        .product-image.carousel .carousel-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(35, 31, 32, 0.65);
            color: var(--white);
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transition: opacity 0.2s ease;
        }

        .product-image.carousel:hover .carousel-nav {
            opacity: 1;
        }

        .product-image.carousel .carousel-nav.prev {
            left: 12px;
        }

        .product-image.carousel .carousel-nav.next {
            right: 12px;
        }

        .product-image.carousel .carousel-indicators {
            position: absolute;
            bottom: 12px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 6px;
        }

        .product-image.carousel .carousel-indicators span {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.35);
            transition: background 0.2s ease;
        }

        .product-image.carousel .carousel-indicators span.active {
            background: var(--psi-red);
        }

        @media (hover: none) {
            .product-image.carousel .carousel-nav {
                opacity: 1;
            }
        }
"""
marker = img_updated + "\n"
if carousel_css not in text:
    text = text.replace(marker, marker + carousel_css)

insert_point = "        const filterElements = {\n            publisher: null,\n            category: null,\n            priceBand: null,\n            sort: null,\n            clear: null,\n            count: null\n        };\n\n        let filtersBound = false;\n"
if "const carouselTimers" not in text:
    text = text.replace(insert_point, insert_point + "\n        const carouselTimers = new Map();\n\n")

cache_marker = "        function cacheFilterElements() {\n            if (filterElements.publisher) return;\n            filterElements.publisher = document.getElementById('filterPublisher');\n            filterElements.category = document.getElementById('filterCategory');\n            filterElements.priceBand = document.getElementById('filterPriceBand');\n            filterElements.sort = document.getElementById('sortProducts');\n            filterElements.clear = document.getElementById('clearFiltersButton');\n            filterElements.count = document.getElementById('productsCount');\n        }\n\n"
if "function clearCarouselTimers" not in text:
    text = text.replace(cache_marker, cache_marker + "        function clearCarouselTimers() {\n            carouselTimers.forEach(id => clearInterval(id));\n            carouselTimers.clear();\n        }\n\n")

if "function getProductImages" not in text:
    primary_marker = "        function productPrimaryImage(product) {\n            if (product.primaryImage) return product.primaryImage;\n            if (product.images && product.images.main) return product.images.main;\n            if (product.images && product.images.front) return product.images.front;\n            return 'psi.svg';\n        }\n\n"
    get_images_fn = "        function getProductImages(product) {\n            const sources = [\n                product.primaryImage,\n                product.images && product.images.main,\n                product.images && product.images.front,\n                product.images && product.images.angle,\n                product.images && product.images.pack\n            ];\n            const unique = [];\n            const seen = new Set();\n            sources.forEach(source => {\n                const sanitized = sanitizeImageUrl(source);\n                if (sanitized && !seen.has(sanitized)) {\n                    seen.add(sanitized);\n                    unique.append(sanitized);\n                }\n            });\n            if (!unique):\n                pass\n        }\n"
