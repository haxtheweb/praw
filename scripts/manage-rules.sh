#!/bin/bash

# HAX PRAW Rule Management System
# Script to search, list, and manage existing rules

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
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

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

show_help() {
    cat << EOF
HAX PRAW Rule Management System

USAGE:
    $0 <command> [options]

COMMANDS:
    list [category]         List all rules or rules in a specific category
    search <term>           Search for rules containing the specified term
    show <rule_id>          Show details for a specific rule ID
    categories              List all rule categories
    stats                   Show rule statistics
    validate                Validate RULES.md structure
    export [format]         Export rules (json, csv, or md)
    help                    Show this help message

CATEGORIES:
    architecture            Architecture & File Structure Rules
    design-system          Design System Standards  
    webcomponent           Web Component Development
    build-workflow         Build & Development Workflow
    documentation          Documentation Standards
    project-specific       Project-Specific Rules

EXAMPLES:
    $0 list                        # List all rules
    $0 list webcomponent          # List web component rules
    $0 search "DDD"               # Search for rules containing "DDD"
    $0 show rHQ7lLRZmZlnFveLrWslUN # Show specific rule
    $0 stats                      # Show rule statistics
    $0 export json                # Export rules as JSON

EOF
}

list_categories() {
    echo -e "${PURPLE}Available Rule Categories:${NC}"
    echo
    grep -E "^## [🏗️🎨🧩⚙️📝🗂️]" "$RULES_FILE" | sed 's/^## /  /' | while read -r line; do
        echo -e "  ${CYAN}$line${NC}"
    done
    echo
}

list_rules() {
    local category="$1"
    
    if [[ -z "$category" ]]; then
        echo -e "${PURPLE}All Rules:${NC}"
        echo
    else
        echo -e "${PURPLE}Rules in category: $category${NC}"
        echo
    fi
    
    local in_category=false
    local rule_count=0
    
    while IFS= read -r line; do
        # Check for category headers
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            if [[ -z "$category" ]]; then
                echo -e "\n${YELLOW}$line${NC}"
                in_category=true
            elif [[ "$line" == *"$category"* ]] || [[ -z "$category" ]]; then
                echo -e "\n${YELLOW}$line${NC}"
                in_category=true
            else
                in_category=false
            fi
        elif [[ "$line" =~ ^###[[:space:]] ]] && [[ "$in_category" == true ]]; then
            # Rule title
            local title=$(echo "$line" | sed 's/^### //')
            echo -e "  ${GREEN}$title${NC}"
            ((rule_count++))
        elif [[ "$line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]] && [[ "$in_category" == true ]]; then
            # Rule ID
            local rule_id=$(echo "$line" | sed 's/^- \*\*Rule ID\*\*: `\(.*\)`$/\1/')
            echo -e "    ${CYAN}ID: $rule_id${NC}"
        elif [[ "$line" =~ ^-[[:space:]]**Content** ]] && [[ "$in_category" == true ]]; then
            # Rule content (truncated)
            local content=$(echo "$line" | sed 's/^- \*\*Content\*\*: //')
            if [[ ${#content} -gt 80 ]]; then
                content="${content:0:80}..."
            fi
            echo -e "    ${CYAN}Content: $content${NC}"
            echo
        fi
    done < "$RULES_FILE"
    
    echo -e "${PURPLE}Total rules found: $rule_count${NC}"
}

search_rules() {
    local term="$1"
    
    if [[ -z "$term" ]]; then
        print_error "Search term is required"
        return 1
    fi
    
    echo -e "${PURPLE}Searching for: '$term'${NC}"
    echo
    
    local current_rule_title=""
    local current_rule_id=""
    local found_count=0
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^###[[:space:]] ]]; then
            current_rule_title=$(echo "$line" | sed 's/^### //')
        elif [[ "$line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]]; then
            current_rule_id=$(echo "$line" | sed 's/^- \*\*Rule ID\*\*: `\(.*\)`$/\1/')
        elif [[ "$line" =~ ^-[[:space:]]**Content** ]]; then
            local content=$(echo "$line" | sed 's/^- \*\*Content\*\*: //')
            
            # Check if search term matches title or content (case insensitive)
            if echo "$current_rule_title" | grep -qi "$term" || echo "$content" | grep -qi "$term"; then
                echo -e "${GREEN}$current_rule_title${NC}"
                echo -e "  ${CYAN}ID: $current_rule_id${NC}"
                
                # Highlight matching text in content
                local highlighted_content=$(echo "$content" | sed -E "s/($term)/${YELLOW}\1${NC}/gi")
                echo -e "  ${CYAN}Content: $highlighted_content${NC}"
                echo
                ((found_count++))
            fi
        fi
    done < "$RULES_FILE"
    
    echo -e "${PURPLE}Found $found_count matching rules${NC}"
}

show_rule() {
    local rule_id="$1"
    
    if [[ -z "$rule_id" ]]; then
        print_error "Rule ID is required"
        return 1
    fi
    
    echo -e "${PURPLE}Rule Details:${NC}"
    echo
    
    local found=false
    local current_rule_title=""
    local current_category=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            current_category="$line"
        elif [[ "$line" =~ ^###[[:space:]] ]]; then
            current_rule_title=$(echo "$line" | sed 's/^### //')
        elif [[ "$line" == *"$rule_id"* ]] && [[ "$line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]]; then
            found=true
            echo -e "${YELLOW}$current_category${NC}"
            echo
            echo -e "${GREEN}Title: $current_rule_title${NC}"
            echo -e "${CYAN}ID: $rule_id${NC}"
            
            # Get the content from next line
            read -r content_line
            local content=$(echo "$content_line" | sed 's/^- \*\*Content\*\*: //')
            echo -e "${CYAN}Content: $content${NC}"
            break
        fi
    done < "$RULES_FILE"
    
    if [[ "$found" == false ]]; then
        print_error "Rule with ID '$rule_id' not found"
        return 1
    fi
}

show_stats() {
    echo -e "${PURPLE}Rule Statistics:${NC}"
    echo
    
    # Count total rules
    local total_rules=$(grep -c "^### " "$RULES_FILE" || echo "0")
    echo -e "${GREEN}Total Rules: $total_rules${NC}"
    
    # Count rules by category
    echo -e "\n${YELLOW}Rules by Category:${NC}"
    
    local current_category=""
    local rule_count=0
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            if [[ -n "$current_category" ]]; then
                echo -e "  ${CYAN}$current_category: $rule_count${NC}"
            fi
            current_category=$(echo "$line" | sed 's/^## //')
            rule_count=0
        elif [[ "$line" =~ ^###[[:space:]] ]]; then
            ((rule_count++))
        fi
    done < "$RULES_FILE"
    
    # Don't forget the last category
    if [[ -n "$current_category" ]]; then
        echo -e "  ${CYAN}$current_category: $rule_count${NC}"
    fi
    
    # Check for duplicate rule IDs
    echo -e "\n${YELLOW}Validation:${NC}"
    local duplicate_ids=$(grep -o '`[^`]*`' "$RULES_FILE" | grep "Rule ID" -A1 | grep -v "Rule ID" | sort | uniq -d | wc -l)
    if [[ "$duplicate_ids" -gt 0 ]]; then
        print_warning "$duplicate_ids duplicate rule ID(s) found"
    else
        print_success "No duplicate rule IDs found"
    fi
}

validate_rules() {
    echo -e "${PURPLE}Validating RULES.md structure...${NC}"
    echo
    
    local errors=0
    local warnings=0
    
    # Check file exists
    if [[ ! -f "$RULES_FILE" ]]; then
        print_error "RULES.md file not found"
        ((errors++))
        return $errors
    fi
    
    # Check for required sections
    local required_sections=(
        "Rule Precedence System"
        "Rule Management System"
        "Future Rule Management"
    )
    
    for section in "${required_sections[@]}"; do
        if ! grep -q "## .*$section" "$RULES_FILE"; then
            print_error "Missing required section: $section"
            ((errors++))
        fi
    done
    
    # Check rule structure
    local rule_count=0
    local malformed_rules=0
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^###[[:space:]] ]]; then
            ((rule_count++))
            local has_id=false
            local has_content=false
            
            # Check next few lines for proper structure
            for i in {1..5}; do
                read -r next_line
                if [[ "$next_line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]]; then
                    has_id=true
                elif [[ "$next_line" =~ ^-[[:space:]]**Content** ]]; then
                    has_content=true
                fi
            done
            
            if [[ "$has_id" == false ]] || [[ "$has_content" == false ]]; then
                ((malformed_rules++))
            fi
        fi
    done < "$RULES_FILE"
    
    if [[ $malformed_rules -gt 0 ]]; then
        print_warning "$malformed_rules malformed rule(s) found"
        ((warnings++))
    fi
    
    # Summary
    echo
    if [[ $errors -eq 0 ]]; then
        print_success "RULES.md structure is valid"
        if [[ $warnings -gt 0 ]]; then
            print_warning "$warnings warning(s) found"
        fi
    else
        print_error "$errors error(s) found"
        return $errors
    fi
    
    print_info "Total rules validated: $rule_count"
}

export_rules() {
    local format="${1:-md}"
    local output_file="/home/bto108a/Documents/git/haxtheweb/praw/exports/rules-export.${format}"
    
    # Create exports directory
    mkdir -p "$(dirname "$output_file")"
    
    case "$format" in
        "json")
            export_json "$output_file"
            ;;
        "csv")
            export_csv "$output_file"
            ;;
        "md")
            cp "$RULES_FILE" "$output_file"
            print_success "Rules exported to $output_file"
            ;;
        *)
            print_error "Unsupported format: $format"
            print_info "Supported formats: json, csv, md"
            return 1
            ;;
    esac
}

export_json() {
    local output_file="$1"
    
    echo '{"rules": [' > "$output_file"
    
    local first_rule=true
    local current_title=""
    local current_id=""
    local current_category=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            current_category=$(echo "$line" | sed 's/^## //')
        elif [[ "$line" =~ ^###[[:space:]] ]]; then
            current_title=$(echo "$line" | sed 's/^### //')
        elif [[ "$line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]]; then
            current_id=$(echo "$line" | sed 's/^- \*\*Rule ID\*\*: `\(.*\)`$/\1/')
        elif [[ "$line" =~ ^-[[:space:]]**Content** ]]; then
            local content=$(echo "$line" | sed 's/^- \*\*Content\*\*: //')
            
            if [[ "$first_rule" == false ]]; then
                echo ',' >> "$output_file"
            fi
            first_rule=false
            
            cat << 'EOF_JSON' >> "$output_file"
  {
    "id": "$current_id",
    "title": "$current_title",
    "category": "$current_category",
    "content": "$content"
  }
EOF_JSON
        fi
    done < "$RULES_FILE"
    
    echo ']' >> "$output_file"
    echo '}' >> "$output_file"
    
    print_success "Rules exported to $output_file"
}

export_csv() {
    local output_file="$1"
    
    echo "ID,Title,Category,Content" > "$output_file"
    
    local current_title=""
    local current_id=""
    local current_category=""
    
    while IFS= read -r line; do
        if [[ "$line" =~ ^##[[:space:]] ]]; then
            current_category=$(echo "$line" | sed 's/^## //' | sed 's/[🏗️🎨🧩⚙️📝🗂️] //g')
        elif [[ "$line" =~ ^###[[:space:]] ]]; then
            current_title=$(echo "$line" | sed 's/^### //')
        elif [[ "$line" =~ ^-[[:space:]]**Rule[[:space:]]ID** ]]; then
            current_id=$(echo "$line" | sed 's/^- \*\*Rule ID\*\*: `\(.*\)`$/\1/')
        elif [[ "$line" =~ ^-[[:space:]]**Content** ]]; then
            local content=$(echo "$line" | sed 's/^- \*\*Content\*\*: //' | sed 's/"/\\"/g')
            echo "\"$current_id\",\"$current_title\",\"$current_category\",\"$content\"" >> "$output_file"
        fi
    done < "$RULES_FILE"
    
    print_success "Rules exported to $output_file"
}

# Main script
main() {
    local command="$1"
    
    # Check if RULES.md exists
    if [[ ! -f "$RULES_FILE" ]] && [[ "$command" != "help" ]]; then
        print_error "RULES.md not found at $RULES_FILE"
        exit 1
    fi
    
    case "$command" in
        "list")
            list_rules "$2"
            ;;
        "search")
            search_rules "$2"
            ;;
        "show")
            show_rule "$2"
            ;;
        "categories")
            list_categories
            ;;
        "stats")
            show_stats
            ;;
        "validate")
            validate_rules
            ;;
        "export")
            export_rules "$2"
            ;;
        "help"|"")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Show header and run
if [[ "$1" != "help" && "$1" != "" ]]; then
    print_header
fi

main "$@"