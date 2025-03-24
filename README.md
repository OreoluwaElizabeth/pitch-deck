# Pitch Deck Parser

This is a web application that parses uploaded pitch deck documents(PDF or PowerPoint) and displays relevant information
in a table format on a simple dashboard.

## Features
- File upload (PDF or PPTX).
- Data parsing(slide titles, text content, metadata)
- Data storage in a database(MongoDB).
- Simple dashboard for displaying parsed data.
- Responsive design
- Docker Compose setup

## Setup
1. Python 3.7 or higher
2. Flask and other dependencies(listed in requirements.txt)
3. Clone the repository.
4. Install dependencies: `pip install -r requirements.txt`.
5. Configure MongoDB connection in `app/config.py`
6. Run the Flask app: `python app/api.py`.
7. Run the Dashboard: `python dashboard.py`

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
2. Uses external libraries to parse file content(PyPDF2 for PDFs and pptx for PowerPoint files)
3. Validates file structure and ensures proper parsing.
4. Stores parsed data in MongoDB using the `PitchDeckData` model.

## Test Cases
1. PDF Parsing Success.
2. PPTX Parsing Success.
3. Unsupported File Type.
4. Invalid PDF format.


## Database Integration
This application uses MongoDB as its database. The PitchDeckData model in app/models.py handles the interaction with the
database.

## Functionality
1. Stores parsed data in the pitch_deck_data collection.
2. Handles database connection errors gracefully.
3. Provides methods for inserting and retrieving data.

## Error Handling
The application includes error handling for database connection issues. If the database connection fails, the 
application will log an error message and return an appropriate response.

## Testing
To test the database functionality:
1. Run the Flask app and upload a file.
2. Use MongoDB Compass or the MongoDB shell to verify that the data has been stored correctly.
3. Temporarily stop your MongoDB server to simulate a connection failure and ensure the application handles it gracefully.

## Dashboard
The application includes a simple dashboard to display the parsed data.

## Functionality
1. Retrieves data from the MongoDB database using the `PitchDeckData.get_all_data()` method.
2. Displays the data in an HTML table.

## Styling and Responsiveness
1. The dashboard is styled using CSS in the `static/style.css` file.
2. It's designed to be responsive, adapting to different screen sizes using media queries.
3. On smaller screens, the table data is stacked, and column headers are displayed using `data-label` attributes.

## Running the Dashboard
1. Ensure the Flask API is running.
2. Run the dashboard application: `python dashboard.py`.
3. Open your web browser and navigate to `http://127.0.0.1:5001`.

## Docker Compose
The application includes a Docker Compose file (`docker-compose.yml`) for easy deployment and containerization.

## Functionality
1. Defines two services: `api` (the Flask API) and `mongodb` (a local MongoDB instance).
2. Builds the API image using a `Dockerfile` located in the `api` directory.
3. Sets up a volume for persistent MongoDB data.
4. Links the API service to the MongoDB service.

## Running with Docker Compose
1. Ensure Docker Desktop is running.
2. Navigate to the project root directory (where `docker-compose.yml` is located).
3. Run `docker-compose up --build`.