#!/bin/bash

# HAX Faculty Course Setup - Super Simple Version
# Usage: faculty-setup "Course Name"

COURSE_NAME="$1"
if [ -z "$COURSE_NAME" ]; then
    echo "❌ Please provide a course name"
    echo "Example: faculty-setup \"Anatomy 101\""
    exit 1
fi

# Create safe directory name (no spaces or special chars)
SAFE_NAME=$(echo "$COURSE_NAME" | sed 's/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]')
COURSE_DIR="$HOME/course-resources/$SAFE_NAME"

echo "🎓 Setting up course resources for: $COURSE_NAME"
echo "📁 Creating folder at: $COURSE_DIR"

# Create the directory structure
mkdir -p "$COURSE_DIR"

# Create a simple instruction file
cat > "$COURSE_DIR/INSTRUCTIONS.md" << EOF
# $COURSE_NAME Course Resources

## 📚 How to Add Your Materials

Simply **drag and drop** your course materials into this folder:

- **PDFs**: Textbook chapters, articles, handouts
- **Word documents**: Syllabi, assignments, notes  
- **Images**: Diagrams, photos, charts
- **Web Resources**: Edit the pre-created \`Web_Resources.txt\` file to add important URLs

## 🎯 How to Use

Once you've added materials, simply tell Warp:

> "Create a HAX site for $COURSE_NAME"
> "Make a quiz about [topic] for $COURSE_NAME"
> "Build a study guide for $COURSE_NAME"

Warp will automatically find and use ALL materials in this folder!

## 📂 Your Course Folder Location
\`$COURSE_DIR\`

## ✅ What You Can Create
- Course websites
- Interactive quizzes  
- Study guides
- Timeline pages
- Image galleries
- Assignment rubrics

Just add your files here and start making requests!
EOF

# Create a default Web_Resources.txt file for faculty to use
cat > "$COURSE_DIR/Web_Resources.txt" << EOF
# Web Resources for $COURSE_NAME
# Add your important website URLs here - one per line
# Format: URL - Description (optional)

# Example entries:
# https://www.khanacademy.org/ - Free online courses
# https://www.youtube.com/watch?v=example - Educational video
# https://www.wikipedia.org/wiki/topic - Background information

# Add your URLs below:

EOF

# Create a marker file so we know this is a course resource folder
echo "$COURSE_NAME" > "$COURSE_DIR/.course_name"
echo "$(date)" > "$COURSE_DIR/.created"

# Add to our master course list
MASTER_LIST="$HOME/course-resources/all_courses.txt"
mkdir -p "$HOME/course-resources"
echo "$COURSE_NAME|$COURSE_DIR|$(date)" >> "$MASTER_LIST"

echo ""
echo "✅ SUCCESS! Your $COURSE_NAME course is ready!"
echo ""
echo "📁 NEXT STEPS:"
echo "1. Open this folder: $COURSE_DIR"
echo "2. Drag your course materials (PDFs, Word docs, images) into it"
echo "3. Tell Warp: 'Create a HAX site for $COURSE_NAME'"
echo ""
echo "🎯 Warp will automatically find and use your materials!"

# Cross-platform folder opening
open_folder() {
    case "$OSTYPE" in
        "darwin"*)
            # macOS
            open "$COURSE_DIR" 2>/dev/null || true
            echo "📂 Folder opened for you!"
            ;;
        "linux-gnu"*)
            # Linux
            if command -v xdg-open >/dev/null 2>&1; then
                xdg-open "$COURSE_DIR" 2>/dev/null || true
                echo "📂 Folder opened for you!"
            else
                echo "📂 Open this folder manually: $COURSE_DIR"
            fi
            ;;
        "msys"* | "cygwin"* | "win32"*)
            # Windows (Git Bash, WSL, etc.)
            if command -v explorer.exe >/dev/null 2>&1; then
                # Convert Unix path to Windows path for explorer
                WIN_PATH=$(cygpath -w "$COURSE_DIR" 2>/dev/null || wslpath -w "$COURSE_DIR" 2>/dev/null || echo "$COURSE_DIR")
                explorer.exe "$WIN_PATH" 2>/dev/null || start "$COURSE_DIR" 2>/dev/null || true
                echo "📂 Folder opened for you!"
            elif command -v start >/dev/null 2>&1; then
                start "$COURSE_DIR" 2>/dev/null || true
                echo "📂 Folder opened for you!"
            else
                echo "📂 Open this folder manually: $COURSE_DIR"
            fi
            ;;
        *)
            echo "📂 Open this folder manually: $COURSE_DIR"
            ;;
    esac
}

# Try to open the folder
open_folder

echo ""
echo "💡 TIP: You can add materials anytime - just drop them in the folder!"