# Smart Document Analyzer

## Project Overview
Smart Document Analyzer is a Flask-based web application designed to upload, analyze, and summarize documents. Utilizing Natural Language Processing (NLP), this application can identify key topics, sentiment analysis, and extract named entities from documents. It supports various file formats including PDFs and images, providing a comprehensive analysis of textual content.

## Features
- **Document Upload:** Users can upload documents in multiple formats, including PDFs and images.
- **Text Extraction:** Converts documents into text for analysis.
- **Keyword Tagging:** Identifies and tags keywords and topics within the documents.
- **Sentiment Analysis:** Classifies the sentiment of the text as positive, neutral, or negative.
- **Entity Recognition:** Identifies names, locations, institutions, and addresses within the text.
- **Summary Generation:** Produces concise summaries of the documents.
- **Search Functionality:** Allows searching documents based on keywords, entities, or sentiment.

## Installation

### Prerequisites
- Docker
- Python 3.9 or higher
- PostgreSQL

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jaketlee07/smart-document-analyzer.git
   cd smart-document-analyzer
   ```

2. **Build the Docker Container**
   ```bash
   docker build -t smart-document-analyzer .
   ```

3. **Run the Docker Container**
   ```bash
   docker run -p 8000:8000 smart-document-analyzer
   ```

4. **Accessing the Application**
   - The application will be available at `http://localhost:8000`.

### Database Configuration
- Ensure PostgreSQL is installed and running.
- Create a database named `smart_doc_analyzer`.
- Update the database URI in the application's configuration file to match your PostgreSQL settings.

## Usage

After installation, navigate to `http://localhost:8000` in your web browser to access the Smart Document Analyzer.

1. **Uploading Documents:**
   - Use the upload form to select and submit your document for analysis.

2. **Viewing Analysis Results:**
   - After uploading, the analysis results will be displayed, including key topics, sentiment, entity recognition, and a document summary.

## Development

For local development, follow the setup instructions mentioned above. Ensure you have all the required dependencies installed.

## License

This project is licensed under the [MIT License](LICENSE).
