# Imaris_2_Tiff-Converter
A small Python script and executable that takes an ims file and converts it to an tiff file.
The images can be saved as 16bit tiffs or as 8-bit images either scaled or unscaled.

## NOTE
The script reads resolution_level = 0 (full resolution) from the ims file and transposes the 5D array from TCZYX to TZCYX.
The new array is saved useing tifffile.imwrite()
In the current version, only the XY pixel size is stored in the tiff metadata.

# Building and using an executable
To convert multiple images without Python experience, you can create a small executable. 
This allows batch conversion of multiple ims files.

## Build
```
pip install pyinstaller
cd path\to\the\Ims2tiff_converter and scaler.py
pyinstaller --onefile Ims2tiff_converter and scaler.py
```

## Usage
- Run the Python executable from the dist folder (dist/IMS_to_TIFF_16bit.exe)
- **Load Image** -> Multiple IMS files can be loaded simultaneously
- **Select Scaling mode**
    - **16-bit:** Saves images in raw intensity format
    - **8-bit:** Converts images and stacks to 8-bits without scaling
    - **8-bit Scaled:** Converts images and stacks to 8-bits by linearly scaling from min-max to 0-255
- **Select output folder**
- Click **Run**

> [!CAUTION]
> Make sure the image conversion has worked correctly.

> [!NOTE]
> Large files may not work depending on available RAM.

# Code
For documentation purposes I have added the Python file and a Jupyter notebook.
