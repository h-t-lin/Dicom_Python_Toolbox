# DICOM Python Toolbox

This toolbox provides two main functions for processing DICOM files: converting DICOM files to NIfTI format and extracting specific information from DICOM headers into an Excel file.

## Features

-   **DICOM to NIfTI Conversion**: Converts batches of DICOM files to NIfTI format. (See `Dicom2Nifti.py`)
-   **DICOM Header Extraction**: Extracts specified attributes from DICOM headers and compiles them into an Excel file. (See `DicomHeader_Reader.py`)

## Requirements

-   Python==3.8
-   pydicom==2.4.3
-   pandas==1.5.3
-   MRIcroGL (for DICOM to NIfTI conversion)

## Installation

1.  Clone the repository:

    ```
    git clone https://github.com/h-t-lin/Dicom_Python_Toolbox.git
    ```

2.  Navigate to the project directory:

    ```
    cd Dicom_Tools
    ```

3.  Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

4.  Ensure MRIcroGL is installed and the path to its root directory *(usually named MRIcroGL)* is known.  
    Download page: [MRIcroGL](https://www.nitrc.org/projects/mricrogl "www.nitrc.org/projects/mricrogl")

## Usage

### 1. DICOM to NIfTI Conversion with `Dicom2Nifti.py`

Use the command to converts batches of DICOM files to NIfTI format.
```bash
python Dicom2Nifti.py --GLpath <MRIcroGL_path> --dcmroot <dicom_root_path> --outdir <output_directory>
```
-   `--GLpath`: Path to the root directory of MRIcroGL.
-   `--dcmroot`: Path to the root directory of the DICOM files. (See next section **DICOM Directory Structure**)
-   `--outdir`: Path to the output directory for the NIfTI files.

### 2. DICOM Header Extraction with `DicomHeader_Reader.py`

Use the command to extract DICOM header information and export it to an Excel file.
```bash
python DicomHeader_Reader.py --mod <modality> --dcmroot <dicom_root_path> --outdir <output_directory>
```

-   `--mod`: Specify the modality (e.g., MR, CT, PT). Must be one of the modalities listed in **mods.yaml**.
-   `--dcmroot`: Path to the root directory of the DICOM files. (See next section **DICOM Directory Structure**)
-   `--outdir`: Path to the output directory for the Excel file.

The script uses two configuration files:

-   `mods.yaml`: Lists the available modalities.
-   `header_attr.yaml`: Lists the DICOM header attributes to extract. You can add more attributes to this file as needed.

## DICOM Directory Structure

This toolbox can process DICOM files organized in three primary structures, or any combination thereof. For reference, please see the `Dicom_rootdir_examples` folder within the toolbox.

The supported structures are:

1.  **Subjects-Series-DICOM:**

    ```
    Dicom_rootdir_example_1/
    ├── Subject1/
    │   ├── Series1/
    │   │   ├── dicom001.dcm
    │   │   ├── dicom002.dcm
    │   │   └── ...
    │   └── Series2/
    │       ├── dicom001.dcm
    │       └── ...
    ├── Subject2/
    │   └── ...
    └── ...
    ```

2.  **Subjects-DICOM:**

    ```
    Dicom_rootdir_example_2/
    ├── Subject1/
    │   ├── dicom001.dcm
    │   ├── dicom002.dcm
    │   └── ...
    ├── Subject2/
    │   ├── dicom001.dcm
    │   └── ...
    └── ...
    ```

3.  **Single Subject DICOM:**

    ```
    Dicom_rootdir_example_3/
    ├── dicom001.dcm
    ├── dicom002.dcm
    └── ...
    ```

4.  ***Not Suggested Structure:***  
    **Series-Subjects-DICOM:**

    ```
    Not_suggested/
    ├── Series1/
    │   ├── Subject1/
    │   │   ├── dicom001.dcm
    │   │   ├── dicom002.dcm
    │   │   └── ...
    │   └── Subject2/
    │       ├── dicom001.dcm
    │       └── ...
    ├── Series2/
    │   └── ...
    └── ...
    ```

    This structure may lead to unclear output, and is thus **not recommended** for use.

## Toolbox File Descriptions

-   `Dicom2Nifti.py`: Script for converting DICOM files to NIfTI format.
-   `DicomHeader_Reader.py`: Script for extracting DICOM header information.
-   `mods.yaml`: Configuration file for DICOM modalities.
-   `header_attr.yaml`: Configuration file for DICOM header attributes.
-   `requirements.txt`: List of required Python packages.
-   `Utils/Finder.py`: Utility script for finding DICOM files.
-   `Utils/SnL.py`: Utility script for file saving and loading (JSON, YAML).

<!-- ## Contributing

(Add information on how to contribute to the project.)

## License

(Add license information.)

## Contact

(Add contact information.) -->