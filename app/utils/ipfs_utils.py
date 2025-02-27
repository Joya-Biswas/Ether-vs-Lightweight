import json
import requests
from dotenv import load_dotenv

# IPFS API endpoint (default for local node)
IPFS_API_URL = "http://localhost:5001/api/v0"

def upload_to_ipfs(name, file):
    try:
        # Add file to IPFS
        add_endpoint = f"{IPFS_API_URL}/add"
        
        # Create a dictionary with the file to be uploaded
        files = {
            'file': (name, file)
        }
        
        # Make the request to the local IPFS node
        response = requests.post(add_endpoint, files=files)
        
        # Parse the response
        if response.status_code == 200:
            result = json.loads(response.text)
            ipfs_hash = result.get("Hash")
            print(f"File uploaded to local IPFS node. IPFS Hash (CID): {ipfs_hash}")
            
            # Optional: Pin the file to ensure it persists in your local node
            pin_endpoint = f"{IPFS_API_URL}/pin/add?arg={ipfs_hash}"
            requests.post(pin_endpoint)
            print(f"File pinned locally")
            
            return ipfs_hash
        else:
            print(f"Error uploading to IPFS: Status code {response.status_code}")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error uploading to IPFS: {str(e)}")
        return None