import os
from dotenv import load_dotenv

try:
    load_dotenv()

    HOST = os.getenv('EMAIL_HOST')
    PORT = os.getenv('EMAIL_PORT')
    SENDER = os.getenv('EMAIL_SENDER')
    PASSWORD = os.getenv('EMAIL_PASSWORD')

except Exception as e:
    print(f'Error loading env variables: {e}')
    exit(1)
