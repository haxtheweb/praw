# PLEDGES

What the HAX community commits to, kept here so agents and contributors can cite it. These pledges first lived in the HAX documentation site, which is retired; they now live in PRAW. `WORLDVIEW.md` says why HAX holds these values, and the [UN Sustainable Development Goals web](https://www.hax.cloud/un-sdgs) shows the goals they support.

Report a problem with any pledge in the unified issue queue, <https://github.com/haxtheweb/issues>.

## Accessibility and empowerment

HAX aims to empower as many people as possible, with a broader view of accessibility (a11y) than usual. When we say a11y, we mean access for everyone, everywhere, regardless of physical ability, technical ability or device capability.

HAX accessibility principles:

- Use as few resources as possible to deliver an experience, so people far away and on limited connections can still use it (see [Environmental impact](#environmental-impact)).
- HAX itself meets WCAG 2.0 AA.
- Within reason, HAX prevents and automatically removes the kinds of web code that lead to accessibility errors.
- Accessible, audited base classes keep every block made with or for HAX consistent, visually and non-visually.

If you notice an accessibility error or issue anywhere in HAX, [file an issue](https://github.com/haxtheweb/issues/issues/new?labels=a11y&title=%5Baccessibility%5D+) so we can fix it quickly.

Supports UN goals 4 (Quality Education) and 10 (Reduced Inequalities). Pillar: Accessible.

## Environmental impact

HAX uses web technology in an ecologically responsible way. The community values:

- Web standards over large libraries, so less is downloaded and run.
- Offline-capable progressive web apps, to reduce energy use.
- Caching and usage settings tuned to cut redundant traffic.
- A database-less approach, which reduces complexity, improves portability and needs less "always on" technology.
- Micro-services that run only when an API request needs them.

If you see a way HAX could use less energy, [file an issue](https://github.com/haxtheweb/issues/issues/new?labels=energy&title=%5Bresource+usage%5D+) describing how we can make it greener.

Supports UN goals 7 (Affordable and Clean Energy) and 12 (Responsible Consumption and Production). Pillars: Efficient, Sustainable.

## Performance is access

HAX aims to be as fast as it can possibly be, through its methods, low-level platform APIs, micro-services and lazy loading expensive assets only when needed. Performance is not a nice to have or a feature. It is access and usability, and a core ideal.

Like accessibility, when we ignore the bytes we send we discriminate against people with slow devices or poor connections. That leaves them out of the conversation and reduces their access to information.

How HAX works toward performance:

- Build directly against modern JavaScript (ES2021+ as of 2024) and move that target forward over time, sticking to web-native APIs from the last three years.
- Maximize Lighthouse and [PageSpeed Insights](https://pagespeed.web.dev/) scores, but not at the cost of shipping more data over time (see unbundling).
- Unbundle assets on the CDN as much as possible; the [magic script](https://www.hax.cloud/magic-script) loads each tag only when a page uses it.
- Send HTML in the initial page load when possible, and use server-side rendering as far as it technically can go.
- HAXcms injects [replace-tag](https://dev.to/btopro/replace-tag-with-high-performance-3ghj) on page load, so content below the fold doesn't load until it is scrolled into view.
- Lit and template literals keep DOM updates minimal when data changes.

This is the Efficient pillar in practice ([`ecosystem/build/data/pillars.json`](ecosystem/build/data/pillars.json)). Supports UN goals 7 and 12, and 10 for people on slow devices and connections.
