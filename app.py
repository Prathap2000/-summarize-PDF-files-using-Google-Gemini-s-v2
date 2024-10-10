import os
import streamlit as st
from google.cloud import storage
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to download a file from GCS
def download_from_gcs(bucket_name, blob_name):
    """Downloads a file from GCS and returns the file path."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Create a temporary file path
    temp_file_path = f"temp_{os.path.basename(blob_name)}"
    
    # Download the file to the temporary path
    blob.download_to_filename(temp_file_path)
    
    return temp_file_path

# Function to summarize the PDF file using the Gemini API
def summarize_pdf_with_gemini(file_path, api_key, summary_type, summary_value, custom_prompt):
    """Uploads the PDF file and retrieves the summary based on user options."""
    # Configure Gemini API with the provided API key
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Upload the file
    sample_pdf = genai.upload_file(file_path)

    # Prepare the prompt based on user selection
    if summary_type == "custom" and custom_prompt:
        prompt = custom_prompt
    else:
        prompt = f"Give me a summary of this PDF file in {summary_value} {summary_type}."

    # Generate summary
    response = model.generate_content([prompt, sample_pdf])

    # Return the summary response text
    if hasattr(response, 'text') and response.text:
        return response.text
    else:
        return "No summary returned. Please check the file or try another document."

# Streamlit interface to display available files and summarize
st.title('File Summarizer using Google Gemini')

# Step 1: Input API key
api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

# Step 2: Upload JSON key for Google Cloud authentication
json_key_file = st.file_uploader("Upload your Google Cloud JSON key file", type="json")

# Initialize session state for various variables
if 'bucket_name' not in st.session_state:
    st.session_state.bucket_name = ""
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = ""
if 'file_names' not in st.session_state:
    st.session_state.file_names = []
if 'summary_type' not in st.session_state:
    st.session_state.summary_type = "lines"
if 'summary_value' not in st.session_state:
    st.session_state.summary_value = 3
if 'custom_prompt' not in st.session_state:
    st.session_state.custom_prompt = ""
if 'show_summary_section' not in st.session_state:
    st.session_state.show_summary_section = False

if json_key_file is not None:
    # Save the uploaded JSON key temporarily
    with open("google_credentials.json", "wb") as f:
        f.write(json_key_file.getbuffer())

    # Set the Google Application Credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_credentials.json"
    
    # Step 3: Input for bucket name
    st.session_state.bucket_name = st.text_input("Enter the Google Cloud Storage bucket name:", st.session_state.bucket_name)

    # List Files button
    if st.button("List Files"):
        if st.session_state.bucket_name:
            try:
                # List available files in the bucket
                storage_client = storage.Client()
                blobs = storage_client.list_blobs(st.session_state.bucket_name)

                # Create a list of file names in the bucket
                st.session_state.file_names = [blob.name for blob in blobs]

                # Check if there are any files available
                if not st.session_state.file_names:
                    st.warning("No files available in the bucket.")
                else:
                    # Mark that files have been listed
                    st.session_state.show_summary_section = True  # Flag to show the summary section

            except Exception as e:
                st.error(f"Error accessing bucket: {str(e)}")
        else:
            st.warning("Please enter a bucket name.")

# Show file selection dropdown if files are available
if st.session_state.show_summary_section:
    if st.session_state.file_names:
        st.session_state.selected_file = st.selectbox("Select a file from the bucket", st.session_state.file_names)

        # Summary Section - Radio buttons for summary options
        st.session_state.summary_type = st.radio("Select the type of summary:", 
                                 ("lines", "paragraphs", "custom"), index=["lines", "paragraphs", "custom"].index(st.session_state.summary_type))

        # Inputs for summary specifications
        if st.session_state.summary_type == "lines":
            st.session_state.summary_value = st.number_input("Specify the number of lines:", min_value=1, max_value=20, value=st.session_state.summary_value)
            st.session_state.custom_prompt = ""  # Clear custom prompt if lines are selected
        elif st.session_state.summary_type == "paragraphs":
            st.session_state.summary_value = st.number_input("Specify the number of paragraphs:", min_value=1, max_value=5, value=st.session_state.summary_value)
            st.session_state.custom_prompt = ""  # Clear custom prompt if paragraphs are selected
        elif st.session_state.summary_type == "custom":
            st.session_state.custom_prompt = st.text_input("Enter your custom prompt:", st.session_state.custom_prompt)

        # Ensure the summary generation button is only enabled if a file is selected
        if st.session_state.selected_file and api_key:
            if st.button("Generate Summary"):
                try:
                    # Download the file from GCS
                    file_path = download_from_gcs(st.session_state.bucket_name, st.session_state.selected_file)

                    # Summarize the PDF file using the uploaded file and user options
                    summary = summarize_pdf_with_gemini(file_path, api_key, st.session_state.summary_type, st.session_state.summary_value, st.session_state.custom_prompt)

                    # Display the summary
                    st.subheader("Summary Result:")
                    st.write(summary)

                    # Optionally, allow downloading the summary as a file
                    st.download_button(
                        label="Download Summary as Text",
                        data=summary.encode('utf-8'),
                        file_name="summary.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"An error occurred while generating the summary: {str(e)}")

                # Clean up temporary file after processing
                os.remove(file_path)
    else:
        st.warning("No files available to select.")
