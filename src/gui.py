import tkinter as tk
from src.video_stream import VideoStreamHandler
from src.content_description import ContentDescriber


class AppGui:
    def __init__(self, width=640, height=480, title='SeeSpeakTranslate'):
        # Dark theme defaults
        self.theme = {
            'bg': '#0f0f0f',
            'fg': '#ffffff',
            'btn_bg': '#1f1f1f',
            'btn_fg': '#ffffff',
            'entry_bg': '#1a1a1a',
            'entry_fg': '#ffffff',
        }

        self.root = tk.Tk()
        self.root.title(title)
        self.root.configure(bg=self.theme['bg'])

        self.user_input = tk.Entry(self.root, width=50, bg=self.theme['entry_bg'], fg=self.theme['entry_fg'], insertbackground=self.theme['entry_fg'])
        self.user_input.pack(padx=8, pady=8)

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg=self.theme['bg'], highlightthickness=0)
        self.canvas.pack()

        self.video_handler = VideoStreamHandler(self.root, self.canvas)
        self.content_describer = ContentDescriber(self.root, self.user_input, self.video_handler, theme=self.theme)

    def run(self):
        self.root.mainloop()
