# HAXcms LEARNING Context

Learned patterns and integration knowledge for WARP when working specifically with HAXcms sites and backends.

## HAXcms Site Integration Patterns

### Site Structure Learning

#### JSON Outline Schema Mastery:
- **Hierarchical Content**: `site.json` structure must reflect logical content organization
- **Parent-Child Relationships**: Proper nesting enables navigation features and breadcrumbs
- **Metadata Consistency**: Each item needs consistent `title`, `description`, `location` properties
- **Slug Management**: URL slugs should be descriptive, SEO-friendly, and maintain consistency

#### Effective site.json Patterns:
```json
{
  "version": "1.0.0",
  "title": "HAX Documentation",
  "description": "Comprehensive HAX ecosystem documentation",
  "license": "Apache-2.0",
  "metadata": {
    "site": {
      "name": "docs",
      "domain": "https://haxtheweb.org",
      "created": "1234567890",
      "updated": "1234567890"
    },
    "theme": {
      "element": "clean-one",
      "path": "@haxtheweb/clean-one/clean-one.js",
      "variables": {
        "--clean-one-accent-color": "var(--ddd-primary-13)"
      }
    }
  },
  "items": [
    {
      "title": "Getting Started",
      "id": "getting-started",
      "location": "pages/getting-started/index.html",
      "order": 0,
      "parent": null,
      "indent": 0,
      "slug": "getting-started"
    }
  ]
}
```

### Content Management Integration

#### HAX Editor Integration Learning:
- **Component Availability**: Editor shows only components available in current site context
- **Property Editing**: HAX schema determines what properties can be edited inline
- **Content Persistence**: Changes in HAX editor must properly update page files
- **Preview Accuracy**: HAX editor preview should match live site rendering

#### Content Authoring Best Practices:
- **Semantic Structure**: Use proper heading hierarchy (h1 → h2 → h3)
- **Component Usage**: Leverage HAX-capable components for rich, interactive content
- **Media Management**: Store assets in `files/` directory with logical organization
- **Accessibility**: Ensure content is accessible from initial authoring, not as afterthought

### Theme Integration Learning

#### HAXCMSLitElement Theme Development:
- **Class Hierarchy**: Custom themes should extend `HAXCMSLitElement` properly
- **DDD Integration**: Themes must use DDD design tokens for consistency
- **Build Requirements**: Always run `yarn run build` after theme modifications
- **Responsive Design**: Themes must work across all device sizes and orientations

#### Theme Configuration Patterns:
```javascript
// Effective theme base class usage
import { HAXCMSLitElement } from '@haxtheweb/haxcms-elements/lib/core/HAXCMSLitElement.js';
import { DDDSuper } from '@haxtheweb/d-d-d/d-d-d.js';

class MyCustomTheme extends DDDSuper(HAXCMSLitElement) {
  static get styles() {
    return [
      super.styles,
      css`
        :host {
          display: block;
          background-color: var(--ddd-theme-default-limestoneLight);
          color: var(--ddd-theme-default-coalyGray);
        }
      `
    ];
  }
}
```

## Backend Integration Learning

### PHP vs Node.js Backend Patterns:

#### HAXcms-PHP Learning:
- **File System**: Direct file system operations for content management
- **Performance**: Generally faster for file-heavy operations
- **Deployment**: Traditional LAMP stack deployment patterns
- **API Endpoints**: RESTful API design with consistent response formats

#### HAXcms-Node.js Learning:
- **Async Operations**: Better handling of concurrent requests
- **JavaScript Ecosystem**: Easier integration with JavaScript tooling
- **Modern Deployment**: Better suited for containerized environments
- **Real-time Features**: WebSocket support for live editing features

### API Integration Patterns:

#### Content Management API:
```javascript
// Effective API usage patterns
const siteData = await fetch('/api/site.json').then(r => r.json());
const pageContent = await fetch('/api/pages/page-slug').then(r => r.json());

// Proper error handling
try {
  const response = await fetch('/api/updatePage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, slug })
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
} catch (error) {
  console.error('Update failed:', error);
}
```

## Educational Content Integration

### OER Schema Implementation Learning:

#### Educational Metadata Patterns:
```html
<!-- Effective OER Schema integration -->
<educational-content 
  learning-objective="Students will understand HAX ecosystem architecture"
  educational-use="instruction" 
  intended-end-user-role="learner"
  educational-level="intermediate">
  <h2>HAX Architecture Overview</h2>
  <p>Content with educational context...</p>
</educational-content>
```

#### Pedagogical Content Structure:
- **Learning Objectives**: Clear, measurable objectives for each content section
- **Assessment Integration**: Formative assessment embedded throughout content
- **Accessibility**: Universal Design for Learning (UDL) principles applied
- **Progressive Disclosure**: Information revealed as learners need it

### Educational Component Usage:

#### Interactive Learning Elements:
- **Question Sets**: Multiple choice, true/false, short answer components
- **Self-Check Activities**: Non-graded activities for knowledge verification  
- **Timeline Components**: Chronological content presentation
- **Stop Notes**: Reflection prompts and key concept highlights

## Performance Optimization Learning

### Site Performance Patterns:

#### Content Optimization:
- **Image Optimization**: Proper image sizing and format selection
- **Lazy Loading**: Components and content loaded as needed
- **Caching Strategy**: Leverage HAXcms built-in caching mechanisms
- **Bundle Optimization**: Minimize JavaScript payload for faster initial loads

#### Database vs File System:
- **File-Based Benefits**: Simpler deployment, better version control integration
- **Performance Considerations**: File system operations vs database queries
- **Scalability Patterns**: How to scale file-based content management
- **Backup Strategies**: Version control as content backup system

### Build Optimization Learning:

#### Site Generation Performance:
```bash
# Effective site generation patterns
hax site mysite --y --custom-theme-name my-theme
cd mysite

# Optimize build process
hax serve --y --no-i  # Development server
hax audit            # Performance and accessibility audit
```

## Cross-Repository Integration Learning

### HAXcms ↔ Webcomponents Integration:
- **Component Registry**: Site must align with available webcomponents
- **Version Compatibility**: HAXcms version must match webcomponent versions
- **Theme Dependencies**: Custom themes may depend on specific components
- **Feature Availability**: Site features depend on backend and component capabilities

### HAXcms ↔ Create (CLI) Integration:
- **Site Generation**: CLI generates sites with proper HAXcms structure
- **Theme Templates**: CLI templates must stay current with HAXcms patterns
- **Content Import**: CLI import features must handle various content sources
- **Maintenance Commands**: CLI provides site maintenance and update commands

### HAXcms ↔ Open APIs Integration:
- **Content Conversion**: Open APIs services convert external content to HAXcms format
- **Analysis Services**: Content analysis and optimization through open APIs
- **Import Pipelines**: Automated content import from various sources
- **Enhancement Services**: AI-powered content enhancement capabilities

## Troubleshooting Patterns

### Common HAXcms Site Issues:

#### Site Structure Problems:
1. **Invalid JSON Outline Schema**: Use JSON schema validator for site.json
2. **Broken Navigation**: Verify parent-child relationships and order values
3. **Missing Pages**: Ensure page files exist for all site.json entries
4. **Theme Loading Issues**: Check theme path and component availability

#### Content Management Issues:
1. **HAX Editor Problems**: Verify component registry and HAX schema implementation
2. **File Upload Issues**: Check file permissions and storage directory configuration
3. **Preview Mismatches**: Ensure theme CSS matches HAX editor styles
4. **Performance Problems**: Audit component usage and media optimization

#### Backend Integration Issues:
1. **API Failures**: Check server configuration and endpoint availability
2. **Authentication Problems**: Verify user permissions and session management
3. **File System Issues**: Check directory permissions and disk space
4. **Version Conflicts**: Ensure backend and frontend version compatibility

### Deployment Learning:

#### Effective Deployment Patterns:
```bash
# Static site deployment
hax site build --y        # Generate static build
rsync -av dist/ server:/path/to/site/

# Dynamic HAXcms deployment  
# Deploy backend (PHP or Node.js)
# Configure web server (Apache/Nginx)
# Set up file permissions
# Configure SSL/TLS
```

#### Security Considerations:
- **File Permissions**: Proper permissions for content directories
- **API Security**: Authentication and authorization for content management
- **Input Validation**: Sanitize all user-generated content
- **SSL/TLS**: HTTPS for all content management operations

## Future Learning Areas

### Emerging HAXcms Patterns:
- **Headless CMS**: HAXcms as content source for external applications
- **Multi-site Management**: Managing multiple HAXcms instances efficiently
- **Advanced Theming**: Dynamic theme switching and customization
- **Real-time Collaboration**: Multi-user content editing capabilities

### Integration Evolution:
- **AI Content Generation**: Leveraging AI for content creation and enhancement
- **Advanced Analytics**: Detailed usage analytics and learning insights
- **Mobile-First Design**: Optimizing HAXcms for mobile-first experiences
- **Accessibility Enhancement**: Beyond WCAG compliance to universal usability

---

*This document captures HAXcms-specific learning from WARP interactions. Update as new patterns emerge in HAXcms development and deployment.*