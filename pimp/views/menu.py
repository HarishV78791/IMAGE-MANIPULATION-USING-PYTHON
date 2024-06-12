import tkinter as tk
from tkinter import messagebox
from ttkbootstrap.themes import standard



def create_menu(root, command_list, theme_var):
    # create menu
    menu = tk.Menu(root)

    # ### File Menu ####
    file = tk.Menu(menu, tearoff=0)

    file.add_command(label='New',underline=0, command=command_list['create_new_image'],accelerator="Ctrl+N")
    file.add_command(label='Open', command=command_list['open_image'],underline=0, accelerator="Ctrl+O")
    file.add_command(label='Save', command=command_list['save_image'],underline=0, accelerator="Ctrl+S")
    file.add_command(label='Quit', command=root.destroy,underline=0, accelerator="Alt+F4")
    menu.add_cascade(label='File', menu=file,underline=0)

    # ### Edit Menu ####
    edit = tk.Menu(menu, tearoff=0)

    edit.add_command(label='Scale', command=command_list['scale_image_frame'],underline=0)
    edit.add_command(label='Crop', command=command_list['crop_image_frame'],underline=0)
    edit.add_command(label='Convert',underline=1)
    edit.add_command(label='Rotate', command=command_list['rotate_frame'],underline=0)
    menu.add_cascade(label='Edit', menu=edit,underline=0)

    # ### Filter Menu ####
    filter = tk.Menu(menu, tearoff=0)

    filter.add_command(label='Enhance Color', command=command_list['color_enhance_frame'],underline=0)
    filter.add_command(label='Brightness', command=command_list['brightness_enhance_frame'],underline=0)
    filter.add_command(label='Contrast', command=command_list['contrast_enhance_frame'],underline=0)
    filter.add_command(label='Sharpness', command=command_list['sharpness_enhance_frame'],underline=0)
    filter.add_command(label='Grey', command=command_list['gray_image_frame'],underline=0)
    filter.add_command(label='Invert',command=command_list['invert_image_frame'],underline=0)
    filter.add_command(label='Solarize', command=command_list['solarize_frame'],underline=1)
    filter.add_command(label='Box Blur', command=command_list['box_blur_frame'],underline=2)
    filter.add_command(label='Gaussian Blur', command=command_list['gauss_blur_frame'],underline=1)
    menu.add_cascade(label='Filter', menu=filter,underline=1)

    # ### Settings Menu ####
    settings_menu = tk.Menu(menu, tearoff=0)
    
    theme_list = standard.STANDARD_THEMES
    menu.add_cascade(label='Settings', menu=settings_menu,underline=0)

    theme_menu = tk.Menu(settings_menu, tearoff=0)
    settings_menu.add_cascade(menu=theme_menu, label='Theme',underline=0)

    for theme in theme_list:
        theme_menu.add_radiobutton(
            label=theme,
            value=theme,
            variable=theme_var
        )

    #### Help Menu ####
    help_menu = tk.Menu(menu, tearoff=0)
    def show_about():
        data = '''
           1. 175CS19010 - Chaithra L 
           2. 175CS19014 - Harish V
           3. 175CS19025 - Moksha prada P
           4. 175CS19031 - Rudresh S
           5. 175CS19035 - Sudarshan S

           Guide:Mrs Reshma M

           HOD:Dr.Parameshwarappa.S

         GOVERNMENT POLYTECHNIC IMMADIHALLI
        '''
        messagebox.showinfo("About us !", data)

    help_menu.add_command(label='About', command=show_about,underline=0)
    help_menu.add_command(label='Shortcut Keys', command=command_list['shortcut_key_page'],underline=0)
    menu.add_cascade(label='Help', menu=help_menu,underline=0)
    
    return menu


print("menu")