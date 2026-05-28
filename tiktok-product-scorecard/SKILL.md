---
name: tiktok-product-scorecard
description: Score products for TikTok Shop viability using a 10-category framework (Hook Potential, Problem Solving, Demonstrability, USP, Creator Compatibility, Content Angle Depth, Price/Margin, Operational Simplicity, Emotional/Social Proof, Market Timing). Use when user asks to "score a product for TikTok", "evaluate TikTok Shop products", "product scorecard", "will this product work on TikTok Shop", "rate my product for TTS", "compare products for TikTok", "TikTok product viability", or wants to assess whether a product is built to scale on TikTok Shop before investing in creators or ads.
---

# TikTok Shop Product Scorecard

Score products on 10 categories (1-10 each, total /100) to predict TikTok Shop viability before spending on creators, ads, or samples.

## Workflow

1. **Determine scope** — single product, batch comparison, or blank template only
2. **Research products** — gather product details, price, mechanism, category saturation
3. **Score each product** — use `references/scoring-framework.md` for scoring guidance
4. **Generate deliverables** — run `scripts/generate_scorecard.py` for Excel + chart
5. **Deliver with summary** — present ranked results with verdicts and key insights

## Scoring Process

Read `references/scoring-framework.md` for the full scoring rubric with 10/1 anchors per category.

For each product, score these 10 categories (1-10):

| # | Category | Core Question |
|---|----------|---------------|
| 1 | Hook Potential | Grab attention in 3-5 seconds? |
| 2 | Problem Solving Strength | Clear emotional pain point? |
| 3 | Demonstrability on Video | One clean shot demo? |
| 4 | Unique Selling Proposition | Distinct mechanism/design? |
| 5 | Creator Compatibility | Creators WANT to film it? |
| 6 | Content Angle Depth | 10+ angles possible? |
| 7 | Price Point & Margin | Impulse price + affiliate room? |
| 8 | Operational Simplicity | Easy FBT, low returns? |
| 9 | Emotional & Social Proof | Comment section explode? |
| 10 | Market Timing & Saturation | Whitespace remains? |

## Score Bands

- **80-100:** Aggressively Pursue — greenlight full rollout
- **65-79:** Strong w/ Proper Positioning — focused angle, watch CPMs/CVR
- **50-64:** Needs Better Hooks — rework before spending
- **Under 50:** Hard to Scale — walk away or rework product

## Generating the Spreadsheet

Create a JSON file with scored products (see `templates/sample_products.json` for format):

```json
[
  {
    "name": "Product Name",
    "category": "Category",
    "scores": [9, 8, 10, 7, 9, 8, 7, 9, 8, 6],
    "notes": ["rationale for each score..."]
  }
]
```

Run the generator:

```bash
python3 scripts/generate_scorecard.py --input products.json --output scorecard.xlsx --chart chart.png
```

- `--input` — JSON file with products (omit for blank template only)
- `--output` — Excel output path (default: TikTok_Shop_Product_Scorecard.xlsx)
- `--chart` — PNG visualization path (optional, requires matplotlib)

Output includes:
- **Scored Comparison tab** — all products side-by-side with conditional formatting
- **Individual product tabs** — full breakdown with rationale per category
- **Blank Scorecard tab** — ready to duplicate for new products
- **Visualization chart** — bar chart + category breakdown

## Condensed Reference Doc

When user also wants a 1-page summary, generate a Markdown doc with:
- All 10 categories with scoring questions
- Score bands table with verdicts and actions
- Notable examples with why they scored high/low

## Key Scoring Principles

- Score relative to TikTok Shop specifically, not general e-commerce
- Be honest, not optimistic — the scorecard prevents emotional spending
- A 7 is strong; reserve 9-10 for truly exceptional performance
- Market Timing is hardest — check FastMoss/Kalodata for saturation data
- Low scores in categories 6-10 are usually fixable with strategy
