# Define the file path
file_path = 'cand.txt'  # Replace with the actual path to your text file

# Open the file for reading
with open(file_path, 'r') as file:
    # Iterate through each line in the file
    for line in file:
        # Check if the line starts with 'psb'
        if line.startswith('psb'):
            # Split the line by whitespace
            parts = line.split()
            
            # Extract the desired information and convert it to the desired format
            extracted_info = [parts[0], float(parts[1]), float(parts[7]) / 1000]
            
            # Print the extracted information as a list
            print(extracted_info) 