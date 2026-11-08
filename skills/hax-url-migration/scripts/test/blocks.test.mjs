import { test } from "node:test";
import assert from "node:assert/strict";
import { loadMap, convert, extract } from "../lib/blocks.mjs";
import { fidelity, unmappedComponents } from "../lib/extract.mjs";
import { proposeGaps } from "../lib/gaps.mjs";
import { nearestDDD, recommendTheme } from "../lib/theme.mjs";
import { parse } from "node-html-parser";

const maps = (...ids) => [...ids, "generic-html"].map(loadMap);

test("extractor alternatives and json keys", () => {
  const el = parse(`<div data-settings='{"youtube_url":"https://youtu.be/x"}'><img data-src="a.jpg" src="lazy.gif" alt="A"></div>`).firstChild;
  assert.equal(extract(el, "img@data-src|img@src").value, "a.jpg");
  assert.equal(extract(el, "@data-settings#youtube_url").value, "https://youtu.be/x");
  assert.equal(extract(el, "figcaption@text|=none").value, "none");
});

test("gutenberg columns become grid-plate with slotted columns", () => {
  const html = `<div class="wp-block-columns"><div class="wp-block-column"><p>Left</p></div><div class="wp-block-column"><figure class="wp-block-image"><img src="/a.jpg" alt="A"><figcaption>Cap</figcaption></figure></div></div>`;
  const r = convert(html, maps("wordpress-gutenberg"));
  assert.match(r.html, /<grid-plate layout="1-1"><div slot="col-1"><p>Left<\/p><\/div><div slot="col-2"><media-image source="\/a.jpg" alt="A" caption="Cap"><\/media-image><\/div><\/grid-plate>/);
  assert.ok(r.assets.includes("/a.jpg"));
});

test("gutenberg gallery and button", () => {
  const html = `<figure class="wp-block-gallery"><figure class="wp-block-image"><img src="1.jpg" alt="one"></figure><figure class="wp-block-image"><img src="2.jpg" alt="two"></figure></figure><div class="wp-block-buttons"><div class="wp-block-button"><a class="wp-block-button__link" href="/go">Go</a></div></div>`;
  const r = convert(html, maps("wordpress-gutenberg"));
  assert.match(r.html, /<image-gallery><media-image source="1.jpg" alt="one"><\/media-image><media-image source="2.jpg" alt="two"><\/media-image><\/image-gallery>/);
  assert.match(r.html, /<simple-cta link="\/go" label="Go"><\/simple-cta>/);
});

test("elementor accordion, counter and unwrapped structure", () => {
  const html = `<section class="elementor-section"><div class="elementor-container"><div class="elementor-column"><div class="elementor-widget-wrap">
    <div class="elementor-element elementor-widget elementor-widget-accordion"><div class="elementor-widget-container"><div class="elementor-accordion">
      <div class="elementor-accordion-item"><div class="elementor-tab-title">Q1</div><div class="elementor-tab-content"><p>A1</p></div></div>
      <div class="elementor-accordion-item"><div class="elementor-tab-title">Q2</div><div class="elementor-tab-content"><p>A2</p></div></div>
    </div></div></div>
    <div class="elementor-widget-counter"><span class="elementor-counter-number" data-from-value="0" data-to-value="250"></span><span class="elementor-counter-number-suffix">+</span></div>
  </div></div></div></section>`;
  const r = convert(html, maps("wordpress-elementor"));
  assert.match(r.html, /<a11y-collapse-group><a11y-collapse heading="Q1"><p>A1<\/p><\/a11y-collapse><a11y-collapse heading="Q2"><p>A2<\/p><\/a11y-collapse><\/a11y-collapse-group>/);
  assert.match(r.html, /<count-up end="250" start="0" suffixtext="\+"><\/count-up>/);
  assert.doesNotMatch(r.html, /elementor/);
});

test("drupal layout builder ratio comes from the class", () => {
  const html = `<div class="layout layout--twocol-section layout--twocol-section--33-67"><div class="layout__region layout__region--first"><p>a</p></div><div class="layout__region layout__region--second"><p>b</p></div></div>`;
  const r = convert(html, maps("drupal"));
  assert.match(r.html, /<grid-plate layout="1-2"><div slot="col-1"><p>a<\/p><\/div><div slot="col-2"><p>b<\/p><\/div><\/grid-plate>/);
});

test("drupal unknown paragraph bundle is flagged as a gap but keeps its text", () => {
  const html = `<div class="paragraph paragraph--type--hero-banner"><h2>Welcome</h2><p>Hello there</p></div>`;
  const r = convert(html, maps("drupal"));
  assert.equal(r.stats.flags[0].flag, "gap");
  assert.equal(r.stats.flags[0].gapKey, "hero-banner");
  assert.match(r.html, /Welcome/);
  assert.equal(fidelity(html, r.html).ratio, 1);
});

test("generic: details, youtube, code, forms", () => {
  const html = `<details><summary>More</summary><p>Hidden</p></details>
    <iframe src="https://www.youtube.com/embed/abc" title="Talk"></iframe>
    <pre><code class="language-js">const a = 1 &lt; 2;</code></pre>
    <form action="/x"><input name="q"></form>`;
  const r = convert(html, maps());
  assert.match(r.html, /<a11y-collapse heading="More"><p>Hidden<\/p><\/a11y-collapse>/);
  assert.match(r.html, /<video-player source="https:\/\/www.youtube.com\/embed\/abc" media-title="Talk"><\/video-player>/);
  assert.match(r.html, /<code-sample type="js"><template preserve-content="preserve-content">const a = 1 &lt; 2;<\/template><\/code-sample>/);
  assert.ok(r.stats.flags.some((f) => f.flag === "form"));
});

test("emdash blocks", () => {
  const html = `<div class="emdash-columns"><div class="emdash-column"><p>x</p></div><div class="emdash-column"><p>y</p></div></div><figure class="emdash-pullquote"><blockquote class="emdash-pullquote__text"><p>Q</p></blockquote><cite class="emdash-pullquote__citation">Me</cite></figure>`;
  const r = convert(html, maps("emdash"));
  assert.match(r.html, /<grid-plate layout="1-1">/);
  assert.match(r.html, /<block-quote citation="Me"><p>Q<\/p><\/block-quote>/);
});

test("stop-note slots for docs callouts", () => {
  const html = `<div class="theme-admonition theme-admonition-warning"><div class="admonitionHeading_x">Careful</div><div class="admonitionContent_y"><p>Hot</p></div></div>`;
  const r = convert(html, maps("docusaurus"));
  assert.match(r.html, /<stop-note status="warning" title="Careful"><div slot="message"><p>Hot<\/p><\/div><\/stop-note>/);
});

test("unmapped repeated components become block proposals", () => {
  const card = (n) => `<div class="team-member"><img src="${n}.jpg" alt="${n}"><h3>${n}</h3><p>Bio</p><a href="/p/${n}">Profile</a></div>`;
  const r = convert(card("ann") + card("bo") + card("cy"), maps());
  const unmapped = unmappedComponents(r.transformed);
  assert.equal(unmapped[0].signature, "div.team-member");
  const g = proposeGaps([{ url: "https://x/a", unmapped, flags: [] }]);
  assert.equal(g.blocks[0].recommendation, "reuse");
  assert.equal(g.blocks[0].reuse.tag, "ddd-card");
});

test("theme helpers", () => {
  assert.equal(nearestDDD("#1e407c").token, "--ddd-theme-default-beaverBlue");
  const t = recommendTheme("course", ["sidebar", "prev-next"]);
  assert.ok(["clean-one", "clean-two", "learn-two-theme"].includes(t.theme));
  assert.equal(recommendTheme("psu-ddd", ["mega-menu", "hero", "footer-columns"]).theme.startsWith("polaris"), true);
});
