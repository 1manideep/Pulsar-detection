#code to print out all filterbank files (with .fil extension) in a given directory
import os 
# Specify the directory path you want to search
directory_path = ''

# Specify the file extension you want to select (e.g., '.txt')
file_extension = '.fil'

# Iterate through files in the directory and print those matching the extension
for filename in os.listdir(directory_path):
    if filename.endswith(file_extension) and os.path.isfile(os.path.join(directory_path, filename)):
        print("File:", filename)
