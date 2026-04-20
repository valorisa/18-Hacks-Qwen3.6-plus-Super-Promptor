# 🏗️ JSON WEBSITE GENERATOR — v2.0
> Transforms any user input into a production-ready Master Blueprint JSON.
> Zero bias. Zero hallucination. Every field earned from the input.

---

## ⚙️ PHASE 0 — INPUT PARSING

Extract these 7 dimensions from the user input. Mark each `[VERIFIED]` or `[DEFAULT]`:

| Dimension         | Extraction rule                                          | Default if missing         |
|-------------------|----------------------------------------------------------|----------------------------|
| `sector`          | Domain or industry inferred from nouns/context           | `"general_services"`       |
| `target_audience` | Who benefits — demographics, role, pain points           | `"broad_public"`           |
| `tone_vibe`       | Emotional register: clinical / playful / luxury / civic  | `"professional_neutral"`   |
| `primary_goal`    | Core conversion: sell / inform / recruit / book / donate | `"generate_leads"`         |
| `brand_name`      | Explicit name OR `[À CLARIFIER]`                         | `"{{BRAND_NAME}}"`         |
| `locale_lang`     | Language + region from input or context                  | `"fr-FR"`                  |
| `constraints`     | Budget tier, tech stack imposed, hard requirements       | `[]`                       |

**Extraction rule**: ≥ 5 dimensions confirmed → mark `"input_confidence": "high"`.
3–4 confirmed → `"medium"` + activate `default_fallback: true`.
< 3 → halt and output a clarification request (do NOT generate the blueprint).

---

## 🎨 PHASE 1 — DESIGN SYSTEM DERIVATION

### 1.1 Color System
Derive a semantic color token system (not just 4 hex values).
All colors must have a dark-mode pair. Use HSL so variants are computable.

```
primary       → dominant action color (CTA, links, highlights)
primary-dark  → dark-mode shift of primary (lightness +20%)
secondary     → supportive / decorative
accent        → contrast pop (use sparingly, < 10% of UI surface)
neutral-900   → headings (dark mode: neutral-50)
neutral-700   → body text (dark mode: neutral-200)
neutral-100   → subtle backgrounds, cards (dark mode: neutral-800)
surface       → page background (dark mode: near-black)
border        → dividers, inputs (10–15% opacity)
semantic:
  success, warning, error, info
```

### 1.2 Typography Scale
Full modular scale (ratio 1.25), not just two fonts.

```
font-xs:  0.75rem
font-sm:  0.875rem
font-md:  1rem         ← body default, line-height: 1.6
font-lg:  1.25rem
font-xl:  1.563rem
font-2xl: 1.953rem
font-3xl: 2.441rem     ← hero headline
font-4xl: 3.052rem     ← display / impact

heading weight: 600 | body weight: 400 | label weight: 500
```

### 1.3 Spacing Scale (4px base unit)
`[4, 8, 12, 16, 24, 32, 48, 64, 96, 128]px`
Map semantically: `spacing-xs=4`, `spacing-sm=8`, `spacing-md=16`, `spacing-lg=32`, `spacing-xl=64`

### 1.4 Motion Tokens
```
duration-fast:   150ms  → hover states, tooltips
duration-base:   300ms  → modals, transitions
duration-slow:   600ms  → page loads, reveals
easing-default: cubic-bezier(0.4, 0, 0.2, 1)
easing-spring:  cubic-bezier(0.34, 1.56, 0.64, 1)
reduced-motion: prefers-reduced-motion: reduce → all durations: 0ms
```

### 1.5 Breakpoints
```
xs: 375px   → mobile portrait
sm: 640px   → mobile landscape
md: 768px   → tablet
lg: 1024px  → small desktop
xl: 1280px  → standard desktop
2xl: 1536px → wide screen
```

### 1.6 Style Variants (pick 1 of 3 based on tone_vibe)
| Variant          | When to choose                                | Key overrides                                                    |
|------------------|-----------------------------------------------|------------------------------------------------------------------|
| `clean_modern`   | SaaS, tech, neutral sectors                   | radius: 8px, shadow: soft-sm, spacing: generous, weight: light  |
| `bold_editorial` | Fashion, culture, media, luxury               | radius: 0–4px, contrast: high, font-display: heavy, grid: asymmetric |
| `structured_pro` | Legal, finance, medical, institutional        | radius: 4px, grid: 12-col strict, palette: muted, CTA: outlined |

---

## 📐 PHASE 2 — SITE ARCHITECTURE

### Standard module set (adapt to sector):
```
/ → Landing / Home
/[offer-slug] → Core offer or product page
/about → Brand story, team, mission
/[resources|blog|guides] → Content hub (SEO magnet)
/contact → Conversion endpoint
/legal/[privacy|terms] → Compliance
```

### Per-page mandatory fields:
- `route`, `page_title`, `meta_title` (≤ 60 chars), `meta_description` (≤ 155 chars)
- `og_image_hint` (describe ideal OG image), `canonical_url`
- `schema_type` (LocalBusiness / SoftwareApplication / Article / etc.)
- `sections[]` with full `content_brief` per section

### Content Brief schema (per section):
```json
{
  "section_id": "hero",
  "layout_pattern": "split_text_image | centered_hero | fullwidth_video | grid_cards",
  "content_hierarchy": {
    "h1_or_h2": "{{HEADLINE_HINT}}",
    "subheadline": "{{SUBHEAD_HINT}}",
    "body_copy": { "word_count": [80, 120], "format": "short_paragraphs" },
    "cta_primary": { "label": "{{CTA_TEXT}}", "destination": "{{ROUTE}}", "style": "filled" },
    "cta_secondary": { "label": "{{CTA_TEXT}}", "destination": "{{ROUTE}}", "style": "ghost" }
  },
  "tone_matrix": {
    "formal":       [0,10],
    "warm":         [0,10],
    "authoritative":[0,10],
    "playful":      [0,10],
    "urgent":       [0,10]
  },
  "seo_brief": {
    "primary_kw":   ["{{KW1}}", "{{KW2}}"],
    "secondary_kw": ["{{KW3}}", "{{KW4}}"],
    "semantic_field": ["{{TERM1}}", "{{TERM2}}", "{{TERM3}}"]
  },
  "content_pillars": ["{{PILLAR_1}}", "{{PILLAR_2}}"],
  "micro_interactions": ["fade_in_up", "stagger_children", "hover_lift"],
  "a11y_notes": "{{E.G. ensure contrast 4.5:1, ARIA label on CTA}}"
}
```

---

## 💻 PHASE 3 — TECH STACK SELECTION (CONDITIONAL)

Select based on `constraints` + `primary_goal` + `sector`:

```
IF constraints.cms_required:
  → cms: "WordPress" | "Sanity" | "Strapi" | "Contentful"
ELSE IF sector IN ["saas","app","tool"]:
  → frontend: "Next.js 14 (App Router)", styling: "Tailwind CSS", anim: "Framer Motion"
ELSE IF primary_goal == "showcase" OR sector IN ["portfolio","agency","creative"]:
  → frontend: "Astro 4", styling: "Tailwind CSS", anim: "GSAP ScrollTrigger"
ELSE IF constraints.budget == "low" OR "static":
  → frontend: "Astro 4 (static)", styling: "Tailwind CSS", anim: "CSS-only"
DEFAULT:
  → frontend: "Next.js 14", styling: "Tailwind CSS", anim: "Framer Motion"

host:  Vercel (Next.js) | Netlify (Astro) | Railway (full-stack)
cicd:  GitHub Actions
analytics: GA4 + Plausible (privacy-first fallback)
perf_monitoring: Sentry + Web Vitals API
```

---

## 🔍 PHASE 4 — SEO & SCHEMA SYSTEM

### Per-page schema.org (choose correct @type):
```
Landing/Home     → Organization + WebSite + SearchAction
Product/Service  → Service | Product | SoftwareApplication
Blog post        → Article + BreadcrumbList
Local business   → LocalBusiness + GeoCoordinates + OpeningHours
E-commerce       → Product + Offer + AggregateRating
```

### Mandatory SEO fields:
```json
{
  "title_tag": "≤60 chars | primary_kw + brand",
  "meta_description": "≤155 chars | action verb + value prop + brand",
  "og_title": "≤70 chars | engaging, social-first",
  "og_description": "≤200 chars",
  "og_image": { "hint": "{{DESCRIBE IDEAL IMAGE}}", "dims": "1200x630", "format": "webp" },
  "twitter_card": "summary_large_image",
  "canonical": "{{FULL_URL}}",
  "hreflang": [{ "lang": "{{LOCALE}}", "url": "{{URL}}" }],
  "robots": "index, follow",
  "sitemap": true,
  "structured_data": "{{SCHEMA_JSON_LD}}"
}
```

---

## ✅ PHASE 5 — QUALITY GATES

Before emitting the JSON, verify internally:

| Gate                    | Criterion                                              | Pass? |
|-------------------------|--------------------------------------------------------|-------|
| JSON validity           | RFC 8259 parseable, no trailing commas                 | ✓/✗   |
| Completeness            | UX, content, SEO, tech, assets, a11y, perf all covered | ✓/✗   |
| No hallucinations       | Every value earned from input or marked `[DEFAULT]`    | ✓/✗   |
| Placeholders honest     | `{{VAR}}` used only for genuinely unknown values       | ✓/✗   |
| Schema valid            | @type matches page purpose                             | ✓/✗   |
| Dark mode paired        | Every color has a dark-mode counterpart                | ✓/✗   |
| Responsive covered      | Breakpoints present in design_system                   | ✓/✗   |
| Motion accessible       | reduced_motion token present                           | ✓/✗   |

Any ✗ → fix before output.

---

## 📦 MASTER OUTPUT SCHEMA

```json
{
  "master_blueprint": {

    "meta": {
      "version": "2.0",
      "generator": "JSON Website Generator",
      "input_confidence": "high | medium | low",
      "default_fallback": false,
      "locale": "{{LOCALE}}",
      "brand_name": "{{BRAND}}",
      "sector": "{{SECTOR}}",
      "target_audience": "{{AUDIENCE}}",
      "tone_vibe": "{{VIBE}}",
      "primary_goal": "{{GOAL}}",
      "constraints": [],
      "quality_targets": {
        "lighthouse_min": 90,
        "lcp_ms_max": 2500,
        "cls_max": 0.1,
        "fid_ms_max": 100,
        "wcag": "2.2 AA",
        "bundle_js_kb_max": 150,
        "bundle_css_kb_max": 30
      },
      "execution_order": [
        "parse_input",
        "derive_design_tokens",
        "scaffold_routes",
        "inject_content_briefs",
        "configure_tech_stack",
        "generate_seo_schema",
        "a11y_audit",
        "perf_budget_check",
        "deploy_pipeline"
      ],
      "chunking": {
        "enabled": false,
        "part": 1,
        "total_parts": 1,
        "reconstruction_order": ["meta","design_system","site_structure","tech_stack","seo"]
      },
      "style_recommendation": "{{1-SENTENCE JUSTIFICATION}}"
    },

    "design_system": {

      "colors": {
        "light": {
          "primary":       "{{HSL}}",
          "primary-hover": "{{HSL}}",
          "secondary":     "{{HSL}}",
          "accent":        "{{HSL}}",
          "neutral-900":   "{{HSL}}",
          "neutral-700":   "{{HSL}}",
          "neutral-400":   "{{HSL}}",
          "neutral-100":   "{{HSL}}",
          "surface":       "{{HSL}}",
          "border":        "hsla(0,0%,0%,0.12)",
          "success":       "{{HSL}}",
          "warning":       "{{HSL}}",
          "error":         "{{HSL}}",
          "info":          "{{HSL}}"
        },
        "dark": {
          "primary":       "{{HSL+20L}}",
          "neutral-900":   "{{HSL}}",
          "neutral-700":   "{{HSL}}",
          "neutral-100":   "{{HSL}}",
          "surface":       "{{HSL}}",
          "border":        "hsla(0,0%,100%,0.10)"
        }
      },

      "typography": {
        "scale_ratio": 1.25,
        "base_px": 16,
        "heading": { "family": "{{FONT}}", "weights": [600, 700], "tracking": "-0.02em" },
        "body":    { "family": "{{FONT}}", "weight": 400, "line_height": 1.6 },
        "label":   { "family": "{{FONT}}", "weight": 500, "tracking": "0.01em" },
        "mono":    { "family": "{{MONOFONT}}", "weight": 400 },
        "sizes": {
          "xs":"0.75rem","sm":"0.875rem","md":"1rem",
          "lg":"1.25rem","xl":"1.563rem","2xl":"1.953rem",
          "3xl":"2.441rem","4xl":"3.052rem"
        }
      },

      "spacing": {
        "base_unit_px": 4,
        "scale": [4,8,12,16,24,32,48,64,96,128],
        "semantic": {
          "xs":"4px","sm":"8px","md":"16px","lg":"32px","xl":"64px","2xl":"96px"
        }
      },

      "borders": {
        "radius": {
          "none":"0","sm":"4px","md":"8px","lg":"12px","xl":"16px","full":"9999px"
        },
        "width": { "thin":"1px","base":"1.5px","thick":"2px" }
      },

      "shadows": {
        "none":  "none",
        "sm":    "0 1px 3px hsla(0,0%,0%,0.08)",
        "md":    "0 4px 12px hsla(0,0%,0%,0.10)",
        "lg":    "0 8px 24px hsla(0,0%,0%,0.12)",
        "focus": "0 0 0 3px {{PRIMARY_HSL_30A}}"
      },

      "motion": {
        "duration-fast":  "150ms",
        "duration-base":  "300ms",
        "duration-slow":  "600ms",
        "easing-default": "cubic-bezier(0.4, 0, 0.2, 1)",
        "easing-spring":  "cubic-bezier(0.34, 1.56, 0.64, 1)",
        "reduced":        "@media (prefers-reduced-motion: reduce) { * { transition-duration: 0ms !important; } }"
      },

      "breakpoints": {
        "xs":"375px","sm":"640px","md":"768px","lg":"1024px","xl":"1280px","2xl":"1536px"
      },

      "components": [
        "Navbar", "Footer", "HeroSection", "CTACard", "FeatureGrid",
        "TestimonialCarousel", "PricingTable", "FAQAccordion",
        "BlogCard", "ContactForm", "CookieBanner", "SkipToMain"
      ],

      "style_variants": [
        {
          "id": "clean_modern",
          "description": "{{DESC}}",
          "recommended_for": ["saas","tech","startup"],
          "css_overrides": {
            "border-radius": "8px",
            "shadow": "sm",
            "font-heading-weight": 600,
            "spacing-multiplier": 1.5,
            "btn-style": "filled-rounded"
          }
        },
        {
          "id": "bold_editorial",
          "description": "{{DESC}}",
          "recommended_for": ["fashion","media","creative","luxury"],
          "css_overrides": {
            "border-radius": "0px",
            "contrast": "high",
            "font-heading-weight": 700,
            "grid": "asymmetric",
            "btn-style": "ghost-uppercase"
          }
        },
        {
          "id": "structured_pro",
          "description": "{{DESC}}",
          "recommended_for": ["legal","finance","medical","institutional"],
          "css_overrides": {
            "border-radius": "4px",
            "grid": "12-col-strict",
            "palette": "muted",
            "btn-style": "outlined",
            "spacing-multiplier": 1.0
          }
        }
      ],
      "recommended_variant": "{{VARIANT_ID}}",

      "asset_strategy": {
        "images": {
          "search_hint": "{{DESCRIBE IDEAL IMAGERY STYLE}}",
          "formats": ["webp","avif"],
          "aspect_ratios": { "hero":"16:9", "card":"4:3", "avatar":"1:1", "banner":"21:9" },
          "loading": { "above_fold": "eager", "below_fold": "lazy" },
          "srcset": true,
          "cdn_hint": "Cloudinary | imgix | next/image"
        },
        "icons": {
          "style": "{{outline|solid|duotone}}",
          "library": "lucide-react",
          "implementation": "css-var colored SVG sprites"
        },
        "videos": {
          "search_hint": "{{CONTEXT}}",
          "formats": ["mp4","webm"],
          "lazy": true,
          "poster_hint": "{{STILL FRAME DESCRIPTION}}",
          "autoplay": false,
          "playsinline": true,
          "muted": true
        },
        "fonts": {
          "source": "fontshare | google-fonts",
          "display": "swap",
          "preload": true,
          "fallback_stack": "system-ui, -apple-system, sans-serif",
          "subset": "latin"
        }
      },

      "a11y": {
        "target": "WCAG 2.2 AA",
        "color_contrast_min": 4.5,
        "focus_style": "visible ring — 3px primary offset 2px",
        "skip_link": true,
        "aria_landmarks": ["banner","main","nav","complementary","contentinfo"],
        "reduced_motion": true,
        "keyboard_nav": true,
        "alt_text_strategy": "{{contextual description of image purpose}}"
      },

      "dark_mode": {
        "strategy": "system-preference + manual toggle",
        "implementation": "CSS custom properties on :root[data-theme='dark']",
        "storage": "localStorage('theme')"
      }
    },

    "site_structure": [
      {
        "route": "/",
        "page_title": "{{BRAND}} — {{VALUE_PROP}}",
        "seo": {
          "title_tag": "{{≤60 chars | primary_kw + brand}}",
          "meta_description": "{{≤155 chars | action verb + value prop}}",
          "og_title": "{{≤70 chars}}",
          "og_description": "{{≤200 chars}}",
          "og_image_hint": "{{ideal OG image description — 1200x630}}",
          "twitter_card": "summary_large_image",
          "canonical": "https://{{DOMAIN}}/",
          "robots": "index, follow",
          "schema_type": "Organization"
        },
        "sections": [
          {
            "section_id": "hero",
            "layout_pattern": "split_text_image",
            "content_hierarchy": {
              "h1": "{{HEADLINE_HINT}}",
              "subheadline": "{{SUBHEAD_HINT}}",
              "body_copy": { "word_count": [60, 100], "format": "1-2 short paragraphs" },
              "cta_primary":   { "label": "{{CTA_TEXT}}", "destination": "/{{OFFER_ROUTE}}", "style": "filled" },
              "cta_secondary": { "label": "{{CTA_TEXT}}", "destination": "/contact", "style": "ghost" },
              "social_proof_hint": "{{e.g. '500+ clients' | 4.9★ rating | logos}}"
            },
            "tone_matrix": { "formal":0, "warm":7, "authoritative":6, "playful":3, "urgent":5 },
            "seo_brief": {
              "primary_kw": ["{{KW1}}", "{{KW2}}"],
              "secondary_kw": ["{{KW3}}", "{{KW4}}"],
              "semantic_field": ["{{TERM1}}", "{{TERM2}}"]
            },
            "content_pillars": ["{{PILLAR_1}}", "{{PILLAR_2}}"],
            "micro_interactions": ["fade_in_up", "stagger_cta_delay_200ms"],
            "a11y_notes": "H1 must be first heading on page; CTA aria-label if label is generic"
          },
          {
            "section_id": "social_proof",
            "layout_pattern": "logo_strip | testimonial_carousel",
            "content_hierarchy": {
              "eyebrow": "Trusted by",
              "items": "3–6 logos or 2–3 testimonial cards",
              "quote_hint": "{{outcome-focused, specific, attributable}}"
            },
            "tone_matrix": { "formal":3, "warm":8, "authoritative":7, "playful":2, "urgent":1 }
          },
          {
            "section_id": "features_or_offer",
            "layout_pattern": "grid_3col | alternating_image_text",
            "content_hierarchy": {
              "section_headline": "{{WHAT YOU GET HINT}}",
              "items": [
                { "icon": "{{ICON_NAME}}", "title": "{{FEATURE}}", "body": "{{2-3 sentences}}" }
              ]
            },
            "tone_matrix": { "formal":5, "warm":5, "authoritative":8, "playful":2, "urgent":3 },
            "seo_brief": {
              "primary_kw": ["{{KW1}}"],
              "semantic_field": ["{{TERM1}}", "{{TERM2}}", "{{TERM3}}"]
            }
          },
          {
            "section_id": "conversion_cta",
            "layout_pattern": "centered_band | split_form",
            "content_hierarchy": {
              "headline": "{{URGENCY OR BENEFIT HEADLINE}}",
              "body": { "word_count": [20, 50] },
              "cta_primary": { "label": "{{ACTION VERB + OUTCOME}}", "style": "filled-lg" }
            },
            "tone_matrix": { "formal":2, "warm":6, "authoritative":5, "playful":2, "urgent":8 }
          }
        ],
        "user_journey_stage": "awareness → consideration"
      }
    ],

    "tech_stack": {
      "frontend":          "{{FRAMEWORK}}",
      "styling":           "Tailwind CSS v3",
      "animation":         "{{Framer Motion | GSAP | CSS-only}}",
      "cms":               "{{CMS or null}}",
      "state_management":  "{{Zustand | none}}",
      "forms":             "React Hook Form + Zod",
      "analytics":         "GA4 + Plausible",
      "error_monitoring":  "Sentry",
      "perf_monitoring":   "Web Vitals API",
      "testing":           { "unit": "Vitest", "e2e": "Playwright", "a11y": "axe-core" },
      "host":              "{{Vercel | Netlify | Railway}}",
      "cdn":               "{{Cloudflare | host-native}}",
      "cicd":              "GitHub Actions",
      "env_secrets":       "{{host-native secrets vault}}",
      "i18n":              "{{next-intl | i18next | null}}"
    },

    "seo_schema": {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "{{PRIMARY_TYPE}}",
          "name": "{{BRAND}}",
          "description": "{{META_DESCRIPTION}}",
          "url": "https://{{DOMAIN}}",
          "logo": { "@type": "ImageObject", "url": "https://{{DOMAIN}}/logo.webp" },
          "sameAs": ["{{SOCIAL_URL_1}}", "{{SOCIAL_URL_2}}"]
        },
        {
          "@type": "WebSite",
          "name": "{{BRAND}}",
          "url": "https://{{DOMAIN}}",
          "potentialAction": {
            "@type": "SearchAction",
            "target": "https://{{DOMAIN}}/search?q={search_term_string}",
            "query-input": "required name=search_term_string"
          }
        }
      ]
    },

    "performance_budget": {
      "js_kb_max": 150,
      "css_kb_max": 30,
      "image_kb_max_hero": 200,
      "total_page_weight_kb_max": 800,
      "third_party_scripts_max": 3,
      "font_files_max": 2
    },

    "launch_checklist": [
      "favicon.ico + apple-touch-icon.png",
      "robots.txt",
      "sitemap.xml (auto-generated)",
      "404 page (on-brand)",
      "Cookie consent banner (RGPD/GDPR if EU)",
      "Legal pages: /legal/privacy + /legal/terms",
      "Open Graph image (1200×630)",
      "Lighthouse audit ≥ 90 all categories",
      "axe-core a11y audit: 0 violations",
      "Cross-browser: Chrome, Firefox, Safari, Edge",
      "Mobile: iOS Safari 15+, Chrome Android"
    ]

  }
}
```

---

## 🔁 CHUNKING PROTOCOL (> 1500 tokens output)

If the full blueprint exceeds 1500 tokens, split as follows:

```
Part 1/3 → meta + design_system
Part 2/3 → site_structure (all routes + sections)
Part 3/3 → tech_stack + seo_schema + performance_budget + launch_checklist
```

Each part opens with:
```json
{ "_chunk": { "part": N, "total": 3, "next_prompt": "Continue JSON Website Generator part N+1" } }
```

---

## 📥 USER INPUT
{{USER_KEYWORDS}}
