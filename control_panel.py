import tkinter as tk
from tkinter import ttk, filedialog

class ControlPanel(ttk.Frame):
    def __init__(self, parent, on_image_selected, on_scale_changed, on_save_clicked, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Callbacks
        self.on_image_selected = on_image_selected
        self.on_scale_changed = on_scale_changed
        self.on_save_clicked = on_save_clicked
        
        # File selection
        self.file_path = tk.StringVar()
        ttk.Label(self, text="Image File:").pack(anchor=tk.W, pady=(0, 5))
        ttk.Entry(self, textvariable=self.file_path, width=40).pack(anchor=tk.W)
        ttk.Button(self, text="Browse", command=self._browse_file).pack(anchor=tk.W, pady=(5, 20))
        
        # Scale controls frame
        scale_frame = ttk.LabelFrame(self, text="Scale Settings", padding=(10, 5))
        scale_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Width multiple
        ttk.Label(scale_frame, text="Width Multiple (1 = 128px):").pack(anchor=tk.W)
        self.width_multiple = ttk.Spinbox(
            scale_frame,
            from_=1,
            to=20,
            width=10,
            command=self._on_scale_change
        )
        self.width_multiple.pack(anchor=tk.W, pady=(5, 15))
        self.width_multiple.set(2)
        
        # Height multiple
        ttk.Label(scale_frame, text="Height Multiple (1 = 128px):").pack(anchor=tk.W)
        self.height_multiple = ttk.Spinbox(
            scale_frame,
            from_=1,
            to=20,
            width=10,
            command=self._on_scale_change
        )
        self.height_multiple.pack(anchor=tk.W, pady=(5, 10))
        self.height_multiple.set(2)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(
            button_frame,
            text="Update Preview",
            command=self._on_scale_change
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="Save Image",
            command=self.on_save_clicked
        ).pack(side=tk.LEFT)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(
            self,
            textvariable=self.status_var,
            wraplength=350
        ).pack(anchor=tk.W, pady=(20, 0))
    
    def _browse_file(self):
        """Handle file browse button click"""
        filetypes = (
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            self.file_path.set(filename)
            self.on_image_selected(filename)
    
    def _on_scale_change(self):
        """Handle scale value changes"""
        try:
            width = int(self.width_multiple.get())
            height = int(self.height_multiple.get())
            self.on_scale_changed(width, height)
        except ValueError:
            pass
    
    def set_status(self, message):
        """Update status message"""
        self.status_var.set(message)