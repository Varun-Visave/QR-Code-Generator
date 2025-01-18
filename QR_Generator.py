import qrcode
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import atexit
import os
import sys

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    sys.path.append(sys._MEIPASS)


def generator():
    data = entry.get().strip()

    if not data:
        window.geometry("350x480")
        qrlabel.pack_forget()
        error_label.pack()
        placeholderlabel.place_configure(x=35, y=145)

        error_label.config(text="Error: This field cannot be Empty", foreground="red")

        return

    try:
        qr = qrcode.QRCode(
            border=3, box_size=10, error_correction=qrcode.ERROR_CORRECT_M
        )
        qr.version = 3
        data_length = len(data)

        if 25 < data_length <= 50:
            qr.border = 2
            qr.box_size = 8
            qr.version = 4
            error_correction = qrcode.ERROR_CORRECT_M

        elif data_length > 50 and data_length <= 100:
            qr.border = 1
            qr.box_size = 6
            qr.version = 5
            error_correction = qrcode.ERROR_CORRECT_M

        elif data_length > 100 and data_length <= 150:
            qr.border = 1
            qr.box_size = 6
            qr.version = 7
            error_correction = qrcode.ERROR_CORRECT_Q

        elif data_length > 150:
            qr.border = 1
            qr.box_size = 6
            qr.version = 7
            error_correction = qrcode.ERROR_CORRECT_H

        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("img1.png")

        image = ImageTk.PhotoImage(file="img1.png")
        qrlabel.configure(image=image)
        qrlabel.image = image
        error_label.pack_forget()
        placeholderlabel.place_forget()
        qrlabel.pack(pady=5)

        window_width = qrlabel.winfo_reqwidth() + 20
        window_height = qrlabel.winfo_reqheight() + 120
        window.geometry(f"{window_width}x{window_height}")

    except Exception as e:
        error_label.config(text=f"Error: {str(e)}", fg="red")


def cleanup():
    file_path = "img1.png"
    if os.path.exists(file_path):
        os.remove(file_path)


window = tk.Tk()
window.title("QR Generator")
window.geometry("350x480")
window.resizable(False, False)
logo = tk.PhotoImage(file="./logo.png")
window.iconphoto(True, logo)

bgimageload = tk.PhotoImage(file="./bgimage.png")
bgimage = bgimageload.zoom(3, 2)
backgroundimage = ttk.Label(window, image=bgimage)
backgroundimage.place(x=0, y=0, relheight=1, relwidth=1)

load_placeholder = tk.PhotoImage(file="./placeholder.png")
placeholder = load_placeholder.subsample(4, 4)
placeholderlabel = ttk.Label(window, image=placeholder)
placeholderlabel.place_configure(x=35, y=130, width=275, height=275)
entry = ttk.Entry(window)

button = ttk.Button(window, text="Generate", command=generator)

text = ttk.Label(window, text="Enter the text to be encoded:")
text.config(background="cyan", foreground="black", font=("courier", 12))

qrlabel = ttk.Label(window)

error_label = ttk.Label(window, foreground="red", font=("courier", 12))

text.pack(pady=5)
entry.pack(pady=5)
button.pack(pady=5)
entry.focus_set()


def cleanup_resources():
    cleanup()


def exit_handler():
    cleanup_resources()
    window.destroy()


atexit.register(cleanup_resources)
window.protocol("WM_DELETE_WINDOW", exit_handler)

window.mainloop()
