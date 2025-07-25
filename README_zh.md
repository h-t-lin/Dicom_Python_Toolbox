# DICOM Python Toolbox

本工具箱主要提供兩大功能：**DICOM 轉換為 NIfTI 格式**，以及**從 DICOM 標頭提取指定資訊並匯出為 Excel 檔案**。

## 功能特色

-   **DICOM 轉 NIfTI 格式**：可批次將 DICOM 影像轉換成 NIfTI 格式（參見 `Dicom2Nifti.py`）。
-   **DICOM 標頭資訊提取**：擷取指定 DICOM 標頭屬性，並匯整成 Excel 檔案（參見 `DicomHeader_Reader.py`）。

## 最新更新（25/03/14）

-   新增支援新的 DICOM 資料夾結構
-   新增 NIfTI 輸出資料夾結構說明
-   改善錯誤處理：若 DICOM 讀取失敗將跳出警告，而不會造成程式當機

## 環境需求

-   Python==3.8
-   pydicom==2.4.3
-   pandas==1.5.3
-   MRIcroGL（DICOM to NIfTI 轉檔需用）

## 安裝步驟

1.  複製（clone）此專案：

    ```
    git clone https://github.com/h-t-lin/Dicom_Python_Toolbox.git
    ```

2.  進入專案資料夾：

    ```
    cd Dicom_Tools
    ```

3.  安裝所需 Python 套件：

    ```
    pip install -r requirements.txt
    ```

4.  請確認 MRIcroGL 已安裝，且已知其資料夾路徑（通常名稱為 MRIcroGL）。
    下載網址：[MRIcroGL](https://www.nitrc.org/projects/mricrogl "www.nitrc.org/projects/mricrogl")

## 使用方法

### 1. 使用 `Dicom2Nifti.py` 進行 DICOM to NIfTI 轉檔

執行下列指令可將批次 DICOM 檔轉成 NIfTI 格式：
```bash
python Dicom2Nifti.py --GLpath <MRIcroGL_path> --dcmroot <dicom_root_path> --outdir <output_directory>
```
-   `--GLpath`：MRIcroGL 安裝資料夾路徑
-   `--dcmroot`：DICOM 檔案資料夾路徑（見下方「DICOM 資料夾結構與 NIfTI 輸出格式」）
-   `--outdir`：NIfTI 檔案輸出資料夾

### 2. 使用 `DicomHeader_Reader.py` 進行 DICOM 標頭資訊提取

執行下列指令可提取 DICOM 標頭資訊並匯出至 Excel 檔：
```bash
python DicomHeader_Reader.py --mod <modality> --dcmroot <dicom_root_path> --outdir <output_directory>
```

-   `--mod`：指定影像模態（如 MR、CT、PT），必須為 **mods.yaml** 所列之型態之一
-   `--dcmroot`：DICOM 檔案資料夾路徑（見下方「DICOM 資料夾結構與 NIfTI 輸出格式」）
-   `--outdir`：Excel 檔案輸出資料夾

本程式使用兩個設定檔：

-   `mods.yaml`：列出可用的影像模態（modality）
-   `header_attr.yaml`：指定要提取的 DICOM 標頭屬性，可自行擴充

## DICOM 資料夾結構與 NIfTI 輸出格式

本工具箱支援四種主要的 DICOM 資料夾結構（也可混合使用）。可參考工具箱內的 `Dicom_rootdir_examples` 範例資料夾。

支援的結構如下：

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
    ```
    # Output NIfTI
    outdir/
    ├── Series1Modality
    │   ├── <Subject1>.nii
    │   ├── <Subject2>.nii
    │   └── ...
    ├── Series2Modality
    │   ├── <Subject1>.nii
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
    ```
    # Output NIfTI
    outdir/
    └── SeriesModality
        └── <Subject1>.nii
        ├── <Subject2>.nii
        └── ...
    ```

3.  **Single Subject DICOM:**

    ```
    Dicom_rootdir_example_3/
    ├── dicom001.dcm
    ├── dicom002.dcm
    └── ...
    ```
    ```
    # Output NIfTI
    outdir/
    └── SeriesModality
        └── <Date-Time>.nii
    ```

4.  **Subjects-(AuxiliaryDirs)-DICOM:**  
    *There can be multiple layers of AuxiliaryDirs.*

    ```
    Dicom_rootdir_example_4/
    ├── Subject1/
    │   ├── AuxiliaryDir1/
    │   │   ├── AuxiliaryDir1-1
    │   │   │   ├── dicom001.dcm
    │   │   │   ├── dicom002.dcm
    │   │   │   └── ...
    │   │   └── AuxiliaryDir1-2
    │   │       ├── dicom001.dcm
    │   │       └── ...
    │   └── AuxiliaryDir2/
    │       ├── AuxiliaryDir2-1
    │       │   └── ...
    │       └── AuxiliaryDir2-2
    │           └── ...
    ├── Subject2/
    │   └── ...
    └── ...
    ```
    ```
    # Output NIfTI
    outdir/
    ├── Series1Modality
    │   ├── <Subject1>.nii
    │   ├── <Subject1>a.nii
    │   ├── <Subject2>.nii
    │   ├── <Subject2>a.nii
    │   └── ...
    ├── Series2Modality
    │   ├── <Subject1>.nii
    │   ├── <Subject1>a.nii
    │   └── ...
    └── ...
    ```

    Note: NIfTI filenames will be suffixed with a, b, c if multiple DICOM series of the same modality exist.  

5.  ***不推薦的資料夾結構***  
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

    註：此結構易造成輸出混亂，**不建議使用**

## 工具箱檔案說明

-   `Dicom2Nifti.py`：DICOM 轉 NIfTI 格式腳本
-   `DicomHeader_Reader.py`：DICOM 標頭資訊擷取腳本
-   `mods.yaml`：影像模態設定檔
-   `header_attr.yaml`：標頭屬性設定檔
-   `requirements.txt`：Python 套件需求
-   `Utils/Finder.py`：DICOM 檔案搜尋工具
-   `Utils/SnL.py`：檔案存取（JSON, YAML）工具

<!-- ## 貢獻方式

（說明如何參與本專案貢獻）

## 授權

（請補充授權資訊）

## 聯絡方式

（請補充聯絡方式） -->