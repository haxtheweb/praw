Everything in HAX is edited where you read it. There is no separate form and no markup to learn; what you see while editing is what visitors get.

Try it on this page
-------------------

1.  Press the pencil in the top bar (or Ctrl Shift E).
2.  Click this list and add a step of your own. Press Enter for a new line.
3.  Select some words and make them **bold** or a link from the text toolbar.
4.  Click a block, like the callout below, to see its settings in the panel.
5.  Press Save. Here, saving pretends to work; on your own site it is saved for real.

<stop-note title="Nothing here is saved" status="info" icon="stopnoteicons:book-icon"><p slot="message">This demo resets when you reload. Break whatever you like.</p></stop-note>

Under the hood
--------------

Each page is plain HTML on disk, and each block is a web component, so the same page works without the editor, without HAXcms, and pasted into other sites. Open View source in the editor to see this page's HTML.

<a11y-collapse heading="Why web components?" heading-button="" icon="icons:expand-more"><p>A web component is a custom HTML tag, like <code>&lt;video-player&gt;</code>, that the browser understands natively. HAX ships hundreds of them, and the <a href="https://hax.cloud/magic-script">magic script</a> loads each one the first time a page uses it.</p></a11y-collapse>