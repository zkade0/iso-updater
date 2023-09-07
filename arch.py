import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin
from tqdm import tqdm  # Import tqdm for progress bar

# Function to get the latest Arch Linux ISO download link
def get_latest_arch_iso_link(base_url):
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the link with the most recent ISO file
        links = soup.find_all('a', href=True)
        iso_links = [link['href'] for link in links if link['href'].endswith('.iso')]
        if iso_links:
            # Return the complete URL using urljoin
            return urljoin(base_url, iso_links[0])
    return None

# Function to extract the Arch Linux version from the ISO file name
def extract_arch_version(iso_file_name):
    match = re.search(r'archlinux-(\d{4}.\d{2}.\d{2})-', iso_file_name)
    if match:
        return match.group(1)
    return None

# Function to compare dates in YYYY.MM.DD format
def compare_dates(date_str1, date_str2):
    date1 = datetime.strptime(date_str1, '%Y.%m.%d')
    date2 = datetime.strptime(date_str2, '%Y.%m.%d')
    return date1 > date2

# Function to download a file and save it to the local directory with a progress bar
def download_file_with_progress(url, local_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(local_path, 'wb') as file, tqdm(
        desc=local_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

    return True

# Specify the local directory where you want to save the ISO file
directory = input("Enter the path to your local directory: ")

# Ensure the directory exists
if not os.path.isdir(directory):
    print("Invalid directory path. Please provide a valid directory path.")
else:
    # Define the base URL for Arch Linux ISOs
    base_url = "https://geo.mirror.pkgbuild.com/iso/latest/"

    # Get the link to the latest Arch Linux ISO
    latest_iso_link = get_latest_arch_iso_link(base_url)

    if latest_iso_link:
        print(f"Latest Arch Linux ISO Link: {latest_iso_link}")

        # Extract the ISO file name from the URL
        iso_file_name_url = latest_iso_link.split('/')[-1]

        # Extract the Arch Linux version from the ISO file name
        arch_version_url = extract_arch_version(iso_file_name_url)

        if arch_version_url:
            print(f"Arch Linux Version (URL): {arch_version_url}")

            # Check if a local ISO file exists
            local_iso_path = os.path.join(directory, iso_file_name_url)
            if os.path.exists(local_iso_path):
                # Extract the Arch Linux version from the local ISO file name
                arch_version_local = extract_arch_version(iso_file_name_url)

                if arch_version_local:
                    print(f"Arch Linux Version (Local): {arch_version_local}")

                    # Compare the dates
                    if compare_dates(arch_version_url, arch_version_local):
                        print("The version in the URL is newer.")
                    else:
                        print("The version in the local file name is newer or the same.")
                        print("Downloading the newer version...")
                        download_file_with_progress(latest_iso_link, local_iso_path)
                else:
                    print("Failed to extract Arch Linux version from the local ISO file name.")
            else:
                print("Local ISO file does not exist. Downloading the latest version...")
                download_file_with_progress(latest_iso_link, local_iso_path)
        else:
            print("Failed to extract Arch Linux version from the URL.")
    else:
        print("Failed to retrieve the latest Arch Linux ISO link.")