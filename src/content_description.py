import threading
import cv2
from PIL import Image
import io
import tkinter as tk
from src.ollama_client import generate_description, OllamaError
from src.services.translation import translate
from src.services.tts import speak


class ContentDescriber:
    def __init__(self, root, user_input, video_handler, theme: dict | None = None):
        self.root = root
        self.user_input = user_input
        self.video_handler = video_handler
        self.message_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.language_var.set("en")
        self.languages = {"en": "English", "tr": "Turkish", "de": "German", "ar": "Arabic"}

        # theme defaults
        self.theme = theme or {"bg": "#0f0f0f", "fg": "#ffffff", "btn_bg": "#1f1f1f", "btn_fg": "#ffffff"}

        self.message_label = tk.Label(root, textvariable=self.message_var, wraplength=500, anchor=tk.E, bg=self.theme["bg"], fg=self.theme["fg"])
        self.message_label.pack()
        self.message_label.place(relx=0.95, rely=0.5, anchor=tk.E)

        self.camera_var = tk.StringVar()
        self.camera_var.set("0")

        camera_label = tk.Label(root, text="Select Camera:", bg=self.theme["bg"], fg=self.theme["fg"])
        camera_label.pack()

        camera_menu = tk.OptionMenu(root, self.camera_var, *self.get_available_cameras())
        camera_menu.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        try:
            camera_menu["menu"].config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        except Exception:
            pass
        camera_menu.pack()

        language_label = tk.Label(root, text="Select Language:", bg=self.theme["bg"], fg=self.theme["fg"]) 
        language_label.pack()

        language_menu = tk.OptionMenu(root, self.language_var, *self.languages.keys())
        language_menu.config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        try:
            language_menu["menu"].config(bg=self.theme["btn_bg"], fg=self.theme["btn_fg"])
        except Exception:
            pass
        language_menu.pack()

        frame_top = tk.Frame(root, bg=self.theme["bg"]) 
        frame_top.pack(side=tk.TOP)
        frame_bottom = tk.Frame(root, bg=self.theme["bg"]) 
        frame_bottom.pack(side=tk.TOP)

        button_stop = tk.Button(frame_top, text="Stop", width=50, command=video_handler.stop_video, bg=self.theme["btn_bg"], fg=self.theme["btn_fg"]) 
        button_stop.pack(side=tk.LEFT, padx=5, pady=5)

        button_describe = tk.Button(frame_top, text="Describe the frame", width=50, command=lambda: self.threaded_describe_content(), bg=self.theme["btn_bg"], fg=self.theme["btn_fg"]) 
        button_describe.pack(side=tk.LEFT, padx=5, pady=5)

        button_tts = tk.Button(frame_top, text="Text-to-Speech", width=50, command=self.text_to_speech, bg=self.theme["btn_bg"], fg=self.theme["btn_fg"]) 
        button_tts.pack(side=tk.LEFT, padx=5, pady=5)

        button_camera = tk.Button(frame_bottom, text="Select Camera", width=50, command=lambda: video_handler.start_stream(self.camera_var.get()), bg=self.theme["btn_bg"], fg=self.theme["btn_fg"]) 
        button_camera.pack(side=tk.LEFT, padx=5, pady=5)

    def get_available_cameras(self):
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(str(i))
                cap.release()
        return available_cameras

    def describe_content(self):
        # show immediate feedback
        self.root.after(0, self.update_message, "Describing...")
        current_frame = self.video_handler.get_current_frame()
        if current_frame is not None:
            pil_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format="JPEG")
            user_request = self.user_input.get()
            try:
                resp_text = generate_description(user_request, img_byte_arr.getvalue())
                if resp_text:
                    translated_text = translate(resp_text, self.language_var.get())
                    self.root.after(0, self.update_message, translated_text)
                else:
                    self.root.after(0, self.update_message, "No description returned from Ollama")
            except OllamaError as oe:
                self.root.after(0, self.update_message, f"Ollama error: {oe}")
            except Exception as e:
                self.root.after(0, self.update_message, f"Unexpected error: {e}")
        else:
            self.root.after(0, self.update_message, "No frame available")

    def threaded_describe_content(self):
        threading.Thread(target=self.describe_content, daemon=True).start()

    def update_message(self, new_text):
        current_text = self.message_var.get()
        updated_text = (current_text + "\n" + new_text) if current_text else new_text
        self.message_var.set(updated_text)

    def text_to_speech(self):
        current_text = self.message_var.get()
        if not current_text:
            self.root.after(0, self.update_message, "No text to speak")
            return
        self.root.after(0, self.update_message, "Speaking...")
        try:
            ok = speak(current_text, lang=self.language_var.get())
            if not ok:
                self.root.after(0, self.update_message, "TTS backend failed or not available")
        except Exception as e:
            self.root.after(0, self.update_message, f"TTS error: {e}")
