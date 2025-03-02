import argparse
import warnings
import os
import pandas as pd
from pydicom import dcmread
from Utils.Finder import DicomFinder
import Utils.SnL as snl

def parse_args():
    parser = argparse.ArgumentParser(description='Training Process of Low-dose Tau PET Enhancement Project')
    parser.add_argument(
        '--mod', default='', dest='modality', help='Specify the modality. (Should be one in mods.yaml)', type=str)
    parser.add_argument(
        '--dcmroot', default='', dest='infolder', help='Path to the root directory of dicom files.', type=str)
    parser.add_argument(
        '--outdir', default='', dest='outfolder', help='Path to the output directory for nifti files', type=str)
    args, rest = parser.parse_known_args()
    return args, rest

def main():

    args, restargs = parse_args()

    # Define paths
    inmainfolder = args.infolder
    outfolder = args.outfolder
    assert os.path.isdir(inmainfolder), NotADirectoryError('Invalid dicom folder.')
    assert os.path.isdir(outfolder), NotADirectoryError('Invalid output folder.')

    # Check modility
    MODALITY = args.modality
    mod_options = snl.load_yaml('mods.yaml')
    assert MODALITY != '', ValueError('Must specify the modality. Use "--mod" to input the modality.')
    assert MODALITY in mod_options, ValueError(f'Invalid modatliy "{MODALITY}".')

    # Import header attributes
    header_attr = snl.load_yaml('header_attr.yaml')
    assert isinstance(header_attr, list), RuntimeError(f'Expect loading a list from "header_attr.yaml", but got {type(header_attr)}.')

    # Find dicom files
    dicom_path_dict = DicomFinder().find(inmainfolder)

    # Function to flatten the data
    def flatten_dataset(dataset, prefix=''):
        flat_dict = {}
        for ele in dataset:
            if ele.VR == 'SQ':
                for idx, itm in enumerate(ele.value):
                    item_prefix = f"{prefix}{ele.keyword}[{idx}]."
                    flat_dict.update(flatten_dataset(itm, item_prefix))
            else:
                flat_dict[f"{prefix}{ele.keyword}"] = ele.value
        return flat_dict
    
    # Find the key with specific keyword
    def find_keyword(dct: dict, keyword: str):
        matched_keys = [key for key in dct.keys() if keyword in key]
        if len(matched_keys) > 0:
            if len(matched_keys) > 1:
                warnings.warn(f'Find more than one attrubute named with keyword {keyword}.')
            return matched_keys[0]
        return None
    
    # Extract the information
    print('*\n*\n----START----\n')
    data = []
    attr_log = set()
    
    for dcm in dicom_path_dict:
        # Read dicom header
        dicom_dataset = dcmread(dcm['path'])
        dicom_dataset.remove_private_tags()

        if dicom_dataset.Modality == MODALITY:
            dicom_info = flatten_dataset(dicom_dataset)
            infodict = {}
            infodict['Subject'] = dcm['subject']
            for attrkw in header_attr:
                try:
                    # If find an attribute named exactly same with the keyword in header_attr.
                    infodict[attrkw] = dicom_info[attrkw]
                    attr_log.add(attrkw)
                except:
                    # Find the first attribute whose name includes the keyword.
                    matched_key = find_keyword(dicom_info, attrkw)
                    if matched_key is not None:
                        infodict[attrkw] = dicom_info[matched_key]
                        attr_log.add(attrkw)
            data.append(infodict)
    
    # Print the attributes not found in dicom header
    attr_not_exist = list(set(header_attr) - attr_log)
    if len(attr_not_exist) > 0:
        attr_not_exist.sort()
        warnings.warn(f'These attributes are not found in dicom headers.\n  {attr_not_exist}')

    # Export excel file
    excel_path = os.path.join(outfolder, 'DicomHeader.xlsx')
    df = pd.DataFrame(data)
    if os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=MODALITY, index=False)
    else:
        df.to_excel(excel_path, sheet_name=MODALITY, index=False)
    print('*\nExcel file was exported successfully.')

    print('*\n*\n----FINISHED----\n')


if __name__ == "__main__":
    main()
