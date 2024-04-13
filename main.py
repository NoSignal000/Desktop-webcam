import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # Open default camera
        self.is_camera_open = True
        self.captured_image = None

        self.root = tk.Tk()
        self.root.title("Camera App")
        

        self.initialize_ui()


    def initialize_ui(self):
        # Camera output label
        self.camera_label = tk.Label(self.root)
        self.camera_label.pack()

        # Button layout
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        # Take photo button
        self.capture_button = tk.Button(self.button_frame, text="Take Photo", command=self.capture_photo)
        self.capture_button.pack(side=tk.LEFT, padx=10, anchor="center")

        # Close button
        self.close_button = tk.Button(self.button_frame, text="Close Camera", command=self.close_window)
        self.close_button.pack(side=tk.LEFT, padx=10, anchor="center")

        self.root.after(10, self.update_camera_frame)
        self.root.mainloop()


    def update_camera_frame(self):
        ret, frame = self.camera.read()  # Read camera frame
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img)
            self.camera_label.configure(image=img)
            self.camera_label.image = img
        self.root.after(10, self.update_camera_frame)


    def toggle_camera(self):
        if self.is_camera_open:
            self.camera.release()
            self.camera_label.configure(image=None)
            self.capture_button.configure(text="Open Camera")
            self.is_camera_open = False
        else:
            self.camera = cv2.VideoCapture(0)  # Re-open camera
            self.capture_button.configure(text="Close Camera")
            self.is_camera_open = True
 

    def capture_photo(self):
        ret, self.captured_image = self.camera.read()
        if ret:
            self.show_capture_window()


    def show_capture_window(self):
        
        # Create a new window for capture confirmation or retake
        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.title("Capture Window")
        
        # self.capture_window.grab_set()

        # Display captured image
        img = Image.fromarray(cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(self.capture_window, image=img)
        label.image = img
        label.pack()
        
        # Button layout
        button_frame = tk.Frame(self.capture_window)
        button_frame.pack(pady=10)

        # Save button
        save_button = tk.Button(button_frame, text="Save", command=self.save_photo)
        save_button.pack(side=tk.LEFT, padx=10)

        # Retake button
        retake_button = tk.Button(button_frame, text="Retake", command=self.close_capture_window)
        retake_button.pack(side=tk.LEFT, padx=10)


    def save_photo(self):
        # Get the file path where the user wants to save the photo
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            # Save the image to the specified file path
            cv2.imwrite(file_path, self.captured_image)
            messagebox.showinfo("Save", "Photo saved successfully")
            self.capture_window.focus_force()
            self.close_capture_window()


    def close_capture_window(self):
        self.capture_window.destroy()


    def close_window(self):
        if self.is_camera_open:
            self.camera.release()
        self.root.destroy()


if __name__ == "__main__":
    app = CameraApp()
