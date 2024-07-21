# Fake Detector Frontend

This is the frontend service for the Fake Detector application, built with Streamlit.

The backend repo can be found [here](https://github.com/wangamulaudzi/fake-detector-backend).

## Local Setup

1. Clone the repository:
`git clone <repository-url>`
`cd fake-news-frontend`

2. Set up a virtual environment:
`pyenv virtualenv 3.10.6 <environment-name>`
`pyenv local <environment-name>`

3. Install dependencies:
`pip install -r requirements.txt`

4. Set up Streamlit secrets:
Create a `.streamlit/secrets.toml` file and add necessary secrets.

5. Run the Streamlit app:
streamlit run fake-detector.py

The app should now be running on `http://localhost:8501`.

## Configuration

- Update the `backend_url` in `fake-detector.py` to point to your deployed backend service.
