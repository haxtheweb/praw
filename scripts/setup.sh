#!/bin/bash

# HAX PRAW Rule Management System Setup
# This script sets up the rule management system for easy use

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRAW_DIR="$(dirname "$SCRIPT_DIR")"
SHELL_RC_FILE=""

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}   HAX PRAW Rule Management System Setup${NC}"
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
    echo -e "${BLUE}ℹ $1${NC}"
}

detect_shell() {
    local shell_name=$(basename "$SHELL")
    case "$shell_name" in
        "zsh")
            SHELL_RC_FILE="$HOME/.zshrc"
            ;;
        "bash")
            SHELL_RC_FILE="$HOME/.bashrc"
            ;;
        "fish")
            SHELL_RC_FILE="$HOME/.config/fish/config.fish"
            ;;
        *)
            print_warning "Unknown shell: $shell_name"
            SHELL_RC_FILE="$HOME/.profile"
            ;;
    esac
}

create_directories() {
    print_info "Creating necessary directories..."
    
    # Create exports directory
    mkdir -p "$PRAW_DIR/exports"
    print_success "Created exports directory"
    
    # Create backups directory
    mkdir -p "$PRAW_DIR/backups"
    print_success "Created backups directory"
}

setup_aliases() {
    print_info "Setting up shell aliases..."
    
    detect_shell
    
    local aliases_content="
# HAX PRAW Rule Management System Aliases
alias praw-add='$SCRIPT_DIR/add-rule.sh'
alias praw-manage='$SCRIPT_DIR/manage-rules.sh'
alias praw-list='$SCRIPT_DIR/manage-rules.sh list'
alias praw-search='$SCRIPT_DIR/manage-rules.sh search'
alias praw-show='$SCRIPT_DIR/manage-rules.sh show'
alias praw-stats='$SCRIPT_DIR/manage-rules.sh stats'
alias praw-validate='$SCRIPT_DIR/manage-rules.sh validate'
alias praw-export='$SCRIPT_DIR/manage-rules.sh export'
alias praw-help='$SCRIPT_DIR/manage-rules.sh help'

# Faculty Resource Management Aliases
alias faculty-setup='$SCRIPT_DIR/faculty-setup.sh'
alias find-course='$SCRIPT_DIR/find-course-resources.sh'
alias add-url-resource='$SCRIPT_DIR/add-url-resource.sh'

# Quick navigation to PRAW directory
alias cd-praw='cd $PRAW_DIR'
"
    
    # Check if aliases already exist
    if grep -q "# HAX PRAW Rule Management System Aliases" "$SHELL_RC_FILE" 2>/dev/null; then
        print_warning "Aliases already exist in $SHELL_RC_FILE"
        read -p "Update existing aliases? (y/N): " update_aliases
        if [[ "$update_aliases" == "y" || "$update_aliases" == "Y" ]]; then
            # Remove old aliases and add new ones
            sed -i '/# HAX PRAW Rule Management System Aliases/,/^$/d' "$SHELL_RC_FILE"
            echo "$aliases_content" >> "$SHELL_RC_FILE"
            print_success "Updated aliases in $SHELL_RC_FILE"
        fi
    else
        echo "$aliases_content" >> "$SHELL_RC_FILE"
        print_success "Added aliases to $SHELL_RC_FILE"
    fi
}

create_symlinks() {
    print_info "Creating convenient symlinks..."
    
    # Create symlink in user's bin directory if it exists
    if [[ -d "$HOME/bin" ]]; then
        ln -sf "$SCRIPT_DIR/add-rule.sh" "$HOME/bin/praw-add" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/manage-rules.sh" "$HOME/bin/praw-manage" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/faculty-setup.sh" "$HOME/bin/faculty-setup" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/find-course-resources.sh" "$HOME/bin/find-course" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/add-url-resource.sh" "$HOME/bin/add-url-resource" 2>/dev/null || true
        print_success "Created symlinks in ~/bin/"
    fi
    
    # Create symlink in /usr/local/bin if writable
    if [[ -w "/usr/local/bin" ]]; then
        ln -sf "$SCRIPT_DIR/add-rule.sh" "/usr/local/bin/praw-add" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/manage-rules.sh" "/usr/local/bin/praw-manage" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/faculty-setup.sh" "/usr/local/bin/faculty-setup" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/find-course-resources.sh" "/usr/local/bin/find-course" 2>/dev/null || true
        ln -sf "$SCRIPT_DIR/add-url-resource.sh" "/usr/local/bin/add-url-resource" 2>/dev/null || true
        print_success "Created system-wide symlinks in /usr/local/bin/"
    fi
}

setup_git_hooks() {
    print_info "Setting up git hooks..."
    
    if [[ -d "$PRAW_DIR/.git" ]]; then
        # Pre-commit hook to validate rules
        local pre_commit_hook="$PRAW_DIR/.git/hooks/pre-commit"
        
        cat > "$pre_commit_hook" << 'EOF'
#!/bin/bash
# HAX PRAW pre-commit hook
# Validates RULES.md structure before committing

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/../../scripts && pwd)"

if [[ -f "$SCRIPT_DIR/manage-rules.sh" ]]; then
    echo "Validating RULES.md structure..."
    if "$SCRIPT_DIR/manage-rules.sh" validate > /dev/null 2>&1; then
        echo "✓ RULES.md validation passed"
    else
        echo "✗ RULES.md validation failed"
        echo "Run 'praw-validate' to see details"
        exit 1
    fi
fi
EOF
        
        chmod +x "$pre_commit_hook"
        print_success "Set up git pre-commit hook"
    else
        print_warning "Not a git repository, skipping git hooks setup"
    fi
}

create_backup() {
    print_info "Creating backup of current state..."
    
    local backup_dir="$PRAW_DIR/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    # Backup RULES.md if it exists
    if [[ -f "$PRAW_DIR/RULES.md" ]]; then
        cp "$PRAW_DIR/RULES.md" "$backup_dir/"
        print_success "Backed up RULES.md"
    fi
    
    # Backup WARP.md files
    find "$PRAW_DIR" -name "WARP.md" -type f | while read -r warp_file; do
        # Cross-platform relative path calculation
        local relative_path=$(echo "$warp_file" | sed "s|^$PRAW_DIR/||")
        local backup_file="$backup_dir/$(dirname "$relative_path")"
        mkdir -p "$backup_file"
        cp "$warp_file" "$backup_file/"
    done
    
    print_success "Created backup in $backup_dir"
}

show_usage() {
    echo
    echo -e "${YELLOW}Usage Examples:${NC}"
    echo
    echo "  # Add a new rule interactively"
    echo "  praw-add"
    echo
    echo "  # Add a rule via command line"
    echo "  praw-add webcomponent 'New Component Rule' 'Always include proper documentation'"
    echo
    echo "  # List all rules"
    echo "  praw-list"
    echo
    echo "  # Search for rules"
    echo "  praw-search DDD"
    echo
    echo "  # Show rule statistics"
    echo "  praw-stats"
    echo
    echo "  # Validate RULES.md structure"
    echo "  praw-validate"
    echo
    echo "  # Export rules to JSON"
    echo "  praw-export json"
    echo
    echo "  # Get help"
    echo "  praw-help"
    echo
    echo "  # Faculty Resource Management:"
    echo "  faculty-setup 'Biology 101'         # Create course resource folder"
    echo "  find-course 'Biology 101'           # Find course materials"
    echo "  add-url-resource 'Biology 101' 'https://example.com' 'Description'"
    echo
}

main() {
    print_header
    
    print_info "Setting up HAX PRAW Rule Management System..."
    echo
    
    # Create necessary directories
    create_directories
    echo
    
    # Create backup
    create_backup
    echo
    
    # Set up aliases
    setup_aliases
    echo
    
    # Create symlinks
    create_symlinks
    echo
    
    # Set up git hooks
    setup_git_hooks
    echo
    
    print_success "Setup complete!"
    echo
    
    print_info "Please restart your terminal or run 'source $SHELL_RC_FILE' to use the new aliases"
    
    show_usage
    
    # Validate current setup
    echo
    print_info "Running validation check..."
    if "$SCRIPT_DIR/manage-rules.sh" validate > /dev/null 2>&1; then
        print_success "RULES.md structure is valid"
    else
        print_warning "RULES.md structure has some issues - run 'praw-validate' for details"
    fi
    
    # Show current stats
    echo
    print_info "Current rule statistics:"
    "$SCRIPT_DIR/manage-rules.sh" stats | tail -n +3
}

# Run setup
main "$@"