import requests
import os

def download_file_with_auth(url, filename, access_token=None):
    """
    Downloads a file from a given URL, optionally using an access token for authentication.

    Args:
        url (str): The URL of the file to download.
        filename (str): The local filename to save the downloaded file as.
        access_token (str, optional): An access token for authentication (e.g., Bearer token).
                                     Defaults to None for unauthenticated downloads.
    """
    headers = {}
    if access_token:
        headers['Authorization'] = f'Bearer {access_token}'
        print("Using authentication with provided access token.")
    else:
        print("Downloading without explicit authentication.")

    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    f.write(chunk)
        print(f"File '{filename}' downloaded successfully.")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing file '{filename}': {e}")

# --- Demo Usage ---
if __name__ == "__main__":
    # Example 1: Downloading a public file (no authentication)
    public_url = "https://www.example.com/some_public_file.txt" # Replace with a real public URL
    public_filename = "public_file.txt"
    # Create a dummy file for demonstration if the URL isn't real
    if not requests.head(public_url).ok:
        with open(public_filename, 'w') as f:
            f.write("This is a public file content.")
        print(f"Created dummy file: {public_filename}")
        public_url = os.path.abspath(public_filename) # Use local path for dummy file download

    download_file_with_auth(public_url, public_filename)

    # Example 2: Downloading a file with a dummy access token
    # In a real scenario, you would obtain this access_token through an OAuth flow or similar.
    authenticated_url = "https://api.example.com/protected_resource/data.zip" # Replace with a real protected URL
    authenticated_filename = "protected_data.zip"
    dummy_access_token = "your_dummy_access_token_here" # Replace with a real token if testing against an API

    print("\n--- Attempting authenticated download ---")
    download_file_with_auth(authenticated_url, authenticated_filename, dummy_access_token)

    # Clean up dummy file if created
    if os.path.exists(public_filename) and public_url == os.path.abspath(public_filename):
        os.remove(public_filename)
        print(f"Removed dummy file: {public_filename}")
