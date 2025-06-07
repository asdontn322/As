import os
import logging
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables (you must set these in .env)
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_USERNAME = os.getenv("SHAREPOINT_USERNAME")
SHAREPOINT_PASSWORD = os.getenv("SHAREPOINT_PASSWORD")
SHAREPOINT_DOC_LIB = os.getenv("SHAREPOINT_DOC_LIB")  # e.g., "Shared Documents"
SHAREPOINT_TARGET_FOLDER = os.getenv("SHAREPOINT_TARGET_FOLDER", "")  # e.g., "AutomationUploads"

DOWNLOAD_DIR = os.path.abspath("download_folder")
LOG_FILE = "logs/automation.log"

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def upload_to_sharepoint():
    try:
        files = sorted(
            [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)],
            key=os.path.getmtime,
            reverse=True
        )

        if not files:
            logging.warning("No files found to upload to SharePoint.")
            return

        latest_file = files[0]
        filename = os.path.basename(latest_file)

        ctx_auth = AuthenticationContext(SHAREPOINT_SITE_URL)
        if ctx_auth.acquire_token_for_user(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD):
            ctx = ClientContext(SHAREPOINT_SITE_URL, ctx_auth)
            target_folder = ctx.web.lists.get_by_title(SHAREPOINT_DOC_LIB).root_folder
            if SHAREPOINT_TARGET_FOLDER:
                target_folder = target_folder.folders.get_by_url(SHAREPOINT_TARGET_FOLDER)

            with open(latest_file, 'rb') as content_file:
                file_content = content_file.read()

            target_file = target_folder.upload_file(filename, file_content).execute_query()
            logging.info(f"Uploaded {filename} to SharePoint at {target_file.serverRelativeUrl}")
        else:
            logging.error("SharePoint authentication failed.")

    except Exception as e:
        logging.error(f"SharePoint upload failed: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting SharePoint upload.")
    upload_to_sharepoint()
    logging.info("SharePoint upload completed.")
