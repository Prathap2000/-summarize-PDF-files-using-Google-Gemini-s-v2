# File Summarizer using Google Gemini

This project is a web application that allows users to upload PDF files from Google Cloud Storage (GCS) and generate summaries using the Google Gemini API. The application is built using Streamlit, making it easy to use and deploy.

## Features

- Upload Google Cloud JSON key for authentication.
- List PDF files available in a specified GCS bucket.
- Select files to summarize.
- Generate summaries in different formats (lines, paragraphs, or custom).
- Download the generated summary as a text file.

## Prerequisites

- Python 3.7 or later
- Google Cloud account with access to Google Cloud Storage
- Google Gemini API key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/file-summarizer.git
   cd file-summarizer
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Cloud credentials:

   - Create a service account in Google Cloud and download the JSON key file.
   - Ensure that the service account has the necessary permissions to access the desired GCS bucket.

## Usage

1. Run the Streamlit application:

   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`.

3. Enter your Google Gemini API key.

4. Upload the Google Cloud JSON key file.

5. Enter the name of your GCS bucket and click "List Files" to see available PDF files.

6. Select a file and choose your summary preferences.

7. Click "Generate Summary" to retrieve the summary of the selected PDF.

8. You can download the summary as a text file.

## Notes

- Ensure your Google Gemini API key is valid and has access to the required features.
- Make sure your GCS bucket contains PDF files for summarization.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Google Gemini API](https://cloud.google.com/generative-ai/docs/gemini)
