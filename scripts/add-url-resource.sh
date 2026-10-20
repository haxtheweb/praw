#!/bin/bash

# Add URL Resource to Course
# Usage: add-url-resource "Course Name" "URL" "Description"

COURSE_NAME="$1"
URL="$2" 
DESCRIPTION="$3"

if [ -z "$COURSE_NAME" ] || [ -z "$URL" ]; then
    echo "❌ Usage: add-url-resource \"Course Name\" \"URL\" \"Description\""
    echo "Example: add-url-resource \"Anatomy 101\" \"https://example.com\" \"Great anatomy resource\""
    exit 1
fi

# Validate inputs: the URL must be a single-line http(s) URL with no whitespace or
# control characters, and the description a single line of bounded length, so
# values cannot inject extra lines/entries into the resources file.
NL=$'\n'
CR=$'\r'
if [[ "$URL" == *"$NL"* || "$URL" == *"$CR"* ]] || \
   ! [[ "$URL" =~ ^https?://[A-Za-z0-9]([A-Za-z0-9.-]*)(:[0-9]+)?([/?#][^[:space:][:cntrl:]\"\<\>\`\\^{}|]*)?$ ]]; then
    echo "❌ Invalid URL: must be a single-line http(s) URL without spaces or control characters"
    exit 1
fi
if [[ "$DESCRIPTION" == *"$NL"* || "$DESCRIPTION" == *"$CR"* || "$DESCRIPTION" =~ [[:cntrl:]] ]]; then
    echo "❌ Invalid description: must be a single line without control characters"
    exit 1
fi
if [ "${#DESCRIPTION}" -gt 500 ]; then
    echo "❌ Invalid description: longer than 500 characters"
    exit 1
fi
if [[ "$COURSE_NAME" == *"$NL"* || "$COURSE_NAME" == *"$CR"* ]]; then
    echo "❌ Invalid course name: must be a single line"
    exit 1
fi

# Convert to safe directory name
SAFE_NAME=$(echo "$COURSE_NAME" | sed 's/[^a-zA-Z0-9]/_/g' | tr '[:upper:]' '[:lower:]')
COURSE_DIR="$HOME/course-resources/$SAFE_NAME"

# Check if course exists
if [ ! -d "$COURSE_DIR" ]; then
    echo "❌ Course not found: $COURSE_NAME"
    echo "💡 Run: faculty-setup \"$COURSE_NAME\" first"
    exit 1
fi

# Add URL to resources file
RESOURCES_FILE="$COURSE_DIR/Web_Resources.txt"

# Create file if it doesn't exist
if [ ! -f "$RESOURCES_FILE" ]; then
    echo "Web Resources for $COURSE_NAME" > "$RESOURCES_FILE"
    echo "=================================" >> "$RESOURCES_FILE"
    echo "" >> "$RESOURCES_FILE"
fi

# Add the URL
echo "$(date '+%Y-%m-%d'): $URL" >> "$RESOURCES_FILE"
if [ ! -z "$DESCRIPTION" ]; then
    echo "  Description: $DESCRIPTION" >> "$RESOURCES_FILE"
fi
echo "" >> "$RESOURCES_FILE"

echo "✅ Added URL to $COURSE_NAME resources!"
echo "🔗 URL: $URL"
if [ ! -z "$DESCRIPTION" ]; then
    echo "📝 Description: $DESCRIPTION"
fi
echo "📁 Location: $RESOURCES_FILE"