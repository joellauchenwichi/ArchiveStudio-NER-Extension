# Detailed Installation Guide

Step-by-step installation instructions for the Archive Studio Enhanced NER Extension.

## Table of Contents
1. [Prerequisites Check](#prerequisites-check)
2. [Installing Dependencies](#installing-dependencies)
3. [Setting Up the Extension](#setting-up-the-extension)
4. [Modifying Archive Studio](#modifying-archive-studio)
5. [Testing the Installation](#testing-the-installation)
6. [Common Issues](#common-issues)

---

## Prerequisites Check

Before starting, verify you have:

### ✅ Archive Studio Installed
- Archive Studio should be installed and working
- You should know where your Archive Studio files are located

### ✅ Python Installed
Check your Python version:
```bash
python --version
```
or
```bash
py --version
```

You need **Python 3.7 or higher**.

### ✅ pip Installed
Check if pip is available:
```bash
pip --version
```
or
```bash
py -m pip --version
```

---

## Installing Dependencies

### Step 1: Install Python Packages

Open your terminal/command prompt and run:

**Using pip:**
```bash
pip install spacy openpyxl pandas
```

**Using py (Windows):**
```bash
py -m pip install spacy openpyxl pandas
```

**Using requirements.txt:**
```bash
pip install -r requirements.txt
```

### Step 2: Download spaCy Language Model

This is **required** for entity recognition to work:

**Using pip:**
```bash
python -m spacy download en_core_web_sm
```

**Using py (Windows):**
```bash
py -m spacy download en_core_web_sm
```

**Verification:**
To verify the model installed correctly:
```bash
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ Model loaded successfully')"
```

---

## Setting Up the Extension

### Step 1: Locate Your Archive Studio Directory

Find where Archive Studio is installed. It should contain:
- `ArchiveStudio.py` (main file)
- `util/` folder (with files like `APIHandler.py`, `DataOperations.py`, etc.)

**Common locations:**
- Windows: `C:\Users\YourName\Downloads\Archive_Studio-main\Archive_Studio-main\`
- Mac/Linux: `~/Downloads/Archive_Studio-main/Archive_Studio-main/`

### Step 2: Copy EnhancedNERHandler.py

1. Download `EnhancedNERHandler.py` from this repository
2. Copy it to the `util/` folder in your Archive Studio directory

**Final location should be:**
```
Archive_Studio/
├── ArchiveStudio.py
└── util/
    ├── APIHandler.py
    ├── DataOperations.py
    ├── EnhancedNERHandler.py  ← NEW FILE HERE
    └── ... (other files)
```

---

## Modifying Archive Studio

You need to make **4 changes** to `ArchiveStudio.py`:

### Change 1: Add Import Statement

**Location:** Near the top of the file, around line 27, where other imports are

**Add this line:**
```python
from util.EnhancedNERHandler import EnhancedNERHandler
```

**It should look like:**
```python
# Import Local Scripts
from util.subs.ImageSplitter import ImageSplitter
from util.FindReplace import FindReplace
from util.APIHandler import APIHandler
# ... other imports ...
from util.EnhancedNERHandler import EnhancedNERHandler  # ← ADD THIS
```

---

### Change 2: Initialize the Handler

**Location:** In the `__init__` method of the `App` class, around line 113

**Add this line:**
```python
# Initialize the Enhanced NER Handler
self.enhanced_ner_handler = EnhancedNERHandler(self)
```

**It should come after other handler initializations:**
```python
# Initialize the AI Functions Handler
self.ai_functions_handler = AIFunctionsHandler(self)

# Initialize the Names and Places Handler
self.names_places_handler = NamesAndPlacesHandler(self)

# Initialize the Highlight Handler
self.highlight_handler = HighlightHandler(self)

# Initialize the Enhanced NER Handler  ← ADD THIS
self.enhanced_ner_handler = EnhancedNERHandler(self)
```

---

### Change 3: Add Menu Items

**Location:** In the `create_menus` method

#### A. Add to File Menu (around line 304)

Find this section:
```python
self.file_menu.add_command(label="Export Text...", command=self.export_manager.export_menu)
self.file_menu.add_command(label="Export CSV...", command=self.export_manager.show_csv_export_options)
```

**Add this line right after:**
```python
self.file_menu.add_command(label="Export Entities to Excel...", command=self.export_entities_excel)
```

#### B. Add to Tools Menu (around line 450)

Find this section:
```python
self.tools_menu.add_command(
    label="Find Relevant Documents",
    command=self.create_find_relevant_documents_window
)
```

**Add these lines right after:**
```python
self.tools_menu.add_separator()
self.tools_menu.add_command(
    label="Extract All Entities (Current Page)",
    command=lambda: self.enhanced_ner_handler.process_current_page()
)
self.tools_menu.add_command(
    label="Extract All Entities (All Pages)",
    command=lambda: self.enhanced_ner_handler.process_all_pages()
)
```

---

### Change 4: Add Export Handler Method

**Location:** Anywhere in the `App` class, around line 1550 (near other handler methods)

**Add this complete method:**
```python
def export_entities_excel(self):
    """Handler for exporting entities to Excel"""
    from tkinter import filedialog
    output_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="Export Entities to Excel"
    )
    if output_path:
        self.enhanced_ner_handler.export_entities_to_excel(output_path)
```

**Make sure it's indented at the same level as other methods like:**
- `def import_pdf(self):`
- `def find_and_replace(self):`
- etc.

---

## Testing the Installation

### Step 1: Start Archive Studio

Run Archive Studio:
```bash
cd C:\Users\YourName\Downloads\Archive_Studio-main\Archive_Studio-main
python ArchiveStudio.py
```

**Check for errors in the console.** If there are import errors, go back and verify the installation steps.

### Step 2: Verify Menu Items Appear

1. Open Archive Studio
2. Check **Tools** menu - you should see:
   - "Extract All Entities (Current Page)"
   - "Extract All Entities (All Pages)"
3. Check **File** menu - you should see:
   - "Export Entities to Excel..."

### Step 3: Test Entity Extraction

1. Load a document with text
2. Make sure text is recognized (Process → Recognize Text if needed)
3. Click **Tools → Extract All Entities (Current Page)**
4. You should see a popup showing extracted entities

### Step 4: Test Excel Export

1. After extracting entities, click **File → Export Entities to Excel...**
2. Choose a location and filename
3. Open the Excel file - you should see multiple sheets

---

## Common Issues

### Issue: "Module 'spacy' not found"

**Solution:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Issue: "Module 'openpyxl' not found"

**Solution:**
```bash
pip install openpyxl
```

### Issue: "EnhancedNERHandler could not be imported"

**Checklist:**
- ✓ Is `EnhancedNERHandler.py` in the `util/` folder?
- ✓ Is there a `__init__.py` file in the `util/` folder?
- ✓ Did you add the import statement correctly?
- ✓ Did you restart Archive Studio after making changes?

### Issue: "No text found to analyze"

**Solution:**
1. Make sure you've loaded documents
2. Run **Process → Recognize Text** first
3. Check that "Displayed Text" dropdown is not set to "None"

### Issue: Menu items don't appear

**Checklist:**
- ✓ Did you add the menu commands in the `create_menus` method?
- ✓ Did you save `ArchiveStudio.py`?
- ✓ Did you restart Archive Studio?
- ✓ Did you initialize the handler in `__init__`?

### Issue: AttributeError about 'start_progress' or 'create_progress_window'

Your version of Archive Studio might use a different progress bar API. The code should auto-adapt, but if it doesn't:

1. Open `EnhancedNERHandler.py`
2. Find the `process_all_pages` method
3. Look at how other parts of Archive Studio use the progress bar
4. Adjust the progress bar calls to match

---

## Verifying Successful Installation

✅ **Installation is complete when:**
1. Archive Studio starts without errors
2. New menu items appear in Tools and File menus
3. Entity extraction runs without errors
4. Excel export creates a multi-sheet workbook

---

## Need Help?

If you're still having issues:
1. Check the error message carefully
2. Look in the main README.md Troubleshooting section
3. Open an issue on GitHub with:
   - Your error message
   - Archive Studio version
   - Python version
   - Operating system

---

**Congratulations!** 🎉 If you've made it this far, your Enhanced NER Extension should be installed and working!