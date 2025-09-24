#!/bin/bash

# HAX Ecosystem Onboarding Script for Warp
# Takes someone from 0 to contributor using Warp as the primary development interface
# Version: 1.0
# Author: HAX Team

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_BASE_DIR="$HOME/Documents/git/haxtheweb"
GITHUB_ORG="haxtheweb"

# Repository list based on the training data analysis
declare -A REPOSITORIES=(
    # Core HAX Repositories
    ["webcomponents"]="The heart of HAX: 250+ LitElement-based web components, themes, and DDD design system"
    ["create"]="HAX CLI tool (@haxtheweb/create) for scaffolding components, sites, and managing workflow"
    ["haxcms-php"]="PHP backend implementation for content management and server-side rendering"
    ["haxcms-nodejs"]="Node.js backend implementation offering same capabilities as PHP version"
    ["desktop"]="Electron-based desktop application providing local development environment"
    
    # Supporting Repositories
    ["hax11ty"]="Integration layer bridging HAX components with Eleventy static site generator"
    ["json-outline-schema"]="JSON schema used by HAXcms for content structure and navigation"
    ["hax-schema"]="HAX property schemas defining web component integration with authoring interface"
    ["open-apis"]="Microservice APIs and shared infrastructure (https://open-apis.hax.cloud/)"
    ["docs"]="Official HAX documentation site built as HAXcms site"
    ["issues"]="Unified issue tracking repository for entire HAX ecosystem"
    
    # Additional Development Tools
    ["psucdn"]="CDN and asset management"
    ["screenshotUrl"]="Screenshot generation services"
    ["edtechjoker"]="Educational technology blog and resources"
    
    # AI and Training Data (Note: ai-site-training-data is private)
    ["HAXiam"]="AI assistant integration"
    
    # Specialized Projects
    ["rpg-me"]="Gamification elements and RPG-style interactions"
    ["art"]="Art-focused educational components and themes"
)

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${PURPLE}================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}================================${NC}\n"
}

# Function to check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    # Check if running in Warp
    if [[ -z "$WARP_SESSION" ]]; then
        print_warning "This script is optimized for Warp Terminal. Some features may not work optimally in other terminals."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Running in Warp Terminal"
    fi
    
    # Check for required tools
    local required_tools=("git" "node" "npm" "curl")
    local missing_tools=()
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        print_error "Missing required tools: ${missing_tools[*]}"
        print_status "Please install the missing tools and re-run this script"
        exit 1
    fi
    
    print_success "All required tools are installed"
    
    # Check Node.js version
    local node_version=$(node --version | sed 's/v//')
    local required_node="18.0.0"
    
    if [[ $(echo "$node_version $required_node" | tr ' ' '\n' | sort -V | head -n1) != "$required_node" ]]; then
        print_warning "Node.js version $node_version detected. HAX ecosystem works best with Node.js 18+."
    else
        print_success "Node.js version $node_version is compatible"
    fi
}

# Function to setup directory structure
setup_directories() {
    print_header "Setting Up Directory Structure"
    
    # Get base directory from user
    echo "Where would you like to install the HAX ecosystem?"
    echo "Default: $DEFAULT_BASE_DIR"
    read -p "Enter path (or press Enter for default): " BASE_DIR
    
    BASE_DIR=${BASE_DIR:-$DEFAULT_BASE_DIR}
    
    print_status "Creating base directory: $BASE_DIR"
    mkdir -p "$BASE_DIR"
    cd "$BASE_DIR"
    
    print_success "Directory structure ready at: $BASE_DIR"
    
    # Export for use in other functions
    export HAX_BASE_DIR="$BASE_DIR"
}

# Function to clone repositories
clone_repositories() {
    print_header "Cloning HAX Ecosystem Repositories"
    
    cd "$HAX_BASE_DIR"
    
    # Check if user has GitHub CLI for better auth
    if command -v gh &> /dev/null; then
        print_success "GitHub CLI detected - using authenticated cloning"
        local clone_cmd="gh repo clone"
    else
        print_status "Using HTTPS cloning (GitHub CLI not detected)"
        local clone_cmd="git clone https://github.com"
    fi
    
    # Ask user which repos they want to clone
    echo "Which repositories would you like to clone?"
    echo "Recommended for beginners: webcomponents, create, docs, issues"
    echo ""
    echo "Available repositories:"
    
    local counter=1
    local repo_list=()
    
    for repo in "${!REPOSITORIES[@]}"; do
        echo "  $counter) $repo - ${REPOSITORIES[$repo]}"
        repo_list+=("$repo")
        ((counter++))
    done
    
    echo ""
    echo "Enter your selection:"
    echo "  'all' - Clone all repositories"
    echo "  'core' - Clone core repositories (webcomponents, create, docs, issues)"
    echo "  '1,2,3' - Clone specific repositories by number"
    echo "  'skip' - Skip repository cloning"
    
    read -p "Selection: " selection
    
    local repos_to_clone=()
    
    case "$selection" in
        "all")
            repos_to_clone=("${repo_list[@]}")
            ;;
        "core")
            repos_to_clone=("webcomponents" "create" "docs" "issues")
            ;;
        "skip")
            print_status "Skipping repository cloning"
            return
            ;;
        *)
            # Parse comma-separated numbers
            IFS=',' read -ra NUMBERS <<< "$selection"
            for num in "${NUMBERS[@]}"; do
                num=$(echo "$num" | xargs) # trim whitespace
                if [[ "$num" =~ ^[0-9]+$ ]] && [[ "$num" -ge 1 ]] && [[ "$num" -le ${#repo_list[@]} ]]; then
                    repos_to_clone+=("${repo_list[$((num-1))]}")
                fi
            done
            ;;
    esac
    
    if [[ ${#repos_to_clone[@]} -eq 0 ]]; then
        print_warning "No valid repositories selected"
        return
    fi
    
    # Clone selected repositories
    for repo in "${repos_to_clone[@]}"; do
        print_status "Cloning $repo..."
        
        if [[ -d "$repo" ]]; then
            print_warning "$repo already exists, skipping"
            continue
        fi
        
        if command -v gh &> /dev/null; then
            if gh repo clone "$GITHUB_ORG/$repo" "$repo"; then
                print_success "Successfully cloned $repo"
            else
                print_error "Failed to clone $repo"
            fi
        else
            if git clone "https://github.com/$GITHUB_ORG/$repo.git" "$repo"; then
                print_success "Successfully cloned $repo"
            else
                print_error "Failed to clone $repo"
            fi
        fi
    done
}

# Function to setup HAX CLI
setup_hax_cli() {
    print_header "Setting Up HAX CLI"
    
    print_status "Installing @haxtheweb/create globally..."
    
    if npm install -g @haxtheweb/create; then
        print_success "HAX CLI installed successfully"
        
        # Test installation
        if command -v hax &> /dev/null; then
            local version=$(hax --version 2>/dev/null || echo "unknown")
            print_success "HAX CLI version: $version"
        else
            print_error "HAX CLI installation failed or not in PATH"
        fi
    else
        print_error "Failed to install HAX CLI"
        print_status "You can install it manually later with: npm install -g @haxtheweb/create"
    fi
}

# Function to create Warp configuration for HAX development
setup_warp_config() {
    print_header "Configuring Warp for HAX Development"
    
    local warp_config_dir="$HOME/.warp"
    local rules_dir="$warp_config_dir/rules"
    
    mkdir -p "$rules_dir"
    
    # Create HAX-specific Warp rules
    cat > "$rules_dir/hax-development.md" << 'EOF'
# HAX Ecosystem Development Rules

## Environment Setup
- Always start new terminals in `~/Documents/git/haxtheweb/` directory
- Use local HAX CLI commands instead of npx (run `hax` not `npx @haxtheweb/create`)
- When running HAX commands, use `--y`, `--no-i`, and `--auto` flags to prevent interactive interruptions

## HAX CLI Commands
- Create web components: `hax webcomponent my-element --y`
- Create HAX sites: `hax site mysite --y`
- Start development server: `hax serve`
- Run DDD compliance audit: `hax audit`
- Update HAX CLI: `hax update`

## Web Component Development
- Use pure JavaScript with LitElement (NO TypeScript compilation)
- Use single quotes and avoid semicolons where possible
- Use `globalThis` instead of `window` for global references
- Import from pre-compiled JavaScript distributions for third-party libraries
- Never use optional chaining syntax (`?.`) due to Polymer parser issues

## Design System
- Use DDD design system located at `elements/d-d-d` for consistency
- Leverage DDD for fonts, colors, padding, spacing, margins
- SimpleColors system is legacy - use DDD when possible

## Content Structure
- HAXcms sites use `site.json` for page structure (JSON outline schema)
- Content files go in `pages/` directory
- Assets go in `files/` directory
- Metadata should include OER Schema parameters for educational content

## Build Process
- Run `yarn run build` after changes to HAXCMSLitElement themes
- Don't manually edit `custom-elements.json` - it's auto-generated
- Traditional build commands are not used in this monorepo

## Accessibility
- Always audit for accessibility enhancements when working on components
- Ensure proper ARIA labels, alt text, and semantic markup
- Test with screen readers and keyboard navigation

## Issues and Development
- Check unified issue queue at `~/Documents/git/haxtheweb/issues` for any repository work
- Follow HAX community pillars: Accessible, Extensible, Free/Open, Efficient, Platform Agnostic, Remixable, Sustainable
EOF

    print_success "Created HAX development rules for Warp"
    
    # Create project-specific WARP.md files
    cd "$HAX_BASE_DIR"
    
    for dir in */; do
        if [[ -d "$dir" && -d "$dir/.git" ]]; then
            local repo_name=$(basename "$dir")
            
            if [[ ! -f "$dir/WARP.md" ]]; then
                print_status "Creating WARP.md for $repo_name"
                
                cat > "$dir/WARP.md" << EOF
# HAX $repo_name Development

This repository is part of the HAX ecosystem. Follow HAX development guidelines:

## Quick Start
- Use \`hax\` CLI commands for scaffolding and development
- Follow unbundled JavaScript approach (no TypeScript compilation)
- Use DDD design system for consistency
- Ensure accessibility compliance

## Common Commands
- Start development: \`hax serve\`
- Build project: \`yarn run build\`
- Audit DDD compliance: \`hax audit\`

## Repository Purpose
${REPOSITORIES[$repo_name]:-"Part of the HAX ecosystem"}

## Getting Help
- Check issues at: ../issues
- Documentation: ../docs
- HAX CLI help: \`hax --help\`
EOF
            fi
        fi
    done
    
    print_success "Project WARP.md files created"
}

# Function to setup development environment
setup_dev_environment() {
    print_header "Setting Up Development Environment"
    
    cd "$HAX_BASE_DIR"
    
    # Setup webcomponents repo if it exists
    if [[ -d "webcomponents" ]]; then
        print_status "Setting up webcomponents repository..."
        cd webcomponents
        
        if [[ -f "package.json" ]]; then
            print_status "Installing dependencies..."
            if npm install; then
                print_success "Dependencies installed for webcomponents"
            else
                print_warning "Failed to install dependencies for webcomponents"
            fi
        fi
        
        cd "$HAX_BASE_DIR"
    fi
    
    # Setup create repo if it exists
    if [[ -d "create" ]]; then
        print_status "Setting up create repository..."
        cd create
        
        if [[ -f "package.json" ]]; then
            print_status "Installing dependencies..."
            if npm install; then
                print_success "Dependencies installed for create"
                
                # Link for local development
                print_status "Linking for local development..."
                npm link
            else
                print_warning "Failed to install dependencies for create"
            fi
        fi
        
        cd "$HAX_BASE_DIR"
    fi
}

# Function to create helpful aliases and shortcuts
create_shortcuts() {
    print_header "Creating Development Shortcuts"
    
    local shell_config=""
    
    # Detect shell and config file
    if [[ "$SHELL" == *"zsh"* ]]; then
        shell_config="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        shell_config="$HOME/.bashrc"
    else
        print_warning "Unknown shell, skipping alias creation"
        return
    fi
    
    print_status "Adding HAX aliases to $shell_config"
    
    # Create HAX aliases section
    cat >> "$shell_config" << EOF

# HAX Development Aliases (added by hax-onboarding.sh)
alias haxdir='cd $HAX_BASE_DIR'
alias haxwc='cd $HAX_BASE_DIR/webcomponents'
alias haxcreate='cd $HAX_BASE_DIR/create'
alias haxdocs='cd $HAX_BASE_DIR/docs'
alias haxissues='cd $HAX_BASE_DIR/issues'
alias haxserve='hax serve --y --no-i --auto'
alias haxaudit='hax audit'
alias haxbuild='yarn run build'

# HAX environment variable
export HAX_DEV_PATH="$HAX_BASE_DIR"

EOF
    
    print_success "HAX development aliases added to $shell_config"
    print_status "Run 'source $shell_config' or restart your terminal to use aliases"
}

# Function to generate onboarding summary
generate_summary() {
    print_header "Onboarding Summary"
    
    cat << EOF
🎉 HAX Ecosystem Onboarding Complete!

## What's Been Set Up:
✅ HAX ecosystem repositories cloned to: $HAX_BASE_DIR
✅ HAX CLI (@haxtheweb/create) installed globally
✅ Warp configuration optimized for HAX development
✅ Project WARP.md files created for each repository
✅ Development shortcuts and aliases configured

## Quick Start Commands:
- Navigate to HAX directory: haxdir
- Start development server: hax serve
- Create new web component: hax webcomponent my-element --y
- Create new site: hax site mysite --y
- Audit DDD compliance: hax audit

## Development Workflow:
1. Use Warp's agent to ask questions about the codebase
2. Create components with: hax webcomponent [name] --y
3. Test components with: hax serve
4. Build changes with: yarn run build (when needed)
5. Check issues at: $HAX_BASE_DIR/issues

## Key Warp Features for HAX:
- Codebase Context: Warp has indexed your HAX repositories
- Code Review: Use Warp's diff review for changes
- Project Rules: HAX-specific rules are configured
- Agent Assistance: Ask Warp agents about HAX development

## Next Steps:
1. Restart your terminal or run: source ~/.zshrc (or ~/.bashrc)
2. Try: haxdir && hax --help
3. Explore the webcomponents directory: haxwc
4. Check out the docs: haxdocs
5. Create your first component!

## Getting Help:
- HAX CLI help: hax --help
- Documentation: $HAX_BASE_DIR/docs
- Issues: $HAX_BASE_DIR/issues
- Ask Warp agents: "How do I create a HAX web component?"

Happy coding with HAX! 🚀
EOF
}

# Function to create initial Warp agent prompts
create_warp_prompts() {
    print_header "Creating Helpful Warp Prompts"
    
    cat > "$HAX_BASE_DIR/WARP_PROMPTS.md" << 'EOF'
# Helpful Warp Agent Prompts for HAX Development

## Getting Started
- "Show me how to create a new HAX web component"
- "What are the key files I should know about in the HAX ecosystem?"
- "Explain the HAX development workflow"
- "How do I use the DDD design system in my components?"

## Component Development
- "Create a new LitElement web component following HAX standards"
- "Add HAX schema properties to make my component HAX-capable"
- "Implement accessibility features in my web component"
- "Convert this component to use DDD design tokens"

## Site Development
- "Create a new HAXcms site with custom theme"
- "Add educational content with proper OER schema metadata"
- "Implement responsive design using DDD system"
- "Create interactive learning components"

## Debugging & Troubleshooting
- "Help me debug this HAX component that's not rendering properly"
- "Why isn't my component appearing in the HAX editor?"
- "Fix accessibility issues in my component"
- "Resolve build errors in the webcomponents monorepo"

## Code Review & Quality
- "Review this component for HAX best practices"
- "Audit this code for accessibility compliance"
- "Optimize this component for performance"
- "Ensure this follows HAX coding standards"

## Documentation & Learning
- "Explain how HAX schema works"
- "What are the HAX community pillars and how do they apply to development?"
- "Show me examples of well-structured educational components"
- "How does the HAX ecosystem relate to web standards?"

## Advanced Tasks
- "Create a custom HAX theme following the architecture patterns"
- "Implement a complex educational interaction component"
- "Add analytics integration following HAX patterns"
- "Create a component library following HAX standards"

## Tips for Better Prompts
1. Be specific about what you're trying to accomplish
2. Mention if you're working on educational content
3. Reference HAX standards and best practices
4. Include context about accessibility requirements
5. Mention which repository you're working in

## Example Detailed Prompt
Instead of: "Make a button component"
Try: "Create a HAX-capable button web component using LitElement that follows DDD design system standards, includes proper accessibility attributes, and can be used in educational content. The button should support different variants and be configurable through the HAX editor."
EOF

    print_success "Created helpful Warp prompts guide at: $HAX_BASE_DIR/WARP_PROMPTS.md"
}

# Main execution function
main() {
    clear
    
    cat << 'EOF'
    __  __  ___   _  __   ____        __                          ___              
   / / / / /   | | |/ /  / __ \____  / /_  ____  ____ __________/ (_)___  ____ _  
  / /_/ / / /| | |   /  / / / / __ \/ __ \/ __ \/ __ `/ ___/ __  / / __ \/ __ `/  
 / __  / / ___ |/   |  / /_/ / / / / /_/ / /_/ / /_/ / /  / /_/ / / / / / /_/ /   
/_/ /_/ /_/  |_/_/|_|  \____/_/ /_/_.___/\____/\__,_/_/   \__,_/_/_/ /_/\__, /    
                                                                      /____/     

Welcome to the HAX Ecosystem Onboarding Script!

This script will set up everything you need to start contributing to HAX
using Warp as your primary development interface.

EOF
    
    read -p "Press Enter to continue..."
    
    # Run setup steps
    check_prerequisites
    setup_directories
    clone_repositories
    setup_hax_cli
    setup_dev_environment
    setup_warp_config
    create_shortcuts
    create_warp_prompts
    
    # Final summary
    generate_summary
    
    print_success "\n🎉 Onboarding complete! Welcome to the HAX ecosystem!"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi