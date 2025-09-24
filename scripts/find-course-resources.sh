#!/bin/bash

# Function to find course resources automatically
# Usage: find-course-resources "Course Name"

COURSE_NAME="$1"
if [ -z "$COURSE_NAME" ]; then
    echo "No course name provided"
    exit 1
fi

# Convert to safe directory name
SAFE_NAME=$(echo "$COURSE_NAME" | sed 's/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]')
COURSE_DIR="$HOME/course-resources/$SAFE_NAME"

# Check if course directory exists
if [ ! -d "$COURSE_DIR" ]; then
    echo "❌ Course not found: $COURSE_NAME"
    echo "💡 Run: faculty-setup \"$COURSE_NAME\" to create it"
    exit 1
fi

echo "📚 Found course resources for: $COURSE_NAME"
echo "📁 Location: $COURSE_DIR"
echo ""

# List all files in the directory
echo "📋 Available materials:"
find "$COURSE_DIR" -type f -not -name ".*" -not -name "INSTRUCTIONS.md" | while read file; do
    filename=$(basename "$file")
    echo "  - $filename"
done

echo ""
echo "✅ Ready to create content using these materials!"
echo "$COURSE_DIR"  # Return the path for scripting