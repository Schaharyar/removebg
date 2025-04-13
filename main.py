from io import BytesIO
from PIL import Image
from rembg import remove
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def remove_background_gui(as_base64: bool = False):
    # Hide root window
    root = tk.Tk()
    root.withdraw()

    try:
        # Open file dialog for multiple images
        file_paths = filedialog.askopenfilenames(
            title="Select one or more images",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )

        if not file_paths:
            print("No file(s) selected.")
            return

        for file_path in file_paths:
            with open(file_path, "rb") as f:
                image_data = f.read()
            image = Image.open(BytesIO(image_data))

            # Remove background
            result = remove(image)

            if as_base64:
                output_buffer = BytesIO()
                result.save(output_buffer, format="PNG")
                encoded = base64.b64encode(output_buffer.getvalue()).decode()
                print(f"Base64 for {os.path.basename(file_path)}:\n{encoded}\n")
            else:
                filename, ext = os.path.splitext(file_path)
                output_path = f"{filename}_nobg.png"
                result.save(output_path)
                print(f"✅ Background removed and saved to: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove background:\n{e}")

if __name__ == "__main__":
    remove_background_gui(as_base64=False)
