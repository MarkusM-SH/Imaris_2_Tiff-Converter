# Imaris_2_Tiff-Converter
A small Python script and executable that takes an ims file and converts it to an tiff file.

## NOTE
The script reads resolution_level = 0 (full resolution) from the ims file and transposes the 5D array from TCZYX to TZCYX.
The new array is saved useing tifffile.imwrite()
In the current version, only the XY pixel size is stored in the tiff metadata.

# USAGE Executable
For batch processing
- Download the Imaris_to_tiff folder
- Run the Python executable (dist\IMS_to_TIFF_16bit\IMS_to_TIFF_16bit.exe)
- Load several IMS files
- Define the output folder
- Click Run
- Make sure the image conversion has worked correctly

!Large files may not work depending on available RAM.

# Code
For documentation purposes I added the Python file and a Jupyter notebook.

