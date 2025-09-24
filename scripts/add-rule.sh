#!/bin/bash

# HAX PRAW Rule Management System
# Script to add new rules to RULES.md

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RULES_FILE="/home/bto108a/Documents/git/haxtheweb/praw/RULES.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRAW_DIR="$(dirname "$SCRIPT_DIR")"

# Helper functions
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}      HAX PRAW Rule Management System${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

generate_rule_id() {
    # Generate a UUID-like string for new rules
    python3 -c "import uuid; print(str(uuid.uuid4()).replace('-', '')[:22])"
}

validate_category() {
    local category="$1"
    local valid_categories=(
        "architecture"
        "design-system" 
        "webcomponent"
        "build-workflow"
        "documentation"
        "project-specific"
    )
    
    for valid in "${valid_categories[@]}"; do
        if [[ "$category" == "$valid" ]]; then
            return 0
        fi
    done
    return 1
}

get_category_emoji() {
    case "$1" in
        "architecture") echo "🏗️" ;;
        "design-system") echo "🎨" ;;
        "webcomponent") echo "🧩" ;;
        "build-workflow") echo "⚙️" ;;
        "documentation") echo "📝" ;;
        "project-specific") echo "🗂️" ;;
        *) echo "📋" ;;
    esac
}

get_category_title() {
    case "$1" in
        "architecture") echo "Architecture & File Structure Rules" ;;
        "design-system") echo "Design System Standards" ;;
        "webcomponent") echo "Web Component Development" ;;
        "build-workflow") echo "Build & Development Workflow" ;;
        "documentation") echo "Documentation Standards" ;;
        "project-specific") echo "Project-Specific Rules" ;;
        *) echo "General Rules" ;;
    esac
}

add_rule_to_file() {
    local category="$1"
    local title="$2"
    local content="$3"
    local rule_id="$4"
    
    local emoji=$(get_category_emoji "$category")
    local category_title=$(get_category_title "$category")
    
    # Create the rule entry
    local rule_entry="
### $title
- **Rule ID**: \`$rule_id\`
- **Content**: $content
"
    
    # Check if category section exists
    if grep -q "## $emoji $category_title" "$RULES_FILE"; then
        # Add to existing category (before the next ## section or end of file)
        local temp_file=$(mktemp)
        local in_category=false
        local added=false
        
        while IFS= read -r line; do
            if [[ "$line" == "## $emoji $category_title" ]]; then
                in_category=true
                echo "$line" >> "$temp_file"
            elif [[ "$line" =~ ^##[[:space:]] ]] && [[ "$in_category" == true ]]; then
                # Found next category, add rule before it
                echo "$rule_entry" >> "$temp_file"
                echo "$line" >> "$temp_file"
                in_category=false
                added=true
            else
                echo "$line" >> "$temp_file"
            fi
        done < "$RULES_FILE"
        
        # If we didn't add it yet, add at end
        if [[ "$added" == false ]] && [[ "$in_category" == true ]]; then
            echo "$rule_entry" >> "$temp_file"
        fi
        
        mv "$temp_file" "$RULES_FILE"
    else
        # Create new category section
        local category_section="
## $emoji $category_title
$rule_entry"
        
        # Add before rule management system section
        sed -i "/## 📋 Rule Management System/i\\$category_section" "$RULES_FILE"
    fi
}

# Main script
main() {
    print_header
    
    # Check if RULES.md exists
    if [[ ! -f "$RULES_FILE" ]]; then
        print_error "RULES.md not found at $RULES_FILE"
        exit 1
    fi
    
    # Interactive mode if no arguments provided
    if [[ $# -eq 0 ]]; then
        echo "Interactive Rule Addition Mode"
        echo
        
        # Get category
        echo "Available categories:"
        echo "  1. architecture     (🏗️ Architecture & File Structure)"
        echo "  2. design-system    (🎨 Design System Standards)"
        echo "  3. webcomponent     (🧩 Web Component Development)"
        echo "  4. build-workflow   (⚙️ Build & Development Workflow)"
        echo "  5. documentation    (📝 Documentation Standards)"
        echo "  6. project-specific (🗂️ Project-Specific Rules)"
        echo
        read -p "Select category (1-6): " category_num
        
        case "$category_num" in
            1) category="architecture" ;;
            2) category="design-system" ;;
            3) category="webcomponent" ;;
            4) category="build-workflow" ;;
            5) category="documentation" ;;
            6) category="project-specific" ;;
            *) print_error "Invalid category selection"; exit 1 ;;
        esac
        
        # Get rule title
        echo
        read -p "Enter rule title: " title
        if [[ -z "$title" ]]; then
            print_error "Rule title is required"
            exit 1
        fi
        
        # Get rule content
        echo
        echo "Enter rule content (press Ctrl+D when finished):"
        content=$(cat)
        if [[ -z "$content" ]]; then
            print_error "Rule content is required"
            exit 1
        fi
        
        # Generate rule ID
        rule_id=$(generate_rule_id)
        
    else
        # Command line mode
        category="$1"
        title="$2"
        content="$3"
        rule_id="${4:-$(generate_rule_id)}"
        
        # Validate inputs
        if ! validate_category "$category"; then
            print_error "Invalid category: $category"
            print_warning "Valid categories: architecture, design-system, webcomponent, build-workflow, documentation, project-specific"
            exit 1
        fi
        
        if [[ -z "$title" || -z "$content" ]]; then
            print_error "Usage: $0 <category> <title> <content> [rule_id]"
            exit 1
        fi
    fi
    
    # Confirm before adding
    echo
    echo "Rule to be added:"
    echo "Category: $(get_category_emoji "$category") $(get_category_title "$category")"
    echo "Title: $title"
    echo "ID: $rule_id"
    echo "Content: $content"
    echo
    
    read -p "Add this rule? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        print_warning "Rule addition cancelled"
        exit 0
    fi
    
    # Add the rule
    add_rule_to_file "$category" "$title" "$content" "$rule_id"
    
    print_success "Rule added successfully!"
    print_success "Rule ID: $rule_id"
    
    # Git add if in git repo
    if git -C "$PRAW_DIR" status &>/dev/null; then
        git -C "$PRAW_DIR" add RULES.md
        print_success "RULES.md staged for commit"
        
        read -p "Create git commit? (y/N): " commit_confirm
        if [[ "$commit_confirm" == "y" || "$commit_confirm" == "Y" ]]; then
            git -C "$PRAW_DIR" commit -m "Add rule: $title

Category: $category
ID: $rule_id"
            print_success "Git commit created"
        fi
    fi
}

# Run the script
main "$@"