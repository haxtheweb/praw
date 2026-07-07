---
name: hax-ecosystem
description: >
  Master skill for the entire HAX (Headless Authoring eXperience) ecosystem.
  Use when working on any HAX project — web components, sites, themes, backends,
  or ecosystem tooling. This skill routes to more specific skills automatically.
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  tags: [hax, ecosystem, webcomponents, haxcms, design-system, onboarding, rules, issues]
---

# HAX Ecosystem

The HAX ecosystem is a comprehensive web development platform for rapid creation of accessible, performant web components and static sites. This skill provides the ecosystem overview and routes to specialized skills for specific tasks.

## When to Use

- Any task involving a HAX project, repository, or convention
- Scaffolding web components or HAXcms sites
- Working with the DDD design system or SimpleColors
- Managing HAX ecosystem rules or conventions
- Analyzing GitHub issues across HAX repositories
- Onboarding a new developer to the HAX ecosystem

## Ecosystem Overview

The HAX ecosystem consists of multiple interconnected repositories:

- **`webcomponents`** — 250+ LitElement-based web components, themes, and the DDD design system
- **`create` (@haxtheweb/create)** — HAX CLI for scaffolding and workflow management
- **`haxcms-php` / `haxcms-nodejs`** — Content management backends (PHP and Node.js)
- **`desktop`** — Electron-based local development environment
- **`hax11ty`** — Eleventy integration for HAX components
- **`json-outline-schema`** — Content structure and navigation schemas
- **`hax-schema`** — HAX property schemas for editor integration
- **`open-apis`** — Microservice APIs and shared infrastructure
- **`docs`** — Official HAX documentation site
- **`issues`** — Unified issue tracking repository

## Community Pillars

HAX is built on community pillars that guide all development:

- **Accessible** — Maximizes accessibility while removing knowledge required to maintain standards (WCAG 2.0 AA)
- **Extensible** — Built for sustainable extension through web standards, microservices, modular architecture
- **Free and Open** — Open community embracing 5Rs of OER (Retain, Reuse, Revise, Remix, Redistribute)
- **Efficient** — Optimized for performance through web standards, lazy loading, offline capability
- **Platform Agnostic** — Works anywhere: standalone HAXsites, HAXcms, static pages, existing CMS platforms
- **Remixable** — Maximizes remix-ability through modular design, open licensing, semantic content structures
- **Sustainable** — Environmental, technological, and community sustainability

## Specialized Skills

For specific tasks, use the more focused skills in this package:

- `hax-webcomponent-dev` — Web component development with LitElement, DDD, HAXSchema
- `hax-site-building` — HAXcms site creation, theme management, JSON Outline Schema
- `hax-design-system` — DDD design system application and SimpleColors migration
- `hax-ecosystem-onboarding` — New developer setup, environment configuration, scaffolding
- `hax-rule-management` — PRAW rule management, validation, export
- `hax-issue-analysis` — GitHub issue fetching, analysis, reporting
- `hax-claudehax` — Operate HAX sites via the ClaudeHAX plugin in Claude Code
- `hax-openstax2hax` — Convert OpenStax books into HAX sites via the openstax2hax plugin

## Core Conventions

- Start all shells in `~/Documents/git/haxtheweb/`
- Use `globalThis` instead of `window`
- Do not use optional chaining (`?.`) — Polymer parser incompatibility
- No TypeScript — pure JavaScript with LitElement
- Use single quotes, avoid semicolons where possible
- Always check issues against `~/Documents/git/haxtheweb/issues`
- Do not run the ubiquity script under any circumstances
- Do not run a build at the top of the monorepo

## References

- For webcomponent details: `../../skills/hax-webcomponent-dev/SKILL.md`
- For site building details: `../../skills/hax-site-building/SKILL.md`
- For design system details: `../../skills/hax-design-system/SKILL.md`
- For onboarding details: `../../skills/hax-ecosystem-onboarding/SKILL.md`
- For rule management details: `../../skills/hax-rule-management/SKILL.md`
- For issue analysis details: `../../skills/hax-issue-analysis/SKILL.md`
- For openstax2hax details: `../../skills/hax-openstax2hax/SKILL.md`
