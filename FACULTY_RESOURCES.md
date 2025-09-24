# Faculty Resource Management System

This system provides a simple, non-technical way for faculty to create resource repositories that AI agents can use to generate grounded, authoritative course content.

## 🎯 Overview

Faculty can create course resource folders, add materials (PDFs, documents, URLs), and then request AI-generated content using natural language - all without technical knowledge.

## 🚀 Quick Start for Faculty

### 1. Set up a course resource folder
```bash
faculty-setup "Your Course Name"
```

### 2. Add your materials
- **Drag and drop** files into the opened folder
- **PDFs**: Textbooks, articles, handouts
- **Word docs**: Syllabi, assignments, notes
- **Images**: Diagrams, charts, photos
- **Text files**: Website URLs, notes

### 3. Request content creation
Simply tell the AI:
- *"Create a HAX site for [Course Name]"*
- *"Make a quiz about [topic] for [Course Name]"*
- *"Build a study guide for [Course Name]"*

The AI automatically finds and uses ALL materials in the course folder!

## 📋 Available Commands

### Core Commands
- `faculty-setup "Course Name"` - Create a new course resource folder
- `find-course "Course Name"` - Locate and list course resources
- `add-url-resource "Course Name" "URL" "Description"` - Add web resources

### Usage Examples
```bash
# Set up a new course
faculty-setup "Biology 101"

# Add a web resource
add-url-resource "Biology 101" "https://www.khanacademy.org/biology" "Khan Academy Biology"

# Find course materials
find-course "Biology 101"
```

## 📁 Folder Structure

Each course gets a standardized folder:
```
~/course-resources/course_name/
├── INSTRUCTIONS.md          # Auto-generated usage guide
├── Web_Resources.txt        # URLs and web links
├── [faculty_files].pdf     # Drag-and-dropped materials
├── [faculty_files].docx    # Documents and syllabi
└── [faculty_files].*       # Any other course materials
```

## 🤖 How It Works

1. **Faculty setup**: One command creates everything needed
2. **Resource gathering**: Simple drag-and-drop interface
3. **AI integration**: Natural language requests automatically use course materials
4. **Content generation**: Grounded in faculty's actual resources, not general knowledge

## ✅ Benefits

- **Zero technical knowledge required**
- **One-command setup**
- **Automatic resource detection**
- **Natural language interface**
- **Grounded, authoritative content**
- **HAX-compatible output**

## 🔧 Installation

### Cross-Platform Support
**Supported Platforms:**
- ✅ **macOS** - Full support with automatic folder opening
- ✅ **Linux** - Full support with xdg-open integration  
- ✅ **Windows** - Git Bash, WSL, and PowerShell support
  - Automatic Windows Explorer integration
  - Handles path conversion (WSL/Cygwin)
  - Compatible with Windows Terminal and Git Bash

### Setup Commands
Add to your shell configuration:
```bash
# macOS/Linux: ~/.zshrc or ~/.bashrc
# Windows: ~/.bashrc (Git Bash) or PowerShell profile
alias faculty-setup="/path/to/praw/scripts/faculty-setup.sh"
alias find-course="/path/to/praw/scripts/find-course-resources.sh"  
alias add-url-resource="/path/to/praw/scripts/add-url-resource.sh"
```

## 📖 Faculty Workflow Example

**Professor Smith wants to create an Anatomy course:**

1. **Setup**: `faculty-setup "Anatomy 101"`
2. **Add materials**: Drags syllabus.pdf, textbook_ch1.pdf, quiz_questions.docx
3. **Add URLs**: `add-url-resource "Anatomy 101" "https://www.innerbody.com" "Interactive anatomy"`
4. **Create content**: "Create a HAX quiz about the skeletal system for Anatomy 101"

The AI automatically uses Professor Smith's specific materials to create the quiz!

## 🌍 Integration with HAX Ecosystem

This system works seamlessly with:
- **HAX sites**: Generate courses with proper structure
- **HAX components**: Use appropriate interactive elements  
- **DDD design system**: Consistent styling and layout
- **HAX CLI**: Leverages existing import capabilities
- **Educational components**: Quizzes, timelines, flashcards

## 🤝 Contributing

This faculty resource system is part of the PRAW (HAX ecosystem rules) project. Contributions welcome for:
- Additional import formats
- Enhanced URL handling
- Better faculty UX
- Integration with LMS systems