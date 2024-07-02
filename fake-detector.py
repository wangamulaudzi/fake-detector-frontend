# Front-end for the fake-news app using streamlit
# By: Wanga Mulaudzi
# June 2024

# Import statements
import gcsfs # For accessing GCP storage
import io # For reading bytes
from PIL import Image # For opening images
import streamlit as st # For the frontend
from st_files_connection import FilesConnection # For creating a connection object

#############
# Variables #
#############
bg_img_path = "fake-detector/images/fake-detector-bg.jpeg" # Path to background image on GCP

######################
# For the background #
######################

# Retrieve GCS secrets from Streamlit Secrets Manager
project_id = st.secrets["connections"]["gcs"]["project_id"]
client_email = st.secrets["connections"]["gcs"]["client_email"]
private_key = st.secrets["connections"]["gcs"]["private_key"].replace('\\n', '\n')  # Correct formatting of the private key

# Initialize a GCS filesystem
fs = gcsfs.GCSFileSystem(project=project_id, token=f'{" ".join([client_email, private_key])}')

# Construct the public URL to the image in GCS
bg_image_url = f"https://storage.cloud.google.com/{bg_img_path}"

# Set the background style using CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{bg_image_url}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp > header {{
        background-color: transparent;
    }}
    .main .block-container {{
        background-color: rgba(236, 224, 209, 0.9);
        padding: 2rem;
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# Create a container for the main content
content_container = st.container()

with content_container:
    #########
    # Title #
    #########

    st.title("Fake Detector")
    st.markdown("## Can AI be the judge?")

    ########################
    # Handle image uploads #
    ########################

    # Let the user upload a file
    # Variable to store uploaded images
    uploaded_image = st.file_uploader("Upload your image (png/jpg):", accept_multiple_files=False,
                                       type=["png", "jpg"])

    #############################
    # Handle the uploaded_image #
    #############################
    if uploaded_image:
        bytes_data = uploaded_image.read()

        print(bytes_data)
