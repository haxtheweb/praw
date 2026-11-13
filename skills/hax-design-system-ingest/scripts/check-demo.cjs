/**
 * Screenshot a theme's demo pages and run axe WCAG 2.1 A/AA on each.
 *
 * Start a dev server for the theme from the webcomponents monorepo ROOT first, so
 * every block's import resolves (from the element folder, blocks stay "Loading..."):
 *   npx web-dev-server --node-resolve --root-dir . \
 *     --app-index elements/<system>-theme/demo/index.html --port 8800
 *
 * usage, from the monorepo root (needs playwright, which resolves globally with
 * NODE_PATH=$(npm root -g) if it isn't installed in the repo):
 *   node check-demo.cjs <system>-theme <port> "<slug>,<slug>,..." [outdir]
 *
 * Light and dark at 1280px (full-page shots + axe) and light at 390px (viewport
 * shot + horizontal-overflow check). Pages are scrolled first so lazily loaded
 * blocks upgrade, as for a reader. "LOADING:n" counts blocks still waiting; blocks
 * inside a closed tab or collapse stay lazy and are expected there.
 */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const [theme, port, slugs, out = "demo-shots"] = process.argv.slice(2);
if (!theme || !port || !slugs) {
  console.error('usage: node check-demo.cjs <theme> <port> "<slug,...>" [outdir]');
  process.exit(2);
}
const axe = fs.readFileSync(
  require.resolve("axe-core/axe.min.js", { paths: [process.cwd()] }),
  "utf8",
);
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  let problems = 0;
  const views = [
    { scheme: "light", w: 1280, h: 900, tag: "desk" },
    { scheme: "dark", w: 1280, h: 900, tag: "desk" },
    { scheme: "light", w: 390, h: 844, tag: "phone" },
  ];
  for (const v of views) {
    const ctx = await browser.newContext({
      viewport: { width: v.w, height: v.h },
      colorScheme: v.scheme,
    });
    const page = await ctx.newPage();
    page.on("pageerror", (e) => console.log("PAGEERROR", e.message.slice(0, 160)));
    for (const slug of slugs.split(",")) {
      await page.goto(`http://localhost:${port}/elements/${theme}/demo/${slug}`, {
        waitUntil: "networkidle",
      });
      await page.waitForTimeout(2500);
      await page.evaluate(async () => {
        const h = globalThis.document.documentElement.scrollHeight;
        for (let y = 0; y < h; y += 600) {
          globalThis.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 150));
        }
        globalThis.scrollTo(0, 0);
      });
      await page.waitForTimeout(1500);
      // a theme module that fails to load leaves an empty page, which axe passes
      const rendered = await page.evaluate(
        (tag) =>
          !!globalThis.customElements.get(tag) &&
          !!globalThis.document.querySelector(tag),
        theme,
      );
      if (!rendered) {
        problems++;
        console.log(`${v.scheme} ${v.tag} ${slug || "home"}`, `NOT RENDERED: <${theme}> did not load (check the dev server log)`);
        continue;
      }
      const name = [theme, v.scheme, v.tag, slug.replace(/\//g, "_") || "home"].join("-");
      await page.screenshot({
        path: path.join(out, name + ".png"),
        fullPage: v.tag === "desk",
      });
      const label = `${v.scheme} ${v.tag} ${slug || "home"}`;
      if (v.tag === "phone") {
        const sw = await page.evaluate(() => globalThis.document.documentElement.scrollWidth);
        if (sw > v.w) {
          problems++;
          console.log(label, `horizontal overflow: ${sw}px wide at ${v.w}px`);
        }
        continue;
      }
      await page.addScriptTag({ content: axe });
      const violations = await page.evaluate(async () =>
        (
          await globalThis.axe.run(globalThis.document, {
            runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"],
          })
        ).violations.map(
          (x) =>
            `${x.id}(${x.nodes.length}): ` +
            x.nodes
              .slice(0, 2)
              .map((n) => n.target.join(" > ") + " " + (n.any[0] ? n.any[0].message.slice(0, 120) : ""))
              .join(" | "),
        ),
      );
      const loading = await page.evaluate(() => {
        let n = 0;
        const walk = (root) =>
          root.querySelectorAll("*").forEach((e) => {
            if (e.textContent === "Loading..." && !e.children.length) n++;
            if (e.shadowRoot) walk(e.shadowRoot);
          });
        walk(globalThis.document);
        return n;
      });
      problems += violations.length;
      console.log(
        label,
        violations.length ? JSON.stringify(violations) : "axe clean",
        loading ? "LOADING:" + loading : "",
      );
    }
    await ctx.close();
  }
  await browser.close();
  process.exit(problems ? 1 : 0);
})();
