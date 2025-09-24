# PRAW - HAX Ecosystem Warp Rules

**PRAW** (Warp spelled backwards) is a repository containing comprehensive Warp AI agent rules for the HAX ecosystem. These rules codify years of development experience, best practices, and conventions to help Warp users work more effectively with HAX projects.

## What is this?

This repository contains `WARP.md` files that define how Warp's AI agents should behave when working with HAX ecosystem projects. These rules ensure consistency, quality, and proper integration across all HAX projects and web components.

## How to Use These Rules

### For Individual Projects

1. **Copy the main WARP.md** to your HAX project root:
   ```bash
   cp WARP.md /path/to/your/hax-project/
   ```

2. **Use specialized rules** by copying relevant subdirectory WARP.md files:
   ```bash
   cp webcomponents/WARP.md /path/to/your/project/elements/
   cp haxcms/WARP.md /path/to/your/haxcms-site/
   ```

### For the Entire HAX Ecosystem

If you're working across multiple HAX repositories, you can:

1. **Clone this repo** to your local HAX development area:
   ```bash
   cd ~/Documents/git/haxtheweb/
   git clone https://github.com/haxtheweb/praw.git
   ```

2. **Symlink the main WARP.md** to your primary working directories:
   ```bash
   ln -s ~/Documents/git/haxtheweb/praw/WARP.md ~/Documents/git/haxtheweb/webcomponents/
   ```

3. **Let Warp automatically detect** the rules when working in HAX directories

## Rule Categories

### 🏗️ Architecture & File Structure
- HAXcms site organization (`docs/`, `files/`, `pages/`)
- Web component registry system
- Reserved routing patterns

### 🎨 Design System Standards  
- DDD (primary design system) usage guidelines
- SimpleColors (legacy) integration
- Consistent styling approaches

### 🧩 Web Component Development
- HAX capability implementation
- Accessibility audit procedures
- JavaScript coding standards
- Educational content creation

### ⚙️ Build & Development Workflow
- Command usage patterns
- Version control integration
- Testing philosophy
- Tool configuration

### 📝 Content Creation Guidelines
- HAX site content authoring
- Documentation standards
- Quality assurance procedures

## Contributing

This repository evolves with the HAX ecosystem. To contribute:

1. **Test new rules** in your local development environment
2. **Submit PRs** with well-documented rule additions or modifications
3. **Provide context** for why specific rules exist
4. **Update examples** to reflect current best practices

## Rule Precedence

When using these rules, Warp follows this precedence order:
1. **Subdirectory WARP.md** (most specific)
2. **Root project WARP.md** 
3. **Global Warp rules** (least specific)

This ensures project-specific needs take priority while maintaining ecosystem consistency.

## Benefits

Using these rules provides:

- ✅ **Consistency** across HAX projects
- 🚀 **Faster development** with established patterns
- 🛡️ **Quality assurance** through automated checks
- 🎯 **Focused AI assistance** tailored to HAX conventions
- 📚 **Knowledge sharing** across the HAX community

## Maintenance

These rules are actively maintained by the HAX core team and community contributors. They reflect current best practices and are updated as the ecosystem evolves.

---

**Made with ❤️ by the HAX Community**

*PRAW ensures that every Warp user working with HAX gets the benefit of collective ecosystem knowledge and established best practices.*