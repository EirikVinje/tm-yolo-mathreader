import cv2
import tkinter as tk
from PIL import Image, ImageTk

class MathExpressionRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Expression Recognizer")

        self.camera_label = tk.Label(root)
        self.camera_label.pack()

        self.execute_button = tk.Button(root, text="Calculate", command=self.execute)
        self.execute_button.pack()

        self.output_label = tk.Label(root, text="Output:")
        self.output_label.pack()

        # Initialize the video capture object
        self.cap = cv2.VideoCapture(0)
        self.show_camera_feed()

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)

            self.camera_label.config(image=image)
            self.camera_label.image = image

            # Call this function again after 10 milliseconds
            self.root.after(10, self.show_camera_feed)
        else:
            self.root.after(10, self.show_camera_feed)

    def execute(self):
        # Capture image from webcam
        ret, frame = self.cap.read()

        # Process image to recognize math expression
        math_expression = self.recognize_math_expression(frame)

        # Update output label
        self.output_label.config(text=f"Output: {math_expression}")

    def recognize_math_expression(self, image):
        # Use your math expression recognition model to process the image
        # Replace this with your actual recognition code
        return "2 + 2 = 4"

def main():
    root = tk.Tk()
    app = MathExpressionRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
