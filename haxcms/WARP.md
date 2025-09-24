# HAXcms Site Development Rules

These rules apply specifically when working with HAXcms sites and their structure.

## Site Architecture

### Directory Structure
- **`docs/`** - Contains all site documentation and content
- **`files/`** - Static assets (images, videos, PDFs, etc.)
- **`pages/`** - Individual page HTML content files
- **`site.json`** - Site structure and metadata in JSON Outline Schema format
- **`manifest.json`** - PWA manifest for site configuration

### Reserved Routes
- **`x/`** prefix is reserved for internal HAXcms functionality
- **`x/search`** - Built-in search functionality
- **`x/tags`** - Tag-based content organization
- **`x/manifest`** - Site manifest endpoints
- Do not create pages or routes that conflict with these patterns

## Site Configuration

### site.json Structure
- **`metadata.site.name`** - Must align exactly with the folder name
- **`metadata.site.description`** - Clear, concise site description
- **`items`** - Page structure following JSON Outline Schema
- **`metadata.theme`** - Theme configuration and settings
- Maintain proper JSON Outline Schema compliance for page hierarchy

### Theme Integration
- Use HAXcms theme inheritance patterns
- Leverage HAXCMSLitElement for custom theme components
- Apply DDD design system tokens consistently across themes
- Ensure responsive design across all device sizes
- Test theme compatibility with core HAX components

## Content Creation

### Page Content Guidelines
- Use HAX-capable web components for rich content
- Apply DDD attributes for consistent spacing and typography
- Include engaging visual elements (videos, interactive components)
- Ensure all content is accessible via HAX editor
- Structure content with semantic HTML elements

### Educational Content Standards
- Apply OER Schema metadata where applicable
- Structure content to support pedagogical objectives
- Include proper learning resource identification
- Consider diverse learning styles in content presentation
- Maintain comprehensive ecosystem context in documentation

### Media and Assets
- Store all media files in `files/` directory
- Use appropriate file formats for web delivery
- Optimize images and videos for web performance
- Include alt text and captions for accessibility
- Organize assets with logical folder structure

## Development Workflow

### Content Management
- Edit content through HAX editor interface when possible
- Maintain JSON Outline Schema compliance in site.json
- Use proper page slug naming conventions (kebab-case)
- Ensure page titles and descriptions are meaningful

### Build Process
- Run `yarn run build` after theme modifications
- Do not manually edit generated manifest files
- Use HAX CLI tools for site operations
- Test site functionality after major changes

### Version Control
- Include all site files in version control
- Use meaningful commit messages for content changes
- Track both content and configuration changes
- Consider using HAX's built-in versioning features

## Site Quality Standards

### Performance
- Optimize for fast loading times
- Use lazy loading for heavy content
- Minimize external dependencies
- Implement proper caching strategies

### Accessibility
- Ensure proper heading hierarchy
- Include skip navigation links
- Test with screen readers
- Provide keyboard navigation support
- Maintain color contrast standards

### SEO and Discoverability
- Include proper meta descriptions
- Use semantic page structure
- Implement structured data where applicable
- Ensure proper internal linking
- Include sitemap generation

### Content Standards
- Maintain consistent writing style
- Include proper citations and references
- Ensure content is factually accurate
- Update outdated information regularly
- Consider multilingual support needs

## Integration Guidelines

### HAX Editor Integration
- Test all content in HAX editor environment
- Verify component rendering and editing
- Ensure proper component property interfaces
- Test content export and import functionality

### API Integration
- Follow HAXcms API conventions
- Implement proper error handling
- Use established endpoint patterns
- Maintain API versioning compatibility

### External Services
- Configure analytics and tracking properly
- Implement proper authentication flows
- Handle external API failures gracefully
- Maintain user privacy standards

---

*These rules ensure HAXcms sites maintain consistency, quality, and proper integration with the broader HAX ecosystem.*