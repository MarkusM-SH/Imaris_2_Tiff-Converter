from imaris_ims_file_reader.ims import ims
import numpy
from tifffile import imwrite
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class ImageProcessorUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Convert IMARIS to Tiff")
        self.master.geometry("500x400")

        button_font = ("Helvetica", 14)
        explanation_text = "Convert all IMS files to tiff with selected bit-depth"
        self.explanation_label = tk.Label(master, text=explanation_text, wraplength=400, justify="center", font=("Helvetica", 16) )
        self.explanation_label.pack()

        self.load_button = tk.Button(master, text="Load Images", command=self.load_image, font=button_font)
        self.load_button.pack(pady=10)        
        
        self.save_mode_label = tk.Label(master, text="Select Convert mode:", justify="left", font= ("Helvetica", 14))
        self.save_mode_label.pack()
        
        self.save_mode_var = tk.StringVar(value="16-bit")
        self.save_mode_dropdown = tk.OptionMenu(master, self.save_mode_var, "16-bit", "8-bit", "8-bit Scaled")
        self.save_mode_dropdown.pack(pady=10)
        
        explanation_text2 = "• 16-bit: Saves images in raw intensity format\n" \
                            "• 8-bit: Converts images and stacks to 8-bits without scaling\n" \
                            "• 8-bit Scaled: Converts images and stacks to 8-bits by linearly scaling from min-max to 0-255"
        self.explanation_label2 = tk.Label(master, text=explanation_text2, wraplength=400, justify="left", font=("Helvetica", 10) )
        self.explanation_label2.pack(pady=10)


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
            mode = self.save_mode_var.get()
            messagebox.showinfo("Save Mode Selected", f"Here is the text for {mode}")
            
            for img in self.img_list:
                def get_axis_labels(shape):
                    axis_labels = ['T', 'C', 'Z', 'X', 'Y']
                    non_singular_axes = [axis_labels[i] for i in range(5) if shape[i] > 1]
                    return ''.join(non_singular_axes)
                
                def convert_to_8bit(a, mode):
                    a = a.astype(numpy.float32)
                    if mode == "8-bit":
                        a = (a / (2**16 - 1)) * 255

                    else:  # "8-bit Max-Scaled"                                       
                        for i in range(a.shape[2]):
                            b = a[:, :, i, :, :]
                            b = b-b.min()
                            a[:, :, i, :, :]= ( b / b.max()) * 255
                        
                    return a.astype(numpy.uint8)
                
                def convert_to_TZCXY(img):
                    a = img[:, :, :, :, :]
                    if get_axis_labels(img.shape) == 'TCZXY':
                        a = numpy.transpose(a, (0, 2, 1, 4, 3))    
                    elif get_axis_labels(img.shape) == 'TCXY':   
                        a = numpy.expand_dims(a, axis=(1))
                    elif get_axis_labels(img.shape) == 'TZXY':   
                        a = numpy.expand_dims(a, axis=(2))
                    elif get_axis_labels(img.shape) == 'CZXY':
                        a = numpy.transpose(a, (1, 0, 2, 3))
                        a = numpy.expand_dims(a, axis=(0))
                    elif get_axis_labels(img.shape) == 'ZXY':
                        a = numpy.expand_dims(a, axis=(0, 2)) 
                    elif get_axis_labels(img.shape) == 'CXY':
                        a = numpy.expand_dims(a, axis=(0, 1))
                    elif get_axis_labels(img.shape) == 'TXY':
                        a = numpy.expand_dims(a, axis=(1, 2))
                    elif get_axis_labels(img.shape) == 'XY':
                        a = numpy.expand_dims(a, axis=(0, 1, 2))
                    return a.astype(numpy.uint16) if mode == "16-bit" else convert_to_8bit(a, mode)
                
                
                file_name = os.path.splitext(os.path.basename(img.fileName))[0]
                output_path = os.path.join(self.output_folder, f"{file_name}.tif")
                
                imwrite(
                    output_path,
                    convert_to_TZCXY(img),
                    imagej=True,
                    resolution=tuple(1 / value for value in img.resolution[1:3]),
                    metadata={'axes': 'TZCYX',
                              'spacing': img.resolution[0],
                              'unit': 'um'}
                )    
                
                print(f"Image '{file_name}' saved successfully as {mode}.")
        else:
            print("Please load images and select an output folder before running the code.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorUI(root)
    root.mainloop()
