import os
import requests
import re

# Function to get the latest release version and download link from GitHub
def get_latest_github_release(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = requests.get(url)
    
    if response.status_code == 200:
        release_data = response.json()
        release_version = release_data['tag_name'].lstrip('v')
        assets = release_data.get('assets', [])
        
        iso_asset = None
        for asset in assets:
            if re.search(r'\.iso$', asset['name']):
                iso_asset = asset
                break
        
        if iso_asset:
            return release_version, iso_asset['browser_download_url']
    
    return None, None

# Function to download a file and save it to the local directory
def download_file(url, local_path):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        return True
    
    return False

# Input the local directory where you want to save the Linux distro file
directory = input("Enter the path to your local directory: ")

if os.path.isdir(directory):
    # Replace with the owner's name and repository name
    owner = 'ublue-os'
    repo = 'main'

    # Get the latest release version and download link from GitHub
    latest_release_version, latest_release_link = get_latest_github_release(owner, repo)

    if latest_release_version and latest_release_link:
        print(f"Latest Release Version: {latest_release_version}")

        # Extract the local version from the filenames in the directory
        local_version = None
        for filename in os.listdir(directory):
            match = re.search(r'\d{8}', filename)
            if match:
                local_version = match.group()
                break

        if latest_release_version != local_version:
            print("Downloading the latest version...")
            download_successful = download_file(latest_release_link, os.path.join(directory, os.path.basename(latest_release_link)))
            
            if download_successful:
                print("Download successful.")
            else:
                print("Download failed.")
        else:
            print("Local version is up to date.")
    else:
        print("Failed to retrieve the latest release information from GitHub.")
else:
    print("Invalid directory path. Please provide a valid directory path.")
