import matplotlib.pyplot as plt
import numpy as np
import json
import sys
sys.path.append('/data1/manideep2/code')
from CCNN import load_pfd

def plot_features(data, save_dir, figure_name):
    # Plot the sum profile
    plt.figure(figsize=(8, 4))
    plt.plot(data['sumprof'])
    #plt.title('Sum Profile')
    #plt.xlabel('Phase Bins')
    #plt.ylabel('Intensity')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'{save_dir}/{figure_name}_sum_profile.png')
    plt.close()

    # Plot the subbands
    plt.figure(figsize=(8, 4))
    plt.imshow(data['subbands'], aspect='auto', cmap='gray')
    #plt.title('Subbands')
    #plt.xlabel('Phase Bins')
    #plt.ylabel('Subbands')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'{save_dir}/{figure_name}_subbands.png')
    plt.close()

    # Plot the time vs. phase
    plt.figure(figsize=(8, 4))
    plt.imshow(data['time_vs_phase'], aspect='auto', cmap='gray')
    #plt.title('Time vs. Phase')
    #plt.xlabel('Phase Bins')
    #plt.ylabel('Time Bins')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'{save_dir}/{figure_name}_time_vs_phase.png')
    plt.close()

    # Plot the DM curve
    plt.figure(figsize=(8, 4))
    plt.plot(data['DM'])
    #plt.title('DM Curve')
    #plt.xlabel('DM Bins')
    #plt.ylabel('Normalized Dispersion Measure')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'{save_dir}/{figure_name}_DM_curve.png')
    plt.close()

#if __name__ == "__main__":
    # Replace 'your_pfd_file.pfd' with the path to your PFD file
    #pfd_file = 'psb_DM52.50_ACCEL_200:2_10.06ms_Cand.pfd'
    
    # Load PFD data and extract features
    #pfd_data = load_pfd(pfd_file)

    # Specify the directory to save the images
    #save_directory = 'output_images4'
    
    #print(pfd_data)

    # Create the output directory if it doesn't exist
    #import os
    #os.makedirs(save_directory, exist_ok=True)

    # Generate and save plots as images
    #plot_features(pfd_data, save_directory, 'my_figure_name')
