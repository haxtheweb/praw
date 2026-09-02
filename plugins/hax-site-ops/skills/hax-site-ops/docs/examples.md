# HAX Examples

## Add pages

User:

```text
/hax add 3 pages about iguanas
```

Expected behavior:

1. Create sensible page titles.
2. Generate useful starter content.
3. Add pages using HAX CLI.
4. Verify pages were added.

## Add a quiz

User:

```text
/hax add a multiple choice quiz to the iguana overview page based on the page content
```

Expected behavior:

1. Find/read the page.
2. Generate one or more questions based on the page.
3. Prefer `<multiple-choice>` or another assessment component.
4. Insert markup using HAX-supported content update commands when available.
5. Verify the page changed.

## Analyze site

User:

```text
/hax analyze this HAX site and suggest 20 new pages
```

Expected behavior:

1. Inspect existing site structure.
2. Identify gaps.
3. Suggest useful pages.
4. Do not make changes unless asked.
