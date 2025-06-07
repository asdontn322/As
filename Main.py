import logging
import time
import subprocess

LOG_FILE = "logs/automation.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_step(name, script):
    logging.info(f"STEP START: {name}")
    try:
        result = subprocess.run(["python", script], check=True)
        logging.info(f"STEP SUCCESS: {name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"STEP FAILED: {name} with error {e}")
    time.sleep(2)

if __name__ == "__main__":
    logging.info("=== FULL AUTOMATION STARTED ===")
    
    run_step("Download Excel from Legacy Website", "automate.py")
    run_step("Upload to SharePoint", "upload_to_sharepoint.py")
    run_step("Upload to Google Cloud Platform", "upload_to_gcp.py")
    
    logging.info("=== FULL AUTOMATION COMPLETED ===")
