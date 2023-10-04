import os
import subprocess

# Define the file path
file_path = 'cand.txt'  # Replace with the actual path to your text file

# Get the current directory
current_directory = os.getcwd()

# Initialize an empty list to store filterbank files
filterbank_files = []

# Iterate through all files in the current directory
for filename in os.listdir(current_directory):
    # Check if the file has a .fil extension
    if filename.endswith(".fil"):
        # If it does, add the file to the list
        filterbank_files.append(filename)

# Print the list of filterbank files
print("Filterbank Files:")
for file in filterbank_files:
    print(file)

def prepfoldm(n, p, DM, name, filterbank_file):
    command = f"prepfold -n {n} -topo -nopdsearch -p {p} -dm {DM} -noxwin -o {name} {filterbank_file}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)

# Open the file for reading
with open(file_path, 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line starts with 'psb'
        if line.startswith('psb'):
            # Split the line by whitespace
            parts = line.split()
            
            # Extract the desired information and convert it to the desired format
            if len(parts) >= 8:
                name = parts[0]
                DM = float(parts[1])
                p = float(parts[7]) / 1000

                # Determine the value of 'n' based on the range of DM
                if 4 <= DM <= 8:
                    n = 16
                elif 8 < DM <= 32:
                    n = 16
                elif DM >= 32:
                    n = 128

                # Call the prepfoldm function with the extracted parameters
                prepfoldm(n, p, DM, name, filterbank_files[0])  # Replace [0] with the appropriate index
