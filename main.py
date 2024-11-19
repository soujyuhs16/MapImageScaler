import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
import os

from image_utils import ImageProcessor
from preview_canvas import PreviewCanvas
from control_panel import ControlPanel

class ImageScalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scaler with Preview")
        self.root.geometry("768x512")
        
        # Configure main window scaling
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Create control panel
        self.control_panel = ControlPanel(
            main_frame,
            on_image_selected=self.load_image,
            on_scale_changed=self.update_preview,
            on_save_clicked=self.save_image
        )
        self.control_panel.grid(row=0, column=0, sticky="nw", padx=(0, 20))
        
        # Create preview canvas
        self.preview_canvas = PreviewCanvas(main_frame)
        self.preview_canvas.grid(row=0, column=1, sticky="nsew")
        
        # Initialize image variables
        self.original_image = None
        self.scaled_image = None
    
    def load_image(self, file_path):
        """Load and display the selected image"""
        try:
            self.original_image = Image.open(file_path)
            self.control_panel.set_status("Image loaded successfully")
            self.update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.original_image = None
    
    def update_preview(self, width_multiple=None, height_multiple=None):
        """Update the preview with current scale settings"""
        if not self.original_image:
            return
            
        try:
            # Get current scale values if not provided
            if width_multiple is None:
                width_multiple = int(self.control_panel.width_multiple.get())
            if height_multiple is None:
                height_multiple = int(self.control_panel.height_multiple.get())
            
            # Validate scale values
            if width_multiple <= 0 or height_multiple <= 0:
                messagebox.showerror("Error", "Multiples must be positive numbers")
                return
            
            # Scale image
            self.scaled_image = ImageProcessor.scale_image(
                self.original_image,
                width_multiple,
                height_multiple
            )
            
            # Create and update preview
            preview = ImageProcessor.create_preview(
                self.scaled_image,
                self.preview_canvas.canvas.winfo_width(),
                self.preview_canvas.canvas.winfo_height()
            )
            self.preview_canvas.update_preview(preview)
            
            # Update status
            self.control_panel.set_status(
                f"Preview: {self.scaled_image.width}x{self.scaled_image.height} pixels"
            )
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def save_image(self):
        """Save the scaled image"""
        if not self.scaled_image:
            messagebox.showerror("Error", "No image to save")
            return
            
        try:
            # Ask for save location
            file_types = [
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg'),
                ('All files', '*.*')
            ]
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=file_types,
                initialfile=f"scaled_{self.scaled_image.width}x{self.scaled_image.height}"
            )
            
            if save_path:
                self.scaled_image.save(save_path)
                self.control_panel.set_status(
                    f"Image saved as: {os.path.basename(save_path)}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageScalerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()