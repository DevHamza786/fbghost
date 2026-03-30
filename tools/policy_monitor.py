import requests
from bs4 import BeautifulSoup
from loguru import logger
import hashlib
import json
import os

POLICY_URL = "https://transparency.fb.com/policies/community-standards/"

class PolicyMonitor:
    def __init__(self, storage_path="database/policy_state.json"):
        self.storage_path = storage_path
        self.last_hash = self.load_state()

    def load_state(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f).get("hash", "")
        return ""

    def save_state(self, new_hash):
        with open(self.storage_path, 'w') as f:
            json.dump({"hash": new_hash}, f)
        self.last_hash = new_hash

    def check_for_updates(self):
        """Scrapes the community standards page and checks for changes."""
        logger.info(f"Checking for policy updates at {POLICY_URL}")
        try:
            response = requests.get(POLICY_URL, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            # Extract main content to hash
            main_content = soup.find('main') or soup.body
            current_text = main_content.get_text(separator=' ', strip=True)
            current_hash = hashlib.md5(current_text.encode()).hexdigest()
            
            if current_hash != self.last_hash:
                logger.warning("META POLICY CHANGE DETECTED!")
                self.save_state(current_hash)
                return True, current_text[:1000] # Return first 1000 chars for context
            
            logger.info("No policy changes detected.")
            return False, None
            
        except Exception as e:
            logger.error(f"Error checking policy: {e}")
            return False, None

if __name__ == "__main__":
    monitor = PolicyMonitor()
    changed, snippet = monitor.check_for_updates()
    if changed:
         print(f"Policy Updated! Snippet: {snippet}")
    else:
         print("No changes.")
