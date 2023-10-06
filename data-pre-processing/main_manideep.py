import os
import subprocess
import shutil
import chardet
import logging

# Logging Function
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

# Function building

# create directory
def create_directory(directory_path):
    logging.info('Executing create_directory function')
    try:
        os.mkdir(directory_path)
        print("Directory created successfully.")
    except OSError as e:
        print("Directory creation failed:", e)
# create_directory("./mum")

# moving files to a directory
def move_files_to_dir(source_dir, target_dir, extension):
    logging.info('Executing move_files_to_dir function')
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    # Get a list of files with the specified extension in the source directory
    files_to_move = [file for file in os.listdir(source_dir) if file.endswith(extension)]
    
    for file in files_to_move:
        source_file = os.path.join(source_dir, file)
        target_file = os.path.join(target_dir, file)
        
        try:
            shutil.move(source_file, target_file)
            print(f"Moved {file} to {target_dir}")
        except Exception as e:
            print(f"Failed to move {file}: {e}")
# move_files_to_dir("./", "./mum", "config.txt")


# to get the name of filterbank file
def get_filenames(directory):
    logging.info('Executing get_filenames function')
    txt_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.fil'):
                txt_files.append(file)
    return txt_files[0]
# print(get_filenames("./")


# reading config data
def read_config_data(option):
    logging.info('Executing read_config_data function')
    # Open the file
    with open("./config.txt", "r") as file:
        # Read the contents of the file
        contents = file.read()

        # Search for the line that contains "option"
        for line in contents.split('\n'):
            if option in line:
                # Extract the value from the line
                value = line.split('=')[-1].strip()
                break
        else:
            # Handle the case where the line is not found
            value = None
        
        return value
# print(read_config_data("Name"))



# PRESTO Functions

# rficlean
def rficlean():
    logging.info('Executing rficlean')
    filename = get_filenames("./")
    command = f"rficlean -o rficlean.fil {filename}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# rficlean()


# prepdata
def prepdata():
    logging.info('Executing prepdata')

    filename = "rficlean.fil"
    command = f"prepdata -nobary -dm 0.0 -o pd {filename}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# prepdata()


# realfft
def realfft():
    logging.info('Executing realfft')
    filename = "pd.dat"
    command = f"realfft {filename}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# realfft()


# accelsearch
def accelsearch():
    logging.info('Executing accelsearch')
    filename = "pd.dat"
    command = f"accelsearch -numharm 4 -zmax 0 {filename}"

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)

    # Moving files to respective directories
    move_files_to_dir("./", "./prepdata_output", "pd.dat")
    move_files_to_dir("./", "./prepdata_output", "pd.fft")
    move_files_to_dir("./", "./prepdata_output", "pd.inf")
    move_files_to_dir("./", "./prepdata_output/candidate_files", "pd_ACCEL_0")
    move_files_to_dir("./", "./prepdata_output/candidate_files", "pd_ACCEL_0.cand")
# accelsearch()





# prepsubband
 def prepsubband():
     logging.info('Executing prepsubband')
     command1 = "prepsubband -nobary -nsub 16 -lodm 0.0 -dmstep 0.30 -downsamp 4 -numdms 492 -o psb rficlean.fil"
     command2 = "prepsubband -nobary -nsub 16 -lodm 147.60 -dmstep 0.50 -downsamp 8 -numdms 240 -o psb rficlean.fil"
     command3 = "prepsubband -nobary -nsub 16 -lodm 267.60 -dmstep 1.0 -downsamp 16 -numdms 264 -o psb rficlean.fil"
     command4 = "prepsubband -nobary -nsub 16 -lodm 531.60 -dmstep 3.0 -downsamp 32 -numdms 168 -o psb rficlean.fil"
     # Concatenate the commands with a semicolon to run them sequentially
     combined_commands_semicolon = f"{command1}; {command2}; {command3}; {command4}"
 
     try:
         subprocess.run(combined_commands_semicolon, shell=True, check=True)
         print("Command executed successfully.")
     except subprocess.CalledProcessError as e:
         print("Command execution failed:", e)
# # prepsubband()


# realfft
def run_realfft():
    logging.info('Executing run_realfft')
    command = "realfft *.dat"
 
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# run_realfft()


# accelsearch
def run_accelsearch():
    logging.info('Executing run_accelsearch')
    command = "ls *.fft | xargs -n 1 accelsearch"
 
    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# run_accelsearch()


# changing encoding
def change_encoding(file_extension):
    logging.info('Executing change_encoding')
    directory = "./"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath) and filename.endswith(file_extension):
            try:
                with open(filepath, 'rb') as file:
                    content = file.read()
                    result = chardet.detect(content)
                    encoding = result['encoding']
                
                with open(filepath, 'r', encoding=encoding, errors='replace') as file:
                    content = file.read()
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                print(f"File '{filename}' converted from '{encoding}' to UTF-8 encoding.")
            
            except UnicodeDecodeError:
                print(f"Error decoding file '{filename}'. Skipping the file.")
                continue
            except Exception as e:
                print(f"Error occurred while converting file '{filename}': {str(e)}")
                continue
# change_encoding()


# accelsift
def accelsift():
    logging.info('Executing accelsift')
    command = "python3 /data1/mpsurnis/soft/presto/examplescripts/ACCEL_sift.py > cands.txt" 

    try:
        subprocess.run(command, shell=True, check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Command execution failed:", e)
# accelsift()


# prepfold
def prepfold(cand_dir, dat_dir):
    logging.info('Executing prepfold')
    # Get the list of .cand and .dat files in the directories
    cand_files = [f for f in os.listdir(cand_dir) if f.endswith('.cand')]
    dat_files = [f for f in os.listdir(dat_dir) if f.endswith('.dat')]

    # Sort the lists of files
    cand_files.sort()
    dat_files.sort()

    # Iterate over the files and run prepfold on each pair
    for cand_file, dat_file in zip(cand_files, dat_files):
        # Create the command with the current pair of files
        command = ['prepfold', '-topo', '-accelcand', '1', '-accelfile', os.path.join(cand_dir, cand_file), os.path.join(dat_dir, dat_file)]

        # Run the command
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process.communicate(b'\n')
        process.wait()


# def clean_all():
#     try:
#         move_files_to_dir("./prepsubband_output", "./", ".inf")
#         move_files_to_dir("./candidate_files", "./", "00")
#         move_files_to_dir("./prepsubband_output", "./", ".dat")
#         move_files_to_dir("./prepsubband_output/realfft_output", "./", ".fft")
#         move_files_to_dir("./candidate_files", "./", ".cand")
#         move_files_to_dir("./candidate_files", "./", ".txtcand") 
#         move_files_to_dir("./rficlean_output", "./", "clean.fil")
#         move_files_to_dir("./rficlean_output", "./", ".pdat")
#         move_files_to_dir("./rficlean_output", "./", ".ps")

#     except Exception as e:
#         pass


# cleaning files
def clean_all():
    logging.info('Executing clean_all function')
    try:
        # prepsubband files
        move_files_to_dir("./", "./prepsubband_output", ".inf")
        move_files_to_dir("./", "./prepsubband_output", ".dat")
        move_files_to_dir("./", "./prepsubband_output/realfft_output", ".fft")
        # candidate files
        move_files_to_dir("./", "./candidate_files", "00")
        move_files_to_dir("./", "./candidate_files", ".cand")
        move_files_to_dir("./", "./candidate_files", ".txtcand") 
        # RFIClean files
        move_files_to_dir("./", "./rficlean_output", "rficlean.fil")
        move_files_to_dir("./", "./rficlean_output", "rficlean_output.pdat")
        move_files_to_dir("./", "./rficlean_output/ps_output", "rficlean_output.ps")
        # prepfold output
        move_files_to_dir("./", "./prepfold_output", ".pfd")
        move_files_to_dir("./", "./prepfold_output", ".pfd.ps")
        move_files_to_dir("./", "./prepfold_output", "pfd.bestprof")

    except Exception as e:
        pass
# clean_all()


if __name__ == "__main__":
    try:
        logging.info('Starting program execution')
        rficlean()
        prepdata()
        realfft()
        accelsearch()
        #ddplan()
        #replace_word_in_file("./dedisp_clean.py", "./dedisp.py", "prepsubband", "prepsubband -nobary")
        #dedisp()
        prepsubband()
        run_realfft()
        run_accelsearch()
        change_encoding("_200")
        accelsift()
        #prepfold("./", "./")
        clean_all()
        logging.info('Program executed successfully')
    except Exception as e:
        logging.exception('An error occurred: ' + str(e))
