# Front-end for the fake-news app using streamlit
# By: Wanga Mulaudzi
# June 2024

# Import statements
import streamlit as st # For the frontend
from st_files_connection import FilesConnection

######################
# For the background #
######################

# # Create connection object and retrieve file contents.
# # Specify input format is a csv and to cache the result for 600 seconds.
# conn = st.connection('gcs', type=FilesConnection)
# df = conn.read("streamlit-bucket/fake-detector/images/fake-detector-bg.jpeg", input_format="csv", ttl=600)

# Set the background
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://storage.cloud.google.com/fake-detector/images/fake-detector-bg.jpeg");
# background-size: cover;
# }
# </style>
# '''

# st.markdown(page_bg_img, unsafe_allow_html=True)

# Let the user upload a file
# Variable to store uploaded images
uploaded_images = st.file_uploader("Upload your image:", accept_multiple_files=True, type=["png", "jpg"])

for uploaded_file in uploaded_images:
    bytes_data = uploaded_file.read()
