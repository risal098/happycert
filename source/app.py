import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog
from tkinter import font as tkfont
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import pandas as pd
import sys


def resource_path(relative_path):
    
    if getattr(sys, 'frozen', False):  
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1100x700")

        # init
        self.image_path = None
        self.image = None
        self.tk_image = None
        self.text = "The Full Name"
        self.text_size = 20
        self.text_position = (100, 100)
        self.text_color = "#000000"
        self.text_font = "Helvetica"
        self.font_file = ""
        self.sheet_path = ""

        # dragging var
        self.drag_data = {"x": 0, "y": 0}  

        # frame canvas for scrollbars
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white", cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbars
        self.v_scrollbar = tk.Scrollbar(
            self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        

        

        # Topbar 
        self.topbar = tk.Frame(root, bg="lightgray", height=40)
        self.topbar.pack(fill=tk.X)
        
        self.h_scrollbar = tk.Scrollbar(
            self.topbar, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.TOP, fill=tk.X)
        # Link scrollbars to the canvas
        self.canvas.config(yscrollcommand=self.v_scrollbar.set,
                           xscrollcommand=self.h_scrollbar.set)

        self.import_button = tk.Button(
            self.topbar, text="Import Image", command=self.import_image)
        self.import_button.pack(side=tk.LEFT, padx=10)

        self.preview_button = tk.Button(
            self.topbar, text="Preview", command=self.preview)
        self.preview_button.pack(side=tk.LEFT, padx=10)

        self.generate_button = tk.Button(
            self.topbar, text="Generate", command=self.generate)
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.text_size_button = tk.Button(
            self.topbar, text="Increase Text Size", command=self.increase_text_size)
        self.text_size_button.pack(side=tk.LEFT, padx=5)

        self.decrease_size_button = tk.Button(
            self.topbar, text="Decrease Text Size", command=self.decrease_text_size)
        self.decrease_size_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            self.topbar, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.font_button = tk.Button(
            self.topbar, text="Change Font", command=self.change_font)
        self.font_button.pack(side=tk.LEFT, padx=10)

        self.color_button = tk.Button(
            self.topbar, text="Change Text Color", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=10)

        # Mouse click to place text
        self.canvas.bind("<Button-1>", self.on_click)
        # Mouse drag to move text
        self.canvas.bind("<B1-Motion>", self.on_drag)

        # Mouse event bindings for panning the image
        # Right mouse button press
        self.canvas.bind("<Button-3>", self.on_right_click)
        # Right mouse button drag
        self.canvas.bind("<B3-Motion>", self.on_right_drag)

    def import_image(self):
            
            file_path = filedialog.askopenfilename(title="Open Image", filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")])
            if file_path:
                self.image_path = file_path
                self.image = Image.open(self.image_path)

                # Resize the image to fit the window (optional)
                window_width = self.root.winfo_width()
                window_height = self.root.winfo_height()

                img_width, img_height = self.image.size
                aspect_ratio = img_width / img_height

              

                    
                self.tk_image = ImageTk.PhotoImage(self.image)

                    
                    
                self.canvas.delete("all")
                self.canvas.create_image(
                        0, 0, anchor=tk.NW, image=self.tk_image)

                    
                self.canvas.config(scrollregion=self.canvas.bbox("all"))

                    
                self.canvas.create_text(self.text_position, text=self.text, font=(
                self.text_font, self.text_size), fill=self.text_color, tags="text")

                #    print(f"Image Path: {self.image_path}")
                 #   print(
                  #      f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def on_click(self, event):
        
        self.text_position = (event.x, event.y)
        self.update_text_position()

    def on_drag(self, event):
        
        self.text_position = (event.x, event.y)
        self.update_text_position()

    def update_text_position(self):
        
        self.canvas.delete("text")  # Delete old text
        self.canvas.create_text(self.text_position, text=self.text, font=(
            self.text_font, self.text_size), fill=self.text_color, tags="text")
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def increase_text_size(self):
        
        self.text_size += 2
        self.update_text_size()

    def decrease_text_size(self):
        
        if self.text_size > 2:
            self.text_size -= 2
        self.update_text_size()

    def save(self, name):
        image = Image.open(self.image_path)
        print("tes")
        draw = ImageDraw.Draw(image)
        if self.font_file == "":
            font = ImageFont.truetype(resource_path("Helvetica.ttf"), size=self.text_size*1.3)
        else:
            font = ImageFont.truetype(self.font_file, size=self.text_size*1.3)
        text = name
        position = self.text_position
        hex_color = self.text_color
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((position[0] - text_width // 2)-5,
                    (position[1] - text_height // 2)-16)
        draw.text(position, text, font=font, fill=rgb_color)
        print(name+"png")
        if self.image_path[-4:] == ".png":
            image.save("results/"+name+'.png')  # Save to a new file
        elif self.image_path[-4:] == ".jpg":
            image.save("results/"+name+'.jpg')
        elif self.image_path[-4:] == ".jpeg":
            image.save("results/"+name+'.jpeg')

    def generate(self):
        
        path_file = filedialog.askopenfilename(title="Select excel", filetypes=[
                                               ("excel type", "*.xlsx *.xls *.xlt")])
        if path_file and os.path.exists(path_file):
            # Load the font into Tkinter
            try:
                # Load the Excel file
                df = pd.read_excel(path_file)

                # Get the first column (index 0) of the dataframe
                first_column = df.iloc[:, 0]

                # Display the items in the first column
                for x in first_column:
                    self.save(x)
            except Exception as e:
                print(f"Error excel: {e}")

    def preview(self):
        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        if self.font_file == "":
            font = ImageFont.truetype(resource_path("Helvetica.ttf"), size=self.text_size*1.3)
        else:
            font = ImageFont.truetype(self.font_file, size=self.text_size*1.3)
        text = "The Full Name"
        position = self.text_position
        hex_color = self.text_color
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((position[0] - text_width // 2)-5,
                    (position[1] - text_height // 2)-16)
        draw.text(position, text, font=font, fill=rgb_color)
        # text_width = draw.textlength(text, font=font)
       # position =  ((position[0] - text_width // 2)-3, position[1]-5)
       # draw.text(position, text, font=font, fill=rgb_color)
       # image.save('output_image.png')  # Save to a new file
        image.show()  # Optionally, show the image

    def update_text_size(self):
        
        self.canvas.delete("text")  # Delete old text
        self.canvas.create_text(self.text_position, text=self.text, font=(
            self.text_font, self.text_size), fill=self.text_color, tags="text")
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def change_font(self):
        
        font_file = filedialog.askopenfilename(title="Select Font", filetypes=[
                                               ("TrueType Font", "*.ttf *.otf")])
        if font_file and os.path.exists(font_file):
            # Load the font into Tkinter
            try:
                self.text_font = tkfont.Font(
                    family=font_file)  # Load the font file
                self.font_file = str(font_file)
                print(f"Selected Font: {self.font_file},{self.text_font},")
                self.update_text_size()
            except Exception as e:
                print(f"Error loading font: {e}")

    def change_color(self):
        
        color = colorchooser.askcolor()[1]  # Returns a hex color
        if color:
            self.text_color = color
            self.update_text_size()

    def reset(self):
        
        self.canvas.delete("all")
        self.text_size = 20
        self.text_position = (100, 100)
        self.text_color = "#000000"
        self.text_font = "Helvetica"
        self.font_file = ""
        print(
            f"Text Position: {self.text_position}, Text Size: {self.text_size}, Text Font: {self.text_font}, Text Color: {self.text_color}")

    def on_right_click(self, event):
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_right_drag(self, event):
        
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y



if __name__ == "__main__":
		directory = "results"
		if not os.path.exists(directory):
				os.makedirs(directory)
				print(f"Directory '{directory}' created.")
		else:
				print(f"Directory '{directory}' already exists.")
		root = tk.Tk()
		app = ImageEditorApp(root)
		root.mainloop()
