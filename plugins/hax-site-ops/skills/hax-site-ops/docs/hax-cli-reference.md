# HAX CLI Reference

Generated on 2026-06-05T22:47:29Z.

Command source:

```text
npx @haxtheweb/create
```

Important: never use `npx hax`; it resolves to the wrong npm package. Use `npx @haxtheweb/create` or a globally installed `hax` command from `@haxtheweb/create`.

## @haxtheweb/create --help

```text
Usage: create-haxtheweb [options] [command]

Options:
  --v                                 Verbose output
  --debug                             Output for developers
  --format <char>                     Output format; json (default), yaml
  --path <char>                       where to perform operation
  --name <char>                       name of the project/web component
  --npm-client <char>                 npm client to use (must be installed) npm,
                                      yarn, pnpm (default: "npm")
  --y                                 yes to all questions
  --skip                              skip frills like animations
  --quiet                             remove console logging
  --auto                              yes to all questions, alias of y
  --no-i                              prevent interactions / sub-process, good
                                      for scripting
  --to-file <char>                    redirect command output to a file
  --no-extras                         skip all extra / automatic command
                                      processing
  --root <char>                       root location to execute the command from
  --org <char>                        organization for package.json
  --author <char>                     author for site / package.json
  --writeHaxProperties                Write haxProperties for the element
  --force                             force creation even if name exists in
                                      registry
  --import-site <char>                URL of site to import
  --import-structure <char>           import method to use:
                                      pressbooksToSite
                                      elmslnToSite
                                      haxcmsToSite
                                      notionToSite
                                      gitbookToSite
                                      evolutionToSite
                                      ploneToSite
                                      wordpressPagesToSite
                                      drupalBookToSite
                                      htmlToSite
                                      docxToSite
  --node-op <char>                    node operation to perform
  --item-id <char>                    node ID to operate on
  --domain <char>                     published domain name
  --title-scrape <char>               CSS Selector for `title` in resource
  --content-scrape <char>             CSS Selector for `body` in resource
  --items-import <char>               import items from a file / site
  --recipe <char>                     path to recipe file
  --custom-theme-name <char>          custom theme name
  --custom-theme-template <char>      custom theme template; (options: base,
                                      polaris-flex, polaris-sidebar)
  --skeleton-file <char>              path to skeleton JSON file
  --skeleton-machine-name <char>      skeleton machine name (installed template)
                                      to create a site from
  --search <char>                     search query text or simple selector (for
                                      site:search)
  --search-field <char>               comma-separated fields for text search
                                      (title,slug,description,tags,content,all)
  --search-case-sensitive             case-sensitive text search
  --search-limit <char>               max number of site search matches to
                                      return
  --search-selector                   treat --search as a selector query (tag,
                                      tag[attr], tag[attr="value"], [attr])
  --search-mode <char>                search mode override (text or selector)
  --source <char>                     rsync source directory or remote path
  --destination <char>                rsync destination directory or remote path
  --exclude <char>                    comma-separated patterns to exclude from
                                      rsync
  --dry-run                           perform rsync dry run
  --delete                            delete extraneous files from destination
  --repos <char...>                   repositories to clone
  -V, --version                       output the version number
  --title <char>                      Title
  --content <char>                    Page content
  --slug <char>                       Path (slug)
  --published <char>                  Publishing status
  --tags <char>                       Tags
  --parent <char>                     Parent
  --order <char>                      Order
  --theme <char>                      Theme
  --hide-in-menu <char>               Hide in menu
  -h, --help                          display help for command

Commands:
  start                               Select which hax sub-program to run
  update [options]                    hax cli self update
  serve                               Launch HAXsite in development mode
                                      (http://localhost)
  site [options] [action]             create or administer a HAXsite
  wc|webcomponent [options] [action]  Create Lit based web components, with HAX
                                      recommendations
  audit [options]                     Audits web components for compliance with
                                      DDD (HAX design system)
  party [options] [action]            Party time! Join the HAX community and get
                                      involved!
  help [command]                      display help for command
```

## @haxtheweb/create site --help

```text
Usage: create-haxtheweb site [options] [action]

create or administer a HAXsite

Arguments:
  action                          Actions to perform on site include:
                                  start - Launch site in browser
                                  (http://localhost)
                                  serve - Launch site in development mode
                                  node:stats - Node Stats / data
                                  node:add - Add a new page
                                  node:edit - Edit a page
                                  node:delete - Delete a page
                                  site:stats - Site Status / stats
                                  site:items - Site items
                                  site:items-import - Import items (JOS /
                                  site.json)
                                  site:list-files - List site files
                                  site:search - Search site content
                                  site:theme - Change theme
                                  site:element - Add new Lit component to
                                  custom/src
                                  site:html - Full site as HTML
                                  site:md - Full site as Markdown
                                  site:schema - Full site as HAXElementSchema
                                  site:skeleton-export - Export site as
                                  skeleton template
                                  site:skeleton-install - Install skeleton
                                  template
                                  site:sync - Sync git repo
                                  site:rsync - Rsync site to remote/local
                                  directory
                                  site:surge - Publish site to Surge.sh
                                  site:netlify - Publish site to Netlify
                                  site:vercel - Publish site to Vercel
                                  setup:github-actions - Setup GitHub Actions
                                  deployment
                                  setup:gitlab-ci - Setup GitLab CI deployment
                                  recipe:read - Read recipe file
                                  recipe:play - Play recipe file
                                  issue:general - Issue: Submit an issue or
                                  suggestion
                                  issue:theme - Issue: Suggest custom theme
                                  

Options:
  --v                             Verbose output
  --debug                         Output for developers
  --format <char>                 Output format; json (default), yaml
  --path <char>                   where to perform operation
  --npm-client <char>             npm client to use (must be installed) npm,
                                  yarn, pnpm (default: "npm")
  --y                             yes to all questions
  --skip                          skip frills like animations
  --quiet                         remove console logging
  --auto                          yes to all questions, alias of y
  --no-i                          prevent interactions / sub-process, good for
                                  scripting
  --to-file <char>                redirect command output to a file
  --no-extras                     skip all extra / automatic command processing
  --root <char>                   root location to execute the command from
  --import-site <char>            URL of site to import
  --import-structure <char>       import method to use:
                                  pressbooksToSite
                                  elmslnToSite
                                  haxcmsToSite
                                  notionToSite
                                  gitbookToSite
                                  evolutionToSite
                                  ploneToSite
                                  wordpressPagesToSite
                                  drupalBookToSite
                                  htmlToSite
                                  docxToSite
  --name <char>                   name of the site (when creating a new one)
  --domain <char>                 published domain name
  --node-op <char>                node operation to perform
  --title-scrape <char>           CSS Selector for `title` in resource
  --content-scrape <char>         CSS Selector for `body` in resource
  --items-import <char>           import items from a file / site
  --recipe <char>                 path to recipe file
  --custom-theme-name <char>      custom theme name
  --custom-theme-template <char>  custom theme template (options: base,
                                  polaris-flex, polaris-sidebar)
  --skeleton-file <char>          path to skeleton JSON file
  --skeleton-machine-name <char>  skeleton machine name (installed template) to
                                  create a site from
  --search <char>                 search query text or simple selector
  --search-field <char>           comma-separated fields for text search
                                  (title,slug,description,tags,content,all)
  --search-case-sensitive         case-sensitive text search
  --search-limit <char>           max number of site search matches to return
  --search-selector               treat --search as a selector query (tag,
                                  tag[attr], tag[attr="value"], [attr])
  --search-mode <char>            search mode override (text or selector)
  --source <char>                 rsync source directory or remote path
  --destination <char>            rsync destination directory or remote path
  --exclude <char>                comma-separated patterns to exclude from rsync
  --dry-run                       perform rsync dry run
  --delete                        delete extraneous files from destination
  -V, --version                   output the version number
  --title <char>                  Title
  --content <char>                Page content
  --slug <char>                   Path (slug)
  --published <char>              Publishing status
  --tags <char>                   Tags
  --parent <char>                 Parent
  --order <char>                  Order
  --theme <char>                  Theme
  --hide-in-menu <char>           Hide in menu
  -h, --help                      display help for command
```

## @haxtheweb/create site --root . --help

```text
Usage: create-haxtheweb site [options] [action]

create or administer a HAXsite

Arguments:
  action                          Actions to perform on site include:
                                  start - Launch site in browser
                                  (http://localhost)
                                  serve - Launch site in development mode
                                  node:stats - Node Stats / data
                                  node:add - Add a new page
                                  node:edit - Edit a page
                                  node:delete - Delete a page
                                  site:stats - Site Status / stats
                                  site:items - Site items
                                  site:items-import - Import items (JOS /
                                  site.json)
                                  site:list-files - List site files
                                  site:search - Search site content
                                  site:theme - Change theme
                                  site:element - Add new Lit component to
                                  custom/src
                                  site:html - Full site as HTML
                                  site:md - Full site as Markdown
                                  site:schema - Full site as HAXElementSchema
                                  site:skeleton-export - Export site as
                                  skeleton template
                                  site:skeleton-install - Install skeleton
                                  template
                                  site:sync - Sync git repo
                                  site:rsync - Rsync site to remote/local
                                  directory
                                  site:surge - Publish site to Surge.sh
                                  site:netlify - Publish site to Netlify
                                  site:vercel - Publish site to Vercel
                                  setup:github-actions - Setup GitHub Actions
                                  deployment
                                  setup:gitlab-ci - Setup GitLab CI deployment
                                  recipe:read - Read recipe file
                                  recipe:play - Play recipe file
                                  issue:general - Issue: Submit an issue or
                                  suggestion
                                  issue:theme - Issue: Suggest custom theme
                                  

Options:
  --v                             Verbose output
  --debug                         Output for developers
  --format <char>                 Output format; json (default), yaml
  --path <char>                   where to perform operation
  --npm-client <char>             npm client to use (must be installed) npm,
                                  yarn, pnpm (default: "npm")
  --y                             yes to all questions
  --skip                          skip frills like animations
  --quiet                         remove console logging
  --auto                          yes to all questions, alias of y
  --no-i                          prevent interactions / sub-process, good for
                                  scripting
  --to-file <char>                redirect command output to a file
  --no-extras                     skip all extra / automatic command processing
  --root <char>                   root location to execute the command from
  --import-site <char>            URL of site to import
  --import-structure <char>       import method to use:
                                  pressbooksToSite
                                  elmslnToSite
                                  haxcmsToSite
                                  notionToSite
                                  gitbookToSite
                                  evolutionToSite
                                  ploneToSite
                                  wordpressPagesToSite
                                  drupalBookToSite
                                  htmlToSite
                                  docxToSite
  --name <char>                   name of the site (when creating a new one)
  --domain <char>                 published domain name
  --node-op <char>                node operation to perform
  --title-scrape <char>           CSS Selector for `title` in resource
  --content-scrape <char>         CSS Selector for `body` in resource
  --items-import <char>           import items from a file / site
  --recipe <char>                 path to recipe file
  --custom-theme-name <char>      custom theme name
  --custom-theme-template <char>  custom theme template (options: base,
                                  polaris-flex, polaris-sidebar)
  --skeleton-file <char>          path to skeleton JSON file
  --skeleton-machine-name <char>  skeleton machine name (installed template) to
                                  create a site from
  --search <char>                 search query text or simple selector
  --search-field <char>           comma-separated fields for text search
                                  (title,slug,description,tags,content,all)
  --search-case-sensitive         case-sensitive text search
  --search-limit <char>           max number of site search matches to return
  --search-selector               treat --search as a selector query (tag,
                                  tag[attr], tag[attr="value"], [attr])
  --search-mode <char>            search mode override (text or selector)
  --source <char>                 rsync source directory or remote path
  --destination <char>            rsync destination directory or remote path
  --exclude <char>                comma-separated patterns to exclude from rsync
  --dry-run                       perform rsync dry run
  --delete                        delete extraneous files from destination
  -V, --version                   output the version number
  --title <char>                  Title
  --content <char>                Page content
  --slug <char>                   Path (slug)
  --published <char>              Publishing status
  --tags <char>                   Tags
  --parent <char>                 Parent
  --order <char>                  Order
  --theme <char>                  Theme
  --hide-in-menu <char>           Hide in menu
  -h, --help                      display help for command
```

## Common safe examples

```bash
npx @haxtheweb/create site --root . site:items
npx @haxtheweb/create site --root . node:add --title "Page Title" --content "<h1>Page Title</h1><p>Starter content.</p>" --y
npx @haxtheweb/create site --root . site:search --search "keyword"
npx @haxtheweb/create site --root . site:html
npx @haxtheweb/create site --root . site:md
```
