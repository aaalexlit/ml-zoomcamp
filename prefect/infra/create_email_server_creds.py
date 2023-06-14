import os
from dotenv import load_dotenv
from prefect_email import EmailServerCredentials

load_dotenv()


def create_email_server_creds_block():
    """Create a block for Gmail creds"""
    EmailServerCredentials(
        username=os.environ.get("PREFECT_CLOUD_GMAIL_ADDRESS"),
        password=os.environ.get("PREFECT_CLOUD_GMAIL_PASSWORD"),
    ).save(name='gmail-creds', overwrite=True)


if __name__ == '__main__':
    create_email_server_creds_block()
