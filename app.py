"""
Albert Sound Controller by Light Intensity
A minimal widget that controls Windows volume based on webcam brightness.
"""

import sys
import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import tkinter as tk
from PIL import Image, ImageTk

class SoundController:
    def __init__(self):
        # Window setup
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("280x160")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)  # Frameless
        
        # Make window draggable
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.on_drag)
        
        # Rounded corners background (white with slight transparency effect)
        self.root.configure(bg="#f5f5f7")
        
        # Main frame
        self.frame = tk.Frame(self.root, bg="#f5f5f7")
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: Webcam
        self.cam_label = tk.Label(self.frame, bg="#000000", width=200, height=140)
        self.cam_label.pack(side="left", fill="both", expand=True)
        
        # Right: Volume bar + close button
        self.right_frame = tk.Frame(self.frame, bg="#f5f5f7", width=50)
        self.right_frame.pack(side="right", fill="y", padx=(10, 0))
        self.right_frame.pack_propagate(False)
        
        # Close button
        self.close_btn = tk.Label(
            self.right_frame, text="✕", font=("Arial", 10), 
            bg="#e5e5e5", fg="#666666", width=2, height=1, cursor="hand2"
        )
        self.close_btn.pack(pady=(0, 5))
        self.close_btn.bind("<Button-1>", lambda e: self.cleanup())
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.configure(bg="#ff6b6b", fg="white"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.configure(bg="#e5e5e5", fg="#666666"))
        
        # Volume bar container
        self.bar_container = tk.Frame(self.right_frame, bg="#e5e5e5", width=30)
        self.bar_container.pack(fill="both", expand=True, pady=(0, 5))
        
        # Volume bar fill
        self.bar_fill = tk.Frame(self.bar_container, bg="#007aff", width=30)
        self.bar_fill.place(relx=0, rely=1, relwidth=1, relheight=0, anchor="sw")
        
        # Volume text
        self.vol_label = tk.Label(self.right_frame, text="0%", font=("Arial", 9, "bold"), bg="#f5f5f7", fg="#1d1d1f")
        self.vol_label.pack()
        
        # Audio setup
        self.setup_audio()
        
        # Webcam setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        
        # Control variables
        self.current_volume = self.get_volume()
        self.smoothing = 0.15
        self.min_brightness = 30
        self.max_brightness = 200
        
        # Start the loop
        self.update()
        self.root.mainloop()
    
    def setup_audio(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
    
    def get_volume(self):
        return self.volume_ctrl.GetMasterVolumeLevelScalar() * 100
    
    def set_volume(self, percent):
        percent = max(0, min(100, percent))
        self.volume_ctrl.SetMasterVolumeLevelScalar(percent / 100.0, None)
    
    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y
    
    def on_drag(self, event):
        x = self.root.winfo_x() + event.x - self.drag_x
        y = self.root.winfo_y() + event.y - self.drag_y
        self.root.geometry(f"+{x}+{y}")
    
    def update(self):
        ret, frame = self.cap.read()
        if ret:
            # Mirror and resize
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (180, 120))
            
            # Calculate brightness
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            
            # Map to volume
            clamped = max(self.min_brightness, min(self.max_brightness, brightness))
            target = (clamped - self.min_brightness) / (self.max_brightness - self.min_brightness) * 100
            
            # Smooth
            self.current_volume += self.smoothing * (target - self.current_volume)
            self.set_volume(self.current_volume)
            
            # Update volume bar
            vol_pct = self.current_volume / 100
            self.bar_fill.place(relx=0, rely=1, relwidth=1, relheight=vol_pct, anchor="sw")
            self.vol_label.config(text=f"{int(self.current_volume)}%")
            
            # Update webcam display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.cam_label.imgtk = imgtk
            self.cam_label.configure(image=imgtk)
        
        self.root.after(33, self.update)  # ~30fps
    
    def cleanup(self):
        self.cap.release()
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    SoundController()
