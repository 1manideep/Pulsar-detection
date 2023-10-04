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
            
            # Construct the new name for the .txt file
            new_txt_name = filename.replace(".fil", ".txt")
            
            # Find the path to the existing "cands.txt" file
            cands_txt_file = os.path.join(root, "cands.txt")
            
            # Rename the "cands.txt" file to match the .fil file name
            if os.path.exists(cands_txt_file):
                new_cands_txt_file = os.path.join(root, new_txt_name)
                os.rename(cands_txt_file, new_cands_txt_file)

            # Move both .fil and .txt files to the output folder
            output_subfolder = os.path.join(output_folder, os.path.basename(root))
            os.makedirs(output_subfolder, exist_ok=True)
            shutil.move(fil_file, os.path.join(output_subfolder, filename))
            shutil.move(new_cands_txt_file, os.path.join(output_subfolder, new_txt_name))

# Print a message when the process is complete
print("Files moved and renamed successfully.")
