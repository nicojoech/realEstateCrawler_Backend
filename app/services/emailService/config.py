import os
from dotenv import load_dotenv, find_dotenv

# Check if .env file exists
if not find_dotenv():
    raise FileNotFoundError("No .env file found. Please create one with the necessary configurations.")

# Load .env file
load_dotenv(find_dotenv())


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"Environment variable {name} not found. Ensure the .env file is set up correctly.")


# Get environment variables
EMAIL_SENDER = get_env_variable("EMAIL_SENDER")
EMAIL_PASSWORD = get_env_variable("EMAIL_PASSWORD")
SMTP_SERVER = get_env_variable("SMTP_SERVER")
SMTP_PORT = get_env_variable("SMTP_PORT")
