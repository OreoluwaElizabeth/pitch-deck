# Pitch Deck Parser

This is a web application that parses uploaded pitch deck documents(PDF or PowerPoint) and displays relevant information
in a table format on a simple dashboard.

## Features
- File upload (PDF or PPTX).
- Data parsing(slide titles, text content, metadata)
- Data storage in a database.
- Simple dashboard for displaying parsed data.

## Setup
1. Python 3.7 or higher
2. Flask and other dependencies(listed in requirements.txt)
3. Clone the repository.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the Flask app: `python app/api.py`.

## API Routes
- `POST /upload`: Upload a PDF or PPTX file.

## Unit Testing
The application includes unit tests to ensure the API works as expected. The tests are written using Python's built-in 
unittest framework.

## Running Tests
1. Navigate to the project root directory.
2. Run the tests: `python -m unittest tests/test_api.py`

## Test Cases
1. File Upload Success.
2. No File Uploaded.
3. Unsupported File Format.
4. Empty File.
5. File Overwrite.
6. File Size Exceeded.
7. File Save Error.

## Data Parsing
The Parser class is responsible for processing uploaded pitch deck files.
It extracts relevant content such as Slide Titles, Text Content and Metadata.

## Functionality
1. Handles both PDF and PPTX files seamlessly.
2. Uses external libraries to parse file content.
3. Validates file structure and ensures proper parsing.

## Test Cases
1. PDF Parsing Success.
2. PPTX Parsing Success.
3. Unsupported File Type.
4. Invalid PDF format.