import os
import subprocess

# User-specified directory containing ISO files
iso_directory = input("Enter the path to the directory with ISO files: ")

# Designated Python file to update ISO files
update_script = input("Enter the path to the designated Python script for updating ISO files: ")

# Function to list ISO files in the directory
def list_iso_files(directory):
    iso_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".iso"):
                iso_files.append(os.path.join(root, file))
    return iso_files

# Function to update ISO files using the designated Python script
def update_iso_file(iso_file, update_script):
    # Run the designated Python script with the ISO file as an argument
    subprocess.run(["python", update_script, iso_file], check=True)

# Main loop to process ISO files
iso_files = list_iso_files(iso_directory)
for iso_file in iso_files:
    print(f"Processing: {iso_file}")
    update_iso_file(iso_file, update_script)
    
    # Delete the old ISO file
    os.remove(iso_file)
    print(f"Deleted old ISO file: {iso_file}")

print("All ISO files have been updated and old files have been deleted.")
