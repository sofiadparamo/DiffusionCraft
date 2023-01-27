import os
import random
import threading
from datetime import datetime
from tkinter import Tk, Label, Button, Text, Frame, Canvas, Scale, Checkbutton, DoubleVar, BooleanVar, \
    HORIZONTAL, OptionMenu, StringVar, messagebox
from typing import List, Tuple, Optional, AnyStr
import glob

import torch
import win32con
import win32gui
import win32ui
from PIL import Image
from PIL.ImageTk import PhotoImage
from diffusers import StableDiffusionImg2ImgPipeline as SDi2iP
from torch import Generator


def process_image_generation(seed: int, hwnd: int, prompt: str, strength: float, out_dir: str):
    dfc: DiffusionCraft = DiffusionCraft(seed=seed, out_dir=out_dir)

    while True:
        try:
            h = open("tmp/h", "r")
            s = open("tmp/s", "r")

            hv = int(h.read())
            sv = float(s.read())

            if hv is not None and hv != 0:
                hwnd = hv
            if sv is not None and sv != 0:
                strength = sv
        except:
            print("Update error, config file not ready")

        input_img: Image = dfc.grab_screenshot(hwnd)

        output_img: Image = dfc.generate_image(prompt=prompt, strength=strength, input_image=input_img)

        print("Image offered to queue")
        output_img.save("tmp/output.png")


class DiffusionCraft:
    def __init__(self, seed: int, out_dir: str = "tmp/") -> None:
        print("Initializing model")
        # Load the pipeline
        device: str = "cuda"
        model_id_or_path: str = "runwayml/stable-diffusion-v1-5"
        self.pipe: SDi2iP = SDi2iP.from_pretrained(model_id_or_path, torch_dtype=torch.float16)

        self.pipe: SDi2iP = self.pipe.to(device)
        self.seed = seed
        self.out_dir = out_dir

        self.generator: Generator = Generator(device=device).manual_seed(seed)

    @staticmethod
    def get_minecraft_windows() -> List[Tuple[int, str]]:
        print("Analysing windows")
        top_list: List = []
        win_list: List = []

        def enum_cb(hwnd, _):
            win_list.append((hwnd, win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(enum_cb, top_list)

        minecrafts = [(hwnd, title) for hwnd, title in win_list if 'minecraft' in title.lower()]

        return minecrafts

    @staticmethod
    def grab_screenshot(window_id: int) -> Image:
        print(f"Grabbing screenshot for Window {window_id}")
        mc_bbox = win32gui.GetWindowRect(window_id)
        width = mc_bbox[2] - mc_bbox[0]
        height = mc_bbox[3] - mc_bbox[1]
        device_context_handle = win32gui.GetWindowDC(window_id)
        device_context = win32ui.CreateDCFromHandle(device_context_handle)
        compatible_context = device_context.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(device_context, width, height)
        compatible_context.SelectObject(bitmap)
        compatible_context.BitBlt((0, 0), (width, height), device_context, (0, 0), win32con.SRCCOPY)
        bitmap.Paint(device_context)
        bmp_info = bitmap.GetInfo()
        bmp_str = bitmap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmp_info['bmWidth'], bmp_info['bmHeight']),
            bmp_str, 'raw', 'BGRX', 0, 1)

        # Crop the title bar

        target_res: int = 512
        w: int = im.size[0]
        h: int = im.size[1]

        im = im.crop((0, 32, w, h))

        # Crop to center 512px
        im = im.crop(
            (round(w / 2 - target_res / 2), round(h / 2 - target_res / 2), round(w / 2 + target_res / 2),
             round(h / 2 + target_res / 2)))

        im.save("tmp/input.png")

        return im

    def generate_image(self, input_image: Image, prompt: str, strength: float) -> Image:
        print(f"Generating image with prompt {prompt} and strength {strength} using seed {self.seed}")
        with torch.autocast("cuda"):
            images: SDi2iP = self.pipe(image=input_image, prompt=prompt, strength=strength,
                                       generator=self.generator, num_inference_steps=35).images

        # PIL image to rgb 512x512
        image: Image = images[0]

        image_number: int = os.listdir(self.out_dir).__len__()
        image.save(f"{self.out_dir}output-{image_number}.png")

        return images[0]


class DiffusionCraftUI:
    prompt: str = ""
    seed: int = 0
    strength: float = 0.47
    show_source_image: bool = False
    hwnd: int = 0

    def __init__(self) -> None:
        print("Initializing UI")
        # Set the main parameters for the window
        self.HEIGHT: int = 700
        self.WIDTH: int = 700
        self.root: Tk = Tk()
        self.root.width = self.WIDTH
        self.root.height = self.HEIGHT
        self.canvas: Canvas = Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()
        self.frame: Frame = Frame(self.root, bg='#36393F')
        self.frame.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')
        self.root.title("DiffusionCraft")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_main)
        self.draw_welcome_interface()
        self.update_interface_loop()

    def draw_welcome_interface(self):
        print("Drawing welcome interface")
        # Titles
        title_label: Label = Label(self.frame, text="DiffusionCraft", bg='#36393F', font=("Arial", 20), fg='#FFFFFF')
        title_label.place(relx=0.05, rely=0.02, relwidth=0.90, relheight=0.2)
        author_label: Label = Label(self.frame, text="Created by SweetSofiMC", bg='#36393F', font=("Arial", 10),
                                    fg='#FFFFFF')
        author_label.place(relx=0.05, rely=0.15, relwidth=0.90, relheight=0.03)
        credits_label: Label = Label(self.frame, text="Original idea by ThoseSixFaces", bg='#36393F', font=("Arial", 8),
                                     fg='#FFFFFF')
        credits_label.place(relx=0.05, rely=0.18, relwidth=0.90, relheight=0.03)

        # Text input for prompt

        prompt_label: Label = Label(self.frame, text="Description of the building", bg='#36393F', font=("Arial", 12),
                                    anchor='w', fg='#FFFFFF', borderwidth=0)
        prompt_label.place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.05)
        prompt_text: Text = Text(self.frame, font=("Arial", 12), wrap="word")
        prompt_text.place(relx=0.05, rely=0.3, relwidth=0.90, relheight=0.2)

        # Seed input

        seed_label: Label = Label(self.frame, text="Seed", bg='#36393F', font=("Arial", 12), anchor='w', fg='#FFFFFF',
                                  borderwidth=0)
        seed_label.place(relx=0.05, rely=0.6, relwidth=0.3, relheight=0.05)
        seed_text: Text = Text(self.frame, font=("Arial", 12))
        seed_text.place(relx=0.05, rely=0.65, relwidth=0.3, relheight=0.05)
        # Init Seed
        seed_text.insert("1.0", str(random.randint(0, 999999999)))

        # Start button
        button: Button = Button(self.frame, text="Start", bg='#57F287', font=40, borderwidth=0,
                                command=lambda: self.on_start_button_press(prompt_text, seed_text))
        button.place(relx=0.05, rely=0.8, relwidth=0.90, relheight=0.1)

    def draw_job_interface(self):
        out_dir = self.create_output_folder()

        print("Drawing job interface")

        # Strength input definition
        strength_var = DoubleVar(self.root, value=0.47)

        def strength_update(_):
            self.strength = strength_var.get()
            message: str = "Strength: " + str(strength_var.get())
            strength_label.config(text=message)
            f = open("tmp/s", "w")
            f.write(str(strength_var.get()))
            f.close()

        # Strength slider

        strength_label: Label = Label(self.frame, text=("Strength: " + str(strength_var.get())), bg='#36393F',
                                      font=("Arial", 12), anchor='w', fg='#FFFFFF', borderwidth=0)
        strength_label.place(relx=0.05, rely=0.05, relwidth=0.3, relheight=0.05)
        strength_slider: Scale = Scale(self.frame, from_=0.25, to=0.9, orient=HORIZONTAL, resolution=0.01,
                                       variable=strength_var, background="#36393F", borderwidth=0, highlightthickness=0,
                                       foreground="#ffffff", command=strength_update)
        strength_slider.place(relx=0.05, rely=0.1, relwidth=0.90, relheight=0.05)

        # Show source image input definition
        show_source_image_var = BooleanVar(self.root, value=False)

        def show_source_image_checkbox_update():
            self.show_source_image = show_source_image_var.get()
            show_source_image_var.set(self.show_source_image)

        # Checkbox for showing the source image

        show_source_image_checkbox: Checkbutton = Checkbutton(self.frame, text="Show source image", bg='#36393F',
                                                              fg="#ffffff", selectcolor="#000000",
                                                              activebackground="#36393F", activeforeground="#ffffff",
                                                              highlightthickness=0,
                                                              borderwidth=0, command=show_source_image_checkbox_update,
                                                              variable=show_source_image_var)
        show_source_image_checkbox.place(relx=0.05, rely=0.2, relwidth=0.90, relheight=0.05)

        # A small dropdown selector for the Minecraft window

        minecrafts: List[Tuple[int, str]] = DiffusionCraft.get_minecraft_windows()
        hwnd_var: StringVar = StringVar(self.root, str(minecrafts[0]))

        def on_minecraft_window_select(_) -> None:
            # For all the minecraft windows, if the window as string is the same as the one selected, select it and
            selected_minecraft: Tuple[int, str] = [m for m in minecrafts if str(m) == hwnd_var.get()][0]

            # Extract the hwnd from the window
            self.hwnd = selected_minecraft[0]

            hwnd_var.set(str(selected_minecraft))

            f = open("tmp/h", "w")
            f.write(str(self.hwnd))
            f.close()

        # Initialize window value
        on_minecraft_window_select(None)

        mc_sel_label: Label = Label(self.frame,
                                    text="Minecraft Window (if nothing shows up Minecraft couldn't been detected)",
                                    bg='#36393F', font=("Arial", 12), anchor='w', fg='#FFFFFF',
                                    borderwidth=0)
        mc_sel_label.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.05)
        minecrafts_strings: List[str] = [str(m) for m in minecrafts]
        option_menu = OptionMenu(self.frame, hwnd_var, *minecrafts_strings, command=on_minecraft_window_select)
        option_menu["highlightthickness"] = 0
        option_menu.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.05)

        print("Starting image generation thread")

        threading.Thread(
            target=process_image_generation, args=(self.seed, self.hwnd, self.prompt, self.strength, out_dir)).start()

        print("Starting image display loop on main thread")
        output_image_label: Optional[Label] = None
        while True:
            self.root.update_idletasks()
            self.root.update()

            if output_image_label is not None:
                output_image_label.destroy()

            # Get the latest image from output folder
            list_of_files: List[AnyStr] = glob.glob(out_dir + '*.png')
            if len(list_of_files) < 1:
                continue

            latest_file: str = max(list_of_files, key=os.path.getctime)

            try:
                output_img: Image = Image.open(latest_file)

                if output_img is None:
                    continue

                output_img_render = PhotoImage(output_img)

                output_image_label = Label(self.frame, bg='#36393F', borderwidth=0, image=output_img_render)
                output_image_label.place(relx=0.05, rely=0.45, relwidth=0.5, relheight=0.5)
            except:
                pass

    def destroy_all_widgets(self) -> None:
        print("Destroying all widgets")
        for widget in self.frame.winfo_children():
            widget.destroy()

    def on_start_button_press(self, prompt_text: Text, seed_text: Text) -> None:
        print("Saving parameters")
        # Get Texts from frame
        self.prompt = prompt_text.get("1.0", "end-1c")
        self.seed = int(seed_text.get("1.0", "end-1c"))
        self.destroy_all_widgets()
        self.draw_job_interface()

    def update_interface_loop(self) -> None:
        print("Starting update interface loop")
        while True:
            # Get text widget content
            self.root.update_idletasks()
            self.root.update()

    def create_output_folder(self) -> str:
        # timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

        folder_name = f"tmp/output-{self.seed}-{self.prompt}-{timestamp}/"

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        else:
            # Show warning message
            messagebox.showwarning("Error",
                                   "Output folder already exists, did you time travel? "
                                   "Please set your date to sync with the internet nad change the seed and prompt")
            # noinspection PyUnresolvedReferences, PyProtectedMember
            os._exit(0)
        return folder_name

    # noinspection PyUnresolvedReferences, PyProtectedMember
    @staticmethod
    def on_closing_main():
        print("Closing program")
        os._exit(0)


if __name__ == "__main__":
    # Check if tmp folder exists, if not, create it
    if not os.path.exists("tmp"):
        os.mkdir("tmp")

    DiffusionCraftUI()
