import argparse
import os
import logging as log
from pydicom import dcmread
from Utils.Finder import DicomFinder

def parse_args():
    parser = argparse.ArgumentParser(description='Training Process of Low-dose Tau PET Enhancement Project')
    parser.add_argument(
        '--GLpath', default='', dest='glpath', help='Path to the root directory of software "MRIcroGL"', type=str)
    parser.add_argument(
        '--dcmroot', default='', dest='inmainfolder', help='Path to the root directory of dicom files.', type=str)
    parser.add_argument(
        '--outdir', default='', dest='outmainfolder', help='Path to the output directory for nifti files', type=str)
    args, rest = parser.parse_known_args()
    return args, rest

def main():

    args, restargs = parse_args()

    # Define paths and command options
    inmainfolder = args.inmainfolder
    outmainfolder = args.outmainfolder
    glpath = args.glpath
    cmd = {
        'exe': os.path.join(glpath, 'Resources', 'dcm2niix'),
        'para': '-a n -z n'  # options of MRIcroGL commands
    }
    assert isdir(glpath, inmainfolder), NotADirectoryError(f'These path should be directories, but got \n  GLpath: "{glpath}"\n  dcmroot: "{inmainfolder}"')
    
    # Create output folder
    os.makedirs(outmainfolder, exist_ok=True)

    # Record errors
    errors = []

    # Find dicom files under the root
    print('*\n*\n----START----\n')
    dicom_path_dict = DicomFinder().find(inmainfolder) 
    for dcm in dicom_path_dict:

        # Check modality in dicom header
        print(f'Processing {dcm["subject"]}...')
        try:
            dicom_info = dcmread(dcm["path"])
        except:
            errors.append(f' Encountering an error when reading DICOM file of {dcm["subject"]}. Please check {dcm["path"]}.')
            continue
        try:
            MOD = dicom_info.Modality
        except:
            errors.append(f' No attribute named "Modality" in DICOM header of {dcm["subject"]}. Please check {dcm["path"]}.')
            continue

        # Create subfolder for each modality under the output folder
        outfolder = os.path.join(outmainfolder, MOD)
        os.makedirs(outfolder, exist_ok=True)

        # Execute the MRIcroGL dcm2niix command line
        command = f'{cmd["exe"]} {cmd["para"]} -f {dcm["subject"]} -o \"{outfolder}\" \"{dcm["folder"]}\"'
        print(f'\nConverting {MOD} of {dcm["subject"]}...')
        os.system(command)

    # Print errors
    if len(errors)>0:
        print('\n**Errors**')
        for msg in errors:
            log.warning(msg)
            print()

    print('*\n*\n----FINISHED----\n')

def isdir(*path) -> bool:
    for p in path:
        if not os.path.isdir(p):
            return False
    return True

if __name__ == "__main__":
    main()
