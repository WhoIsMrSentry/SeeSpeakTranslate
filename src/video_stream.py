import cv2
from PIL import Image, ImageTk
import tkinter as tk


class VideoStreamHandler:
    def __init__(self, root: tk.Tk, canvas: tk.Canvas):
        self.root = root
        self.canvas = canvas
        self.cap = None
        self.photo = None
        self.current_frame = None
        self._running = False
        self._canvas_image_id = None

    def start_stream(self, camera_index: str | int):
        # Stop previous stream if any
        self.stop_stream()
        self.cap = cv2.VideoCapture(int(camera_index))
        self._running = True
        # initialize canvas image id to avoid creating multiple items
        if self._canvas_image_id is None:
            # create a blank image placeholder
            w = int(self.canvas.cget("width"))
            h = int(self.canvas.cget("height"))
            blank = ImageTk.PhotoImage(Image.new("RGB", (w, h), (0, 0, 0)))
            self._canvas_image_id = self.canvas.create_image(0, 0, image=blank, anchor=tk.NW)
            self.photo = blank
        # start update loop on main thread
        self._update_frame()

    def _update_frame(self):
        if not self._running or self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            try:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=img)
                # update existing canvas image item
                if self._canvas_image_id is not None:
                    self.canvas.itemconfig(self._canvas_image_id, image=self.photo)
                else:
                    self._canvas_image_id = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            except Exception:
                pass
        # schedule next frame; ~30 FPS => 33 ms
        self.root.after(33, self._update_frame)

    def stop_stream(self):
        self._running = False
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    # kept for backward compatibility with older name
    def stop_video(self):
        self.stop_stream()

    def get_current_frame(self):
        return self.current_frame
