# Smart Document Analyzer

## Project Overview

Smart Document Analyzer is a Flask-based web application that leverages advanced Natural Language Processing (NLP) techniques to analyze and summarize textual content in uploaded documents. It supports a variety of file formats such as PDFs and text files. The application provides insights by performing sentiment analysis, extracting keywords, and generating concise summaries.

## Features

- **Document Upload:** Supports uploading documents in multiple formats, including PDF and plain text.
- **Text Extraction:** Automatically converts non-text content into text for analysis.
- **Keyword Extraction:** Identifies key terms and phrases within the documents.
- **Sentiment Analysis:** Analyzes and determines the sentiment of the text (positive, neutral, negative).
- **Summary Generation:** Automatically generates a summary of the main points of the document.
- **Entity Recognition:** Detects entities like names, places, and dates within the text.
- **Search Functionality:** Enables users to search within their uploaded documents based on keywords or entities.

  ## Demo Video
  [![DEMO VIDEO]([http://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg](https://github.com/jaketlee07/smart-document-analyzer/assets/54076176/10ed7483-09ca-4b14-9bba-aa63de8ccb34))]([http://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE](https://drive.google.com/file/d/1Qzx9IQejnzukL-xVSQFjRhjQpFm5k0HQ/view?usp=sharing))

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

Here are some images of the working Docker
<img width="1440" alt="Screenshot 2024-03-30 at 12 47 38 AM" src="https://github.com/jaketlee07/smart-document-analyzer/assets/54076176/fc27347b-5d6d-402b-abf4-4c02afa1b7ce">
<img width="908" alt="Screenshot 2024-03-30 at 12 48 31 AM" src="https://github.com/jaketlee07/smart-document-analyzer/assets/54076176/5a6aaff8-a7b5-4a54-ac03-3912394d4eae">

## License

This project is licensed under the [MIT License](LICENSE).
