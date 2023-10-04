import os
import shutil

# Define the root directory to start the search
root_directory = '/path/to/root/directory'  # Replace with your root directory path

# Define the folder where you want to move the files
output_folder = '/path/to/output/folder'  # Replace with your desired output folder path

# Iterate through all directories and subdirectories
for root, dirs, files in os.walk(root_directory):
    for filename in files:
        # Check if the file has a .fil extension
        if filename.endswith(".fil"):
            fil_file = os.path.join(root, filename)  # Full path to the .fil file
            
            # Find the corresponding .txt file with the same name
            txt_file = os.path.join(root, filename.replace(".fil", ".txt"))
            
            # Check if the .txt file exists
            if os.path.exists(txt_file):
                # Create a folder with the name of the .fil file (without extension)
                output_subfolder = os.path.join(output_folder, os.path.splitext(filename)[0])
                os.makedirs(output_subfolder, exist_ok=True)
                
                # Move both .fil and .txt files to the output folder
                shutil.move(fil_file, os.path.join(output_subfolder, filename))
                shutil.move(txt_file, os.path.join(output_subfolder, filename.replace(".fil", ".txt")))

# Print a message when the process is complete
print("Files moved and renamed successfully.")
