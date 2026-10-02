# Pattern Library Map

Generated from `elements/d-d-d/lib/DDDPatternLibrary.js`.
This is the iron rule for pattern ids, levels, components, tokens, and contract
targets. The `hax-pattern-library-audit` skill consults this map; update it when
the registry changes.

## Summary

- **8 atoms** (recipe-only documentation — fills DDD "Logical Gaps" + theming)
- **21 molecules** (5 recipe-only, 16 gate-published via demoSchemaOverride or stax-area)
- **34 organisms** (10 recipe-only, 24 gate-published)
- **6 templates** (all stax-page)
- **10 internal contracts** (6 original + 4 site-*/theme)
- **Total: 69 patterns + 10 contracts**

## Patterns

### Atoms (8)
| id | title | components | publish |
|----|-------|------------|---------|
| atom-heading-pairings | Heading color / size / letter-spacing / line-height pairings | (none) | recipe-only |
| atom-link-chevron | Link + chevron convention | simple-icon-lite | recipe-only |
| atom-heading-treatments | Heading horizontal-line + vertical-line treatments | (none) | recipe-only |
| atom-dropcap | Drop cap on paragraph / blockquote | (none) | recipe-only |
| atom-header-slash | Double-slash after headers convention | (none) | recipe-only |
| atom-icon-sizing | Icon sizing via DDD icon variables | simple-icon-lite | recipe-only |
| atom-gradient-surface | Gradient surface | (none) | recipe-only |
| atom-palette-preview | Palette preview | hax-palette-picker | recipe-only |

### Molecules (21)
| id | title | components | publish |
|----|-------|------------|---------|
| mol-media-object | Media object | media-image | stax-area |
| mol-stat-block | Stat block | count-up | stax-area |
| mol-pill | Pill / tag | simple-tag | demoSchemaOverride → simple-tag |
| mol-callout | Callout (stop-note status variants) | stop-note | demoSchemaOverride → stop-note |
| mol-link-tile | Link tile | accent-card | demoSchemaOverride → accent-card |
| mol-avatar-byline | Avatar byline | author-card | demoSchemaOverride → author-card |
| mol-badge-chip | Badge chip (figure-label) | figure-label | demoSchemaOverride → figure-label |
| mol-pull-quote | Pull quote | block-quote | demoSchemaOverride → block-quote |
| mol-cta-button | CTA button (simple-cta variants) | simple-cta | demoSchemaOverride → simple-cta |
| mol-tag-pill-list | Tag / pill list | (none) | recipe-only |
| mol-self-check-question | Self-check question | self-check | demoSchemaOverride → self-check |
| mol-figure-caption | Figure with caption (a11y-figure) | a11y-figure | demoSchemaOverride → a11y-figure |
| mol-breadcrumb | Breadcrumb | (none) | recipe-only |
| mol-toast | Toast notification | simple-toast | recipe-only |
| mol-progress-bar | Progress bar | simple-progress | recipe-only |
| mol-form-field | Form field | simple-fields | demoSchemaOverride → simple-fields |
| mol-audio-player | Audio player | audio-player | demoSchemaOverride → audio-player |
| mol-count-display | Count display | count-up | demoSchemaOverride → count-up |
| mol-qr-code | QR code | q-r | demoSchemaOverride → q-r |
| mol-social-share | Social share links | social-share-link | recipe-only |
| mol-progress-promise | Promise progress | promise-progress | recipe-only |

### Organisms (34)
| id | title | components | publish |
|----|-------|------------|---------|
| org-hero | Hero section | page-section, simple-cta | stax-area |
| org-feature-card-grid | Feature card grid | grid-plate, accent-card | stax-area |
| org-faq-accordion | FAQ accordion group | page-section, a11y-collapse | stax-area |
| org-testimonial | Testimonial block | person-testimonial | demoSchemaOverride → person-testimonial |
| org-media-playlist | Media playlist block | media-playlist, audio-player | demoSchemaOverride → media-playlist |
| org-timeline | Timeline | lrndesign-timeline | demoSchemaOverride → lrndesign-timeline |
| org-data-table | Data table | editable-table | demoSchemaOverride → editable-table |
| org-tabs | Tabs content | a11y-tabs | demoSchemaOverride → a11y-tabs |
| org-steps | Steps / process | ddd-steps-list, ddd-steps-list-item | stax-area |
| org-pagination | Pagination | simple-pager | recipe-only |
| org-contents-menu | Page contents menu | page-contents-menu | recipe-only |
| org-empty-state | Empty state | accent-card, simple-icon-lite, simple-cta | stax-area |
| org-contact-form | Contact form | simple-fields, simple-cta | stax-area |
| org-settings-panel | Settings panel | simple-fields, a11y-collapse | stax-area |
| org-learning-objectives | Learning objectives | learning-component | demoSchemaOverride → learning-component |
| org-quiz | Quiz (multiple-choice) | multiple-choice | demoSchemaOverride → multiple-choice |
| org-flashcard-set | Flashcard set | flash-card-set | demoSchemaOverride → flash-card-set |
| org-video-feature | Video feature | video-player, page-section | stax-area |
| org-carousel | Image carousel | a11y-carousel, media-image | recipe-only |
| org-chart | Chart (bar) | lrndesign-bar | demoSchemaOverride → lrndesign-bar |
| org-stats-grid | Stats grid | grid-plate, count-up | stax-area |
| org-post-header | Post header | date-card, media-image | stax-area |
| org-post-list | Post list | post-card | demoSchemaOverride → post-card |
| org-footer | Footer | simple-tag, social-share-link | recipe-only |
| org-banner | Announcement banner | accent-card, simple-cta | stax-area |
| org-newsletter | Newsletter signup | simple-fields, simple-cta | stax-area |
| org-sidebar-layout | Sidebar layout | grid-plate | stax-area |
| org-two-column | Two column | grid-plate | stax-area |
| org-site-header | Site header (theme documentation) | site-title, site-breadcrumb, site-menu-button | recipe-only |
| org-vocab-term | Vocabulary term | vocab-term | demoSchemaOverride → vocab-term |
| org-course-syllabus | Course syllabus | oer-schema | demoSchemaOverride → oer-schema |
| org-category-list | Category list | collection-list | demoSchemaOverride → collection-list |
| org-site-menu | Site menu (theme documentation) | site-menu | recipe-only |
| org-site-top-menu | Site top menu (theme documentation) | site-top-menu | recipe-only |

### Templates (6)
| id | title | components | publish |
|----|-------|------------|---------|
| tpl-landing | Landing | page-section, grid-plate, accent-card, simple-cta | stax-page |
| tpl-article | Article / blog post | block-quote, media-image, self-check | stax-page |
| tpl-course-module | Course module | learning-component, self-check | stax-page |
| tpl-profile | Profile / bio | author-card, media-image, grid-plate | stax-page |
| tpl-faq | FAQ page | page-section, a11y-collapse | stax-page |
| tpl-gallery | Gallery / portfolio | image-gallery, media-image, grid-plate | stax-page |

## Internal contracts (10)

| id | title | target elements |
|----|-------|-----------------|
| contract-element-title | Element title / caption | video-player, a11y-media-player, stop-note, multiple-choice, media-image |
| contract-callout-status | Callout / status box | stop-note, self-check |
| contract-collapsible-heading | Collapsible heading | a11y-collapse, a11y-details, simple-fields, grade-book, cms-hax |
| contract-click-to-reveal-trigger | Click-to-reveal trigger | multiple-choice, self-check, a11y-collapse |
| contract-iframe-embed-wrapper | Iframe / embed wrapper | wikipedia-query, video-player, runkit-embed, spotify-embed, twitter-embed, linkedin-embed |
| contract-admin-fieldset | Admin panel fieldset | simple-fields, grade-book, cms-hax |
| contract-site-menu | Site menu internals | site-menu, site-top-menu, map-menu |
| contract-site-footer | Site footer internals | site-footer, license-element |
| contract-site-title | Site title typography | site-title |
| contract-theme-header | Theme header composition | all 13 DDD-based themes (learn-two-theme, chamfer-theme, journey-theme, twenty-six-theme, training-theme, haxma-theme, resume-theme, spacebook-theme, clean-portfolio-theme, glossy-portfolio-theme, polaris-theme, clean-one, clean-two) |

## HAX-capability gate

**Verified HAX-capable** (ship haxProperties — gate-published):
stop-note, wikipedia-query, multiple-choice, self-check, media-image,
editable-table, a11y-collapse, a11y-tabs, lrndesign-timeline,
person-testimonial, author-card, media-playlist, image-gallery,
image-compare-slider, a11y-figure, video-player, simple-cta, accent-card,
grid-plate, a11y-media-player, ddd-card, ddd-steps-list, ddd-steps-list-item,
page-section, figure-label, block-quote, learning-component, count-up,
simple-tag, simple-fields, flash-card-set, progress-donut, audio-player,
lrndesign-bar, lrndesign-line, lrndesign-pie, q-r, date-card, post-card,
collection-list, vocab-term, oer-schema.

**Excluded** (no haxProperties — recipe-only documentation, not published to the rail):
hax-palette-picker, simple-toast, simple-progress, social-share-link,
promise-progress, simple-pager, page-contents-menu, simple-login,
a11y-carousel, site-title, site-breadcrumb, site-menu-button, site-menu,
site-top-menu, site-footer.
