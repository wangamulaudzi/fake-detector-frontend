# Front-end for the fake-detector app using streamlit
# By: Wanga Mulaudzi
# June 2024

# Import statements
import gcsfs # For accessing GCP storage
import json # For loading google credentials
import os # For operating system operations
import requests # For handling API calls
import streamlit as st # For the frontend

# Function to create formatted HTML string
def create_html_text(reveal, text, color):
    """
    HTML text for displaying the classification

    Parameters:
        reveal: The classification of the image
        text: The probability
        color: Color of the text

    Returns:
        The HTML string
    """
    html_string = f'''
        <p style="text-align: center; font-size: 32px; color: {color};">{reveal}</p>
        <p></p>
        <p style="text-align: center; font-size: 25px; color: black;">{text}% confidence</p>
        '''

    return html_string

def get_gcs_credentials():
    """
    Get google cloud storage credentials
    """
    if "GCS_CREDENTIALS" in os.environ:
        # Production: Read from the environment variable
        try:
            return json.loads(os.environ["GCS_CREDENTIALS"])
        except json.JSONDecodeError as e:
            return None

    else:
        # Local development: Use Streamlit secrets
        return st.secrets["google"]["credentials"]

def main(bg_img_path, backend_url):
    ######################
    # For the background #
    ######################

    credentials_dict = get_gcs_credentials()

    # Initialize GCSFileSystem with the credentials
    fs = gcsfs.GCSFileSystem(token=credentials_dict)

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
        st.markdown("## Who better to judge AI than AI itself?")

        st.markdown('''
                    In a twist of fate (and a pinch of irony), you can now use AI to unravel the mystery of AI-generated vs. real images of people. Gone are the days of trusty human eyes — now it’s up to our digital detective to sift through the pixels and decide: real or deepfake?

                    Join in on this journey where algorithms play detective. Upload an image, sit back, and let our AI unravel the digital riddles that blur the line between what’s real and what’s artificial.

                    Ready to witness AI’s judgment? Upload your image and let AI be the judge!
                    ''')

        ########################
        # Handle image uploads #
        ########################

        # Let the user upload a file
        # Variable to store uploaded images
        uploaded_image = st.file_uploader(label="Upload your suspect", accept_multiple_files=False,
                                        type=["png", "jpg", "jpeg"])

        #############################
        # Handle the uploaded_image #
        #############################
        if uploaded_image:
            # Display the uploaded image
            st.image(uploaded_image, caption="Your uploaded image.", use_column_width=True)

            st.write("")
            with st.spinner("Classifying..."):

                # Convert the uploaded image to bytes
                bytes_data = uploaded_image.read()

                # Make the API call to the backend
                response = requests.post(
                    backend_url + "api/upload_and_predict",
                    files={"file": ("image.jpg", bytes_data, "image/jpeg")},
                    timeout=180
                )

            data = response.json()

            if data["prediction"] == "Real":
                # Using Markdown with inline HTML for custom styling
                html_text = create_html_text(data["prediction"]+"!", str(int(data["real_probability"]*100)), "green")
                st.markdown(html_text, unsafe_allow_html=True)

            else:
                # Using Markdown with inline HTML for custom styling
                html_text = create_html_text(data["prediction"]+"!", str(int(data["fake_probability"]*100)), "red")
                st.markdown(html_text, unsafe_allow_html=True)

        footer = st.container()
        with footer:
            st.markdown("---")
            st.markdown("<p style='text-align: center; color: grey; font-style: italic;'>Disclaimer: This detector is only 80% accurate and is for recreational purposes only.</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    #############
    # Variables #
    #############
    bg_img_path = "fake-detector/images/fake-detector-bg.jpeg" # Path to background image on GCP
    # backend_url = "http://127.0.0.1:8080/"
    backend_url = "https://fake-detector-backend-sfbmb7r2wa-ew.a.run.app/"

    main(bg_img_path, backend_url)
