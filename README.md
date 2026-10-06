# ArchiveStudio-NER-Extension
Named Entity Recognition extension for Archive Studio using spaCy

# Archive Studio

Archive Studio is a Windows desktop application designed to support historians, archivists, and researchers working with digitized historical documents. It provides tools for importing, organizing, transcribing, correcting, formatting, translating, analyzing, and exporting archival material.

This version extends the original Archive Studio application with an enhanced **Named Entity Recognition (NER)** workflow using spaCy, allowing researchers to automatically identify people, places, organizations, dates, events, and other entities across historical documents and export the results to Excel.

---

## Features

### Document Management

* Create, open, and save Archive Studio projects
* Open recently used projects
* Import PDFs
* Import images from folders
* Import text and images
* Navigate between pages and documents
* Manage archival images and associated text

### Text Processing

Archive Studio supports multiple stages of text processing, including:

* Original OCR/HTR text
* Corrected text
* Formatted text
* Translated text
* Separated document text
* Text search and replacement
* Processing individual pages or entire collections

The application also provides options to skip pages that have already been processed.

### AI-Assisted Processing

Archive Studio integrates AI-assisted workflows for working with historical documents, including functionality for:

* Handwritten Text Recognition (HTR)
* Text correction
* Text formatting
* Translation
* Relevance classification
* Document separation
* Text and document analysis

API configuration is handled through the application's settings.

---

# Enhanced Named Entity Recognition

This version of Archive Studio includes an enhanced Named Entity Recognition system implemented with **spaCy**.

The NER system uses spaCy's:

```text
en_core_web_sm
```

language model.

If the model is not installed, Archive Studio attempts to install it automatically the first time the NER functionality is initialized. If automatic installation fails, the application provides the command required to install it manually:

```bash
python -m spacy download en_core_web_sm
```

## Entity Types

The NER system recognizes and organizes entities into the following categories:

| spaCy Entity  | Archive Studio Category |
| ------------- | ----------------------- |
| `PERSON`      | People                  |
| `GPE`         | Places                  |
| `LOC`         | Places                  |
| `ORG`         | Organizations           |
| `DATE`        | Dates                   |
| `MONEY`       | Money                   |
| `EVENT`       | Events                  |
| `WORK_OF_ART` | Works                   |
| `LAW`         | Laws                    |
| `LANGUAGE`    | Languages               |
| `PRODUCT`     | Products                |

Other spaCy entity labels that may be detected are retained using their spaCy label when they do not have a custom Archive Studio category.

---

## Extracting Entities

Entities can be extracted from:

* The current page
* All pages in the project

When processing all pages, Archive Studio displays a progress window while the documents are analyzed.

The extracted entities are automatically added to the project's data table.

### People and Places

People and Places use the application's existing:

```text
People
Places
```

columns.

### Additional Entity Types

Other entity categories are stored in columns following the format:

```text
NER_<EntityType>
```

For example:

```text
NER_Organizations
NER_Dates
NER_Money
NER_Events
```

This allows entity information to remain associated with the page from which it was extracted.

---

# Exporting Entities to Excel

Archive Studio can export extracted entities to an Excel workbook.

The export contains three types of information:

### Summary

The **Summary** sheet provides statistics for each entity category, including:

* Entity type
* Number of pages containing entities
* Number of unique entities
* Total number of mentions

### Individual Entity Sheets

Each entity category receives its own sheet.

For example:

```text
People
Places
Organizations
Dates
Money
Events
```

Each record can contain:

| Field       | Description                            |
| ----------- | -------------------------------------- |
| Entity      | Extracted entity                       |
| Page        | Page where the entity was found        |
| Document_No | Associated document/page information   |
| Context     | Surrounding text containing the entity |

The context field attempts to provide up to approximately 100 characters before and after the entity, when available.

### Master Data

The **Master Data** sheet combines entity information with other project information.

When available, it includes:

* Index
* Page
* People
* Places
* NER entity columns
* Image path
* Original text
* Corrected text
* Formatted text
* Translation

This allows researchers to connect extracted entities back to the original archival material.

---

# Getting Started

## 1. Install Python

Install Python 3 and ensure that Python is available from your command line.

You can verify the installation with:

```bash
python --version
```

## 2. Install Dependencies

Install the required Python packages for the application.

At minimum, the enhanced NER functionality requires:

```bash
pip install spacy pandas openpyxl
```

The application also uses additional packages for its graphical interface, document processing, image handling, and other functionality.

## 3. Install the spaCy Model

Install the English spaCy model:

```bash
python -m spacy download en_core_web_sm
```

Archive Studio can also attempt this installation automatically when the application starts and the model is unavailable.

## 4. Launch Archive Studio

Run:

```bash
python ArchiveStudio.py
```

---

# Basic Workflow

A typical workflow is:

```text
Create/Open Project
        ↓
Import Documents
        ↓
Review Images
        ↓
Perform HTR/OCR
        ↓
Correct Text
        ↓
Format / Translate Text
        ↓
Separate Documents
        ↓
Extract Entities
        ↓
Review Results
        ↓
Export Data
```

Researchers can perform only the stages relevant to their project.

---

# Entity Extraction Workflow

A typical NER workflow is:

1. Import or open an archival project.
2. Ensure that text is available for the pages you want to analyze.
3. Select the entity extraction functionality.
4. Choose whether to process the current page or all pages.
5. Allow spaCy to analyze the text.
6. Review the extracted entities.
7. Save the project.
8. Export the entities to Excel if required.

The application displays a summary after extraction, including the number of unique entities found in each category and several example entities.

---

# Supported Text Sources for Entity Extraction

The NER system analyzes the text returned by Archive Studio's existing text-handling system.

This allows entity extraction to work with the appropriate processed text associated with each page rather than requiring a separate text file.

For Excel context generation, Archive Studio checks available text fields in the following order:

```text
Formatted_Text
Corrected_Text
Original_Text
Translation
```

It then attempts to locate the extracted entity and include surrounding text as context.

---

# Project Structure

The project is organized around the main Archive Studio application and supporting utility modules.

A simplified structure is:

```text
ArchiveStudio/
│
├── ArchiveStudio.py
│
└── util/
    ├── AIFunctions.py
    ├── APIHandler.py
    ├── DataOperations.py
    ├── EnhancedNERHandler.py
    ├── ExportFunctions.py
    ├── Highlights.py
    ├── ImageHandler.py
    ├── NamesAndPlaces.py
    ├── ProjectIO.py
    ├── Settings.py
    └── ...
```

The enhanced entity extraction functionality is implemented in:

```text
util/EnhancedNERHandler.py
```

---

# Keyboard Shortcuts

Archive Studio includes keyboard shortcuts for common operations.

| Shortcut           | Action               |
| ------------------ | -------------------- |
| `Ctrl + N`         | New Project          |
| `Ctrl + O`         | Open Project         |
| `Ctrl + S`         | Save Project         |
| `Ctrl + F`         | Find and Replace     |
| `Ctrl + Z`         | Undo                 |
| `Ctrl + Y`         | Redo                 |
| `Ctrl + Left`      | Previous Document    |
| `Ctrl + Right`     | Next Document        |
| `Ctrl + I`         | Edit Current Image   |
| `Ctrl + Shift + I` | Edit All Images      |
| `Ctrl + D`         | Delete Current Image |

---

# Export Options

Archive Studio provides several export options, including:

* Export Text
* Export CSV
* Export Entities to Excel

The entity Excel export is designed specifically for researchers who want to analyze extracted people, places, organizations, dates, and other entities outside Archive Studio.

---

# Limitations

The enhanced NER functionality relies on spaCy's pretrained English model:

```text
en_core_web_sm
```

Consequently:

* Entity recognition quality depends on the accuracy of the underlying spaCy model.
* Historical documents may contain spelling variations, unusual names, archaic language, damaged text, or OCR/HTR errors that affect entity recognition.
* Automatically extracted entities should therefore be reviewed before being treated as authoritative archival metadata.
* The current implementation uses an English spaCy model and is therefore primarily intended for English-language text.

---

# Original Project

Archive Studio builds upon an earlier Archive Studio application developed for working with historical documents.

This modified version extends the original application with an enhanced NER workflow and structured Excel export so that researchers can move from digitized archival documents to more structured entity-level data.

---

# License

Please refer to the original Archive Studio project's license and repository documentation for licensing information.

Any modifications and additions should be used in accordance with the applicable license and the terms of the original project.

---

# Citation

If you use Archive Studio in research, please cite the original Archive Studio project and any modified version or repository from which you obtained this implementation.

For research involving automatically extracted entities, consider documenting the spaCy model and version used so that the extraction process can be reproduced.

---

# Acknowledgments

This project builds upon the original Archive Studio application and incorporates open-source technologies including:

* spaCy
* pandas
* openpyxl
* PyMuPDF
* Pillow
* Tkinter
* tkinterdnd2

The enhanced NER functionality was developed to extend Archive Studio's existing historical-document workflow and make extracted archival entities easier to review, organize, and export.
