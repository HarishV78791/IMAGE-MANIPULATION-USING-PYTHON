from msilib import text
import pathlib
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import ANCHOR, CENTER, UNDERLINE
import ttkbootstrap as bttk
from ttkbootstrap.icons import Emoji
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
import settings as st
from .menu import create_menu
from models.model import update_config_file, update_last_login_date_time


update_last_login_date_time()

root = bttk.Window(
        title = st.MAIN_WIN_TITLE,
        iconphoto=st.LOGO,
        themename=st.BASE_THEME
        )

# root.wm_attributes("transparentcolor", 'grey')
theme_var = tk.StringVar(root, st.BASE_THEME)
status_var = tk.StringVar(root,"Welcome")
new_image_color_var = tk.StringVar(root, "#0000ff")
height_entry_var = tk.IntVar(root, "100")
width_entry_var = tk.IntVar(root, "100")
rotate_angle_var = tk.IntVar(root, "0")
color_enh_var = tk.DoubleVar(root, "1.0",)
contrast_enh_var = tk.DoubleVar(root, "1")
brightness_enh_var = tk.DoubleVar(root, "1")
sharpness_enh_var = tk.DoubleVar(root, "1")
solarize_enh_var = tk.IntVar(root, "100")
box_blur_enh_var = tk.IntVar(root, "0")
gaussian_blur_enh_var = tk.IntVar(root, "0")
top_left_x_var = tk.IntVar(root, "0")
top_left_y_var = tk.IntVar(root, "0")
bottom_right_x_var = tk.IntVar(root, "0")
bottom_right_y_var = tk.IntVar(root, "0")
scale_img_var = tk.DoubleVar(root, "1")

style = bttk.Style()

bttk.Style().configure('TButton', font="-size 14")

def set_theme(*args):
    theme = theme_var.get()
    theme_update = {'THEME': theme}
    update_config_file(theme_update)
    style.theme_use(theme)
    bttk.Style().configure('TButton', font="-size 14")


theme_var.trace('w', set_theme)


def display_image_1(image_path):
    img_frame_height = image_frame.winfo_height()
    img_frame_width = image_frame.winfo_width()

    with Image.open(image_path) as img:
        img_width = img.width
        img_height= img.height

        ratio = min((img_frame_width/img_width), (img_frame_height/img_height))
        if ratio < 1:
            img_scale = ImageOps.scale(img, ratio)
            img_scale.save(st.PREVIEW_IMAGE)
        else:
            img.save(st.PREVIEW_IMAGE)

    with Image.open(st.PREVIEW_IMAGE) as img:
        image_label.image = ImageTk.PhotoImage(img)
        image_label.config(image=image_label.image)


def display_image(image_path):
    img_frame_height = image_frame.winfo_height()
    img_frame_width = image_frame.winfo_width()

    with Image.open(image_path) as img:
        img_width = img.width
        img_height= img.height

        ratio = min((img_frame_width/img_width), (img_frame_height/img_height))
        if ratio < 1:
            img_scale = ImageOps.scale(img, ratio)
            image_label.image = ImageTk.PhotoImage(img_scale)
        else:
            image_label.image = ImageTk.PhotoImage(img)
        
        image_label.config(image=image_label.image)
        status_var.set(f"Image Width = {img_width} and height = {img_height}")

def shortcut_key_page():

    sk_page = tk.Toplevel(root, padx=35, pady=5)
    sk_page.title("Shortcut Keys")
    sk_page.geometry("500x300")
    sk_page.resizable(False, False)
    sk_page.grab_set()

    sk_page.columnconfigure(0, weight=1)
    sk_page.columnconfigure(1, weight=1)
    sk_page_label = bttk.Label(sk_page, text="Shortcut Keys", anchor=CENTER, font='bold 25')
    sk_page_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=(50,10))

    bttk.Label(sk_page, text="Command", anchor=CENTER).grid(row=1, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Key Binding", anchor=CENTER).grid(row=1, column=1, sticky='nsew')
    bttk.Separator(sk_page).grid(row=2, column=0, columnspan=2, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + O", anchor=CENTER).grid(row=3, column=0, sticky='nsew', pady=(20,0))
    bttk.Label(sk_page, text="Open Image", anchor=CENTER).grid(row=3, column=1, sticky='nsew', pady=(20,0))

    bttk.Label(sk_page, text="Ctrl + S", anchor=CENTER).grid(row=4, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Save Image", anchor=CENTER).grid(row=4, column=1, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + I", anchor=CENTER).grid(row=5, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Insert Image", anchor=CENTER).grid(row=5, column=1, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + r", anchor=CENTER).grid(row=6, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Rotate Right 90 deg", anchor=CENTER).grid(row=6, column=1, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + Shift + R", anchor=CENTER).grid(row=7, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Rotate Left 90 deg", anchor=CENTER).grid(row=7, column=1, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + h", anchor=CENTER).grid(row=8, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Flip Horizontal", anchor=CENTER).grid(row=8, column=1, sticky='nsew')

    bttk.Label(sk_page, text="Ctrl + Shift + H", anchor=CENTER).grid(row=9, column=0, sticky='nsew')
    bttk.Label(sk_page, text="Flip Vertical", anchor=CENTER).grid(row=9, column=1, sticky='nsew')


def open_image(*args):
    filename = filedialog.askopenfilename(
		initialdir=st.INITIAL_DIR,
		title = "Open Image File",
		filetype=(
            ("Image files", ("*.jpg","*.jpeg","*.png")), 
            ("JPEG files", "*.jpeg"), 
            ("PNG files", "*.png"), 
            ("JPG files", "*.jpg"),  
            )
		)

    if filename:
        file_path = filename.rsplit('/',1)[0]
        st.INITIAL_DIR = file_path
        st.INITIAL_IMAGE = filename
        data = {
                "INITIAL_DIR":file_path,
                "INITIAL_IMAGE":filename,
                }
        update_config_file(data)
    
        with Image.open(filename) as img:
            img.save(st.LAST_IMAGE)

        display_image(st.LAST_IMAGE)
        status_var.set(f"Open file {filename}")


def choose_color():
    cd = ColorChooserDialog()
    cd.show()
    color = cd.result
    if color:
        new_image_color_var.set(color.hex)


def generate_image():
    try:
        height = int(height_entry_var.get())
        width = int(width_entry_var.get())
        color = new_image_color_var.get()
    except:
        messagebox.showerror("Error in Data", "Width, Height should be in numbers greater than 10")
        return None
    if height < 10 or width<10:
        messagebox.showerror("Error in Data", "Width, Height should be in numbers greater than 10")
        return None
    img1 = Image.new('RGBA',(width,height),color)

    img1.save(st.LAST_IMAGE)
    display_image(st.LAST_IMAGE)
    status_var.set(f"New Image Created with height= {height}, width={width} and color= {color}")


def create_new_image(*args):
    global image_option_frame
    image_option_frame.grid_forget()
    image_option_frame.destroy()
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew') 

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    width_label = bttk.Label(image_option_frame,text="Width", bootstyle="inverse-info", padding=5)
    width_label.grid(row=0, column=0, sticky='nsew')
    height_label = bttk.Label(image_option_frame,text="Height", bootstyle="inverse-info", padding=5)
    height_label.grid(row=1, column=0, sticky='nsew')
    Color_label = bttk.Label(image_option_frame,text="Choose Color", bootstyle="inverse-info", padding=5)
    Color_label.grid(row=2, column=0, sticky='nsew')

    width_entry = bttk.Entry(image_option_frame, textvariable=width_entry_var, bootstyle='info')
    width_entry.grid(row=0, column=1, sticky='nsew')
    height_entry = bttk.Entry(image_option_frame, textvariable=height_entry_var, bootstyle='info')
    height_entry.grid(row=1, column=1, sticky='nsew')

    color_btn = bttk.Button(image_option_frame, text="color", command=choose_color)
    color_btn.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)
    generate_btn = bttk.Button(image_option_frame, text="Create", command=generate_image)
    generate_btn.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    status_var.set(f"Chosen New Image option")
    display_image(st.LAST_IMAGE)


def save_image():
    filename = filedialog.asksaveasfilename(
        defaultextension='.png', 
        initialdir=st.INITIAL_DIR,
        filetype=(
            ("Image files", ("*.jpg","*.jpeg","*.png")), 
            ("JPEG files", "*.jpeg"), 
            ("PNG files", "*.png"), 
            ("JPG files", "*.jpg"),  
            ),
        title = "Save Image",
        )
    if filename:
        ext = filename.rsplit('.')[-1]
        if ext in ('jpg', 'jpeg', 'png'):
            with Image.open(st.LAST_IMAGE) as img:
                try:
                    img.save(filename)
                except:
                    img.convert('RGB').save(filename,"JPEG")
            status_var.set(f"Image Saved in {filename}")

        else:
            status_var.set("Error in Saving")
            messagebox.showerror("File Save", "Unable to Save file with the given file name.")



def rotate_image(*args):
    file = pathlib.Path(st.LAST_IMAGE)
    if file.exists():
        angle = rotate_angle_var.get()
        with Image.open(st.LAST_IMAGE) as img:
            preview_img = img.rotate(angle, expand=True)
            preview_img.save(st.PREVIEW_IMAGE)
        
        display_image(st.PREVIEW_IMAGE)
    else:
        messagebox.showerror("Broken Image", "Please open an image (Ctrl+O) or create a new one (Ctrl+N)")



def save_preview():
    file = pathlib.Path(st.PREVIEW_IMAGE)
    if file.exists():
        with Image.open(file) as img:
            img.save(st.LAST_IMAGE)
        file.unlink()
    display_image(st.LAST_IMAGE)


def cancel_preview():
    file = pathlib.Path(st.PREVIEW_IMAGE)
    if file.exists():
        file.unlink()
    display_image(st.LAST_IMAGE)


def color_enhance_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_filter = ImageEnhance.Color(img)
        new_img = img_filter.enhance(color_enh_var.get())
        new_img.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def brightness_enhance_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_filter = ImageEnhance.Brightness(img)
        new_img = img_filter.enhance(brightness_enh_var.get())
        new_img.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def contrast_enhance_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_filter = ImageEnhance.Contrast(img)
        new_img = img_filter.enhance(contrast_enh_var.get())
        new_img.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def sharpness_enhance_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_filter = ImageEnhance.Sharpness(img)
        new_img = img_filter.enhance(sharpness_enh_var.get())
        new_img.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def solarize_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_solarize = ImageOps.solarize(img, threshold=solarize_enh_var.get())
        img_solarize.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def scale_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_scale = ImageOps.scale(img, scale_img_var.get())
        img_scale.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def gray_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_scale = ImageOps.grayscale(img)
        img_scale.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def invert_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_scale = ImageOps.invert(img)
        img_scale.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def box_blur_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_blur = img.filter(filter=ImageFilter.BoxBlur(box_blur_enh_var.get()))
        img_blur.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def gauss_blur_image():
    with Image.open(st.LAST_IMAGE) as img:
        img_blur = img.filter(filter=ImageFilter.GaussianBlur(gaussian_blur_enh_var.get()))
        img_blur.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def crop_image():
    with Image.open(st.LAST_IMAGE) as img:
        x1 = top_left_x_var.get()
        y1 = top_left_y_var.get()
        x2 = bottom_right_x_var.get()
        y2 = bottom_right_y_var.get()
        img_crop = img.crop((x1,y1,x2,y2))
        img_crop.save(st.PREVIEW_IMAGE)
    display_image(st.PREVIEW_IMAGE)


def rotate_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    width_label = bttk.Label(image_option_frame,text="ROTATE", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    width_label.grid(row=0, column=0,columnspan=2, sticky='nsew')
    height_label = bttk.Label(image_option_frame,text="Rotate", bootstyle="inverse-info", padding=5)
    height_label.grid(row=1, column=0, sticky='nsew')

    height_entry = bttk.Entry(image_option_frame, textvariable=rotate_angle_var, bootstyle='info')
    height_entry.grid(row=1, column=1, sticky='nsew')

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=rotate_image)
    preview_btn.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=4, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=4, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Rotate Image Options")


def color_enhance_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Enhance Color", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Color", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=color_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=color_enh_var,from_ = 0.5, to = 2.0)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=color_enhance_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Color Enhance Options")


def brightness_enhance_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Brightness", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Brightness", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=brightness_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=brightness_enh_var, from_ = 0.5, to = 2.0)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=brightness_enhance_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Brightness Options")


def contrast_enhance_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Contrast", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Contrast", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=contrast_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=contrast_enh_var, from_ = 0.5, to = 2.0)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=contrast_enhance_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Contrast Options")


def sharpness_enhance_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Sharpness", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Sharpness", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=sharpness_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=sharpness_enh_var, from_ = 0.5, to = 2.0)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=sharpness_enhance_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Sharpness Options")


def solarize_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Solarize Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Solarize ", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=solarize_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=solarize_enh_var, from_ = 1, to = 100)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=solarize_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Sharpness Options")


def box_blur_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Blur Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Blur ", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=box_blur_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=box_blur_enh_var, from_ = 0, to = 10)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=box_blur_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Box Blur Options")


def gauss_blur_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Gauss Blur Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Blur ", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=gaussian_blur_enh_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=gaussian_blur_enh_var, from_ = 0, to = 10)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=gauss_blur_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Gaussian Blur Options")


def scale_image_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Scale Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    color_label = bttk.Label(image_option_frame,text="Scale ", bootstyle="inverse-info", padding=5)
    color_label.grid(row=1, column=0, sticky='nsew')
    color_val = bttk.Label(image_option_frame,textvariable=scale_img_var, bootstyle="inverse-info", padding=5)
    color_val.grid(row=1, column=1, sticky='nsew')
    color_scale = bttk.Scale(image_option_frame, variable=scale_img_var, from_ = 0.5, to = 2)
    color_scale.grid(row=2, column=0,columnspan=2, sticky='nsew', padx=10)

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=scale_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Scale Image")


def gray_image_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Gray Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')


    preview_btn = bttk.Button(image_option_frame, text="Preview", command=gray_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Gray Image")


def invert_image_frame():
    global image_option_frame

    image_option_frame.grid_forget()    
    image_option_frame.destroy() 
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew')   

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Invert Image", anchor=tk.CENTER,bootstyle="inverse-info", padding=10)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')


    preview_btn = bttk.Button(image_option_frame, text="Preview", command=invert_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)
    status_var.set(f"Gray Image")


def crop_image_frame(*args):
    with Image.open(st.LAST_IMAGE) as img:
        x,y = img.size
        bottom_right_x_var.set(x)
        bottom_right_y_var.set(y)

    global image_option_frame
    image_option_frame.grid_forget()
    image_option_frame.destroy()
    image_option_frame = bttk.Frame(image_frame, style='info', width=150)
    image_option_frame.grid(row=0, column=1, sticky='nsew') 

    image_option_frame.columnconfigure(0, weight=1)
    image_option_frame.columnconfigure(1, weight=2)

    title_label = bttk.Label(image_option_frame,text="Crop Image",anchor=tk.CENTER, bootstyle="inverse-info", padding=5)
    title_label.grid(row=0, column=0,columnspan=2, sticky='nsew')

    top_left_x_label = bttk.Label(image_option_frame,text="Top Left X", bootstyle="inverse-info", padding=5)
    top_left_x_label.grid(row=1, column=0, sticky='nsew')
    top_left_y_label = bttk.Label(image_option_frame,text="Top Left Y", bootstyle="inverse-info", padding=5)
    top_left_y_label.grid(row=2, column=0, sticky='nsew')


    top_left_x = bttk.Entry(image_option_frame, textvariable=top_left_x_var, bootstyle='info')
    top_left_x.grid(row=1, column=1, sticky='nsew')
    top_left_y = bttk.Entry(image_option_frame, textvariable=top_left_y_var, bootstyle='info')
    top_left_y.grid(row=2, column=1, sticky='nsew')


    bottom_right_x_label = bttk.Label(image_option_frame,text="Bottom Right X", bootstyle="inverse-info", padding=5)
    bottom_right_x_label.grid(row=3, column=0, sticky='nsew')
    bottom_right_y_label = bttk.Label(image_option_frame,text="Bottom Right Y", bootstyle="inverse-info", padding=5)
    bottom_right_y_label.grid(row=4, column=0, sticky='nsew')


    bottom_right_x = bttk.Entry(image_option_frame, textvariable=bottom_right_x_var, bootstyle='info')
    bottom_right_x.grid(row=3, column=1, sticky='nsew')
    bottom_right_y = bttk.Entry(image_option_frame, textvariable=bottom_right_y_var, bootstyle='info')
    bottom_right_y.grid(row=4, column=1, sticky='nsew')

    preview_btn = bttk.Button(image_option_frame, text="Preview", command=crop_image)
    preview_btn.grid(row=10, column=0, columnspan=2, sticky='nsew', padx=20, pady=15)

    cancel_btn = bttk.Button(image_option_frame, text=Emoji.get("CROSS MARK"), command=cancel_preview, bootstyle='danger')
    cancel_btn.grid(row=11, column=0, sticky='nsew', padx=20, pady=15)

    save_btn = bttk.Button(image_option_frame, text=Emoji.get('FLOPPY DISK'), command=save_preview, bootstyle='success')
    save_btn.grid(row=11, column=1, sticky='nsew', padx=20, pady=15)
    display_image(st.LAST_IMAGE)



    status_var.set(f"Crop Image")
    display_image(st.LAST_IMAGE)



def rotate_90_right_image(*args):
    rotate_angle_var.set(90)
    rotate_image()
    save_preview()


def rotate_90_left_image(*args):
    rotate_angle_var.set(-90)
    rotate_image()
    save_preview()


def flip_image(direction):
    file = pathlib.Path(st.PREVIEW_IMAGE)
    if file.exists():
        with Image.open(file) as img:
            flip_img = img.transpose(direction)
        file.unlink()
    else:
        file = pathlib.Path(st.LAST_IMAGE)
        with Image.open(file) as img:
            flip_img = img.transpose(direction) 
   
    flip_img.save(st.LAST_IMAGE)
    display_image(st.LAST_IMAGE)


def flip_horizontal_image(*args):
    flip_image(Image.FLIP_LEFT_RIGHT)


def flip_vertical_image(*args):
    flip_image(Image.FLIP_TOP_BOTTOM)



root.geometry(f'{int(root.winfo_screenwidth()-100)}x{int(root.winfo_screenheight()-100)}')


##### Main Frame #####


##### Buttons Frame #####
root.columnconfigure(0, weight=1)
top_button_frame = bttk.Frame(root)
top_button_frame.grid(row=0, column=0, sticky='nsew')

new_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('HEAVY PLUS SIGN'),
                    style='primary-outline',
                    padding=10,
                    command=create_new_image
                    )
new_btn.pack(side=tk.LEFT)
ToolTip(new_btn, text="New Image")


open_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('open file folder'),
                    style='primary-outline',
                    padding=10,
                    command=open_image,
                    width=5,
                    )
open_btn.pack(side=tk.LEFT)
ToolTip(open_btn, text="Open Image")


save_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('FLOPPY DISK'),
                    style='primary-outline',
                    padding=10,
                    command=save_image,
                    width=5,
                    )
save_btn.pack(side=tk.LEFT)
ToolTip(save_btn, text="Save Image")


scale_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('FRAME WITH PICTURE'),
                    style='primary-outline',
                    padding=10,
                    command=scale_image_frame,
                    width=5,
                    )
scale_btn.pack(side=tk.LEFT)
ToolTip(scale_btn, text="Scale Image")


rotate_right_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('CLOCKWISE RIGHTWARDS AND LEFTWARDS OPEN CIRCLE ARROWS'),
                    style='primary-outline',
                    padding=10,
                    command=rotate_90_right_image,
                    width=5,
                    )
rotate_right_btn.pack(side=tk.LEFT)
ToolTip(rotate_right_btn, text="Rotate 90° Clockwise")


rotate_left_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('ANTICLOCKWISE DOWNWARDS AND UPWARDS OPEN CIRCLE ARROWS'),
                    style='primary-outline',
                    padding=10,
                    command=rotate_90_left_image,
                    width=5,
                    )
rotate_left_btn.pack(side=tk.LEFT)
ToolTip(rotate_left_btn, text="Rotate 90° AntiClockWise")


flip_horiz_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('LEFT RIGHT ARROW'),
                    style='primary-outline',
                    padding=10,
                    command=flip_horizontal_image,
                    width=5,
                    )
flip_horiz_btn.pack(side=tk.LEFT)
ToolTip(flip_horiz_btn, text="Flip Horizontal")


flip_vertical_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('UP DOWN ARROW'),
                    style='primary-outline',
                    padding=10,
                    command=flip_vertical_image,
                    width=5,
                    )
flip_vertical_btn.pack(side=tk.LEFT)
ToolTip(flip_vertical_btn, text="Flip Vertical")


brightness_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('HIGH BRIGHTNESS SYMBOL'),
                    style='primary-outline',
                    padding=10,
                    command=brightness_enhance_frame,
                    width=5,
                    )
brightness_btn.pack(side=tk.LEFT)
ToolTip(brightness_btn, text="Brightness")

contrast_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('LOW BRIGHTNESS SYMBOL'),
                    style='primary-outline',
                    padding=10,
                    command=contrast_enhance_frame,
                    width=5,
                    )
contrast_btn.pack(side=tk.LEFT)
ToolTip(contrast_btn, text="Contrast")

crop_btn = bttk.Button(top_button_frame,
                    text=Emoji.get('WHITE SQUARE BUTTON'),
                    style='primary-outline',
                    padding=10,
                    command=crop_image_frame,
                    width=5,
                    )
crop_btn.pack(side=tk.LEFT)
ToolTip(crop_btn, text="Crop")




##### Image Frame #####
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# image_frame = ScrolledFrame(root, bootstyle="danger", padding=10)
image_frame = bttk.Frame(root, padding=5)
image_frame.grid(row=1, column=0, sticky='nsew')
image_frame.update()

img_frame_height = image_frame.winfo_height()
img_frame_width = image_frame.winfo_width()

image_frame.rowconfigure(0, weight=1)
image_frame.columnconfigure(0, weight=1)
# image_frame.columnconfigure(1, weight=1)

try:
    img_temp = ImageTk.PhotoImage(Image.open(st.LAST_IMAGE))
    image_label = bttk.Label(image_frame, image=img_temp)
except:
    image_label = bttk.Label(image_frame)

image_label.grid(row=0, column=0, sticky='nsew')

popup_menu=tk.Menu(image_label,tearoff=0)
popup_menu.add_command(label="Open Image", command=open_image, accelerator="Ctrl+o")
popup_menu.add_command(label="Save Image", command=save_image, accelerator="Ctrl+S")
popup_menu.add_command(label="Rotate Right", command=rotate_90_right_image, accelerator="Ctrl+R")
popup_menu.add_command(label="Rotate Left", command=rotate_90_right_image, accelerator="Ctrl+Shift+R")
popup_menu.add_command(label="Flip Horizontal", command=flip_horizontal_image, accelerator="Ctrl+h")
popup_menu.add_command(label="Flip Vertical", command=flip_vertical_image, accelerator="Ctrl+Shift+H")

def image_right_click_menu(event):
    # print(event)
    try:
        popup_menu.tk_popup(event.x_root, event.y_root,0)
    except:
        popup_menu.grab_release()


image_label.bind("<Button-3>", image_right_click_menu)

root.bind_all("<Control-n>", create_new_image)
root.bind_all("<Control-o>", open_image)
root.bind_all("<Control-r>", rotate_90_right_image)
root.bind_all("<Control-R>", rotate_90_left_image)
root.bind_all("<Control-h>", flip_horizontal_image)
root.bind_all("<Control-H>", flip_vertical_image)

#############################################
##### options Frame #####
##############################################
image_option_frame = bttk.Frame(image_frame, style='info', width=150)
image_option_frame.grid(row=0, column=1, sticky='nsew')
image_option_frame.grid_forget()

# image_option_frame.rowconfigure(0, weight=1)
# image_option_frame.columnconfigure(0, weight=1)



##### Status Frame #####
root.columnconfigure(0, weight=1)
status_frame = bttk.Frame(root, bootstyle="info", padding=5)
status_frame.grid(row=2, column=0, sticky='nsew')

left_label = bttk.Label(status_frame, text="Department of CSE, GPTI", bootstyle="inverse-info")
left_label.pack(side=tk.LEFT, padx=5)


right_label = bttk.Label(status_frame, textvariable=status_var, bootstyle="inverse-info")
right_label.pack(side=tk.RIGHT, padx=5)


command_list = {
        'shortcut_key_page':shortcut_key_page,
        'open_image':open_image,
        'save_image':save_image,
        'rotate_frame':rotate_frame,
        'create_new_image':create_new_image,
        'color_enhance_frame':color_enhance_frame,
        'brightness_enhance_frame':brightness_enhance_frame,
        'contrast_enhance_frame':contrast_enhance_frame,
        'sharpness_enhance_frame':sharpness_enhance_frame,
        'solarize_frame':solarize_frame,
        'box_blur_frame':box_blur_frame,
        'gauss_blur_frame':gauss_blur_frame,
        'crop_image_frame':crop_image_frame,
        'scale_image_frame':scale_image_frame,
        'gray_image_frame':gray_image_frame,
        'invert_image_frame':invert_image_frame,
}

menu = create_menu(root,command_list, theme_var)
root.config(menu=menu)

print("view")