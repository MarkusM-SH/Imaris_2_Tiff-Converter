from imaris_ims_file_reader.ims import ims
import numpy
from tifffile import imwrite
import tkinter as tk
from tkinter import filedialog
import os

class ImageProcessorUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Convert IMARIS to Tiff")

        # Set the size of the window (width x height)
        self.master.geometry("500x340")

        ### change font size of button
        button_font = ("Helvetica", 16)
        
        self.load_button = tk.Button(master, text="Load Image", command=self.load_image, font=button_font)
        self.load_button.pack(pady=20)

        # Add an explanation label under the Scaling button
        explanation_text = "Convert all IMS files to tiff in 16bit full resolution"
        self.explanation_label = tk.Label(master, text=explanation_text, wraplength=400, justify="center")
        self.explanation_label.pack()

        self.output_button = tk.Button(master, text="Select Output Folder", command=self.select_output_folder, font=button_font)
        self.output_button.pack(pady=10)

        self.run_button = tk.Button(master, text="Run", command=self.run_code, font=button_font)
        self.run_button.pack(pady=10)

    def load_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Imaris Image Files", "*.ims")])
        if file_paths:
            self.img_list = [ims(file_path) for file_path in file_paths]
            print("Images loaded successfully.")

    def select_output_folder(self):
        output_folder = filedialog.askdirectory()
        if output_folder:
            self.output_folder = output_folder
            print("Output folder selected:", self.output_folder)

    def run_code(self):
        if hasattr(self, 'img_list') and hasattr(self, 'output_folder'):
            for img in self.img_list:
                def get_axis_labels(shape):
                    axis_labels = ['T', 'C', 'Z', 'X', 'Y']
                    non_singular_axes = [axis_labels[i] for i in range(5) if shape[i] > 1]
                    return ''.join(non_singular_axes)

                def convert_to_TZCXY(img): 
                    a= img[:,:,:,:,:] 
                    if get_axis_labels(img.shape) == 'TCZXY':
                        a =numpy.transpose(a, (0, 2, 1, 4, 3))    
                    elif get_axis_labels(img.shape) == 'TCXY':   
                        a = numpy.expand_dims(a, axis=(1))
                    elif get_axis_labels(img.shape) == 'TZXY':   
                        a = numpy.expand_dims(a, axis=(2))
                    elif get_axis_labels(img.shape) == 'CZXY':
                        a =numpy.transpose(a, (1,0,2,3))
                        a = numpy.expand_dims(a, axis=(0))
                    elif get_axis_labels(img.shape) == 'ZXY':
                        a = numpy.expand_dims(a, axis=(0,2)) 
                    elif get_axis_labels(img.shape) == 'CXY':
                        a = numpy.expand_dims(a, axis=(0,1))
                    elif get_axis_labels(img.shape) == 'TXY':
                        a = numpy.expand_dims(a, axis=(1,2))
                    elif get_axis_labels(img.shape) == 'XY':
                        a = numpy.expand_dims(a, axis=(0,1,2))
                    return a

                # Generate output filename based on the IMS file name
                file_name = os.path.splitext(os.path.basename(img.fileName))[0]
                output_path = os.path.join(self.output_folder, f"{file_name}.tif")

                imwrite(
                    output_path,
                    convert_to_TZCXY(img),
                    imagej=True,
                    resolution=tuple(1 / value for value in img.resolution[1:3]),
                    metadata={'axes': 'TZCYX',
                        'spacing': img.resolution[0],
                            'unit': 'um',}
                )    
                
                print(f"Image '{file_name}' saved successfully.")

        else:
            print("Please load images and select an output folder before running the code.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorUI(root)
    root.mainloop()
