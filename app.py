import cv2
import requests
import customtkinter as ctk
from PIL import Image

appWidth, appHeight = 1920, 1080

class MathExpressionRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Expression Recognizer")
        self.root.geometry(f"{appWidth}x{appHeight}")
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 1)
        self.root.grid_rowconfigure(0, weight = 1)

        # Create left and right frames
        self.left_frame = ctk.CTkFrame(root, corner_radius=2)
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.right_frame = ctk.CTkFrame(root, corner_radius=2)
        self.right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.camera_label = ctk.CTkLabel(self.left_frame, text="")
        self.camera_label.grid(pady=appHeight/4-20)

        # input text box to write the math expression
        self.input_label = ctk.CTkLabel(self.right_frame, text="Input:", font=("Arial", 30))
        self.input_label.grid(pady=10)

        self.input_text = ctk.CTkEntry(self.right_frame, font=("Arial", 30), corner_radius=2)
        self.input_text.grid(pady=10)

        self.execute_button = ctk.CTkButton(self.right_frame, text="Calculate", command=self.execute, font=("Arial", 40), corner_radius=2)
        self.execute_button.grid(padx=(appWidth/4)-100, pady=10)

        self.output_label = ctk.CTkLabel(self.right_frame, text="Output:", font=("Arial", 30))
        self.output_label.grid(pady=10)

        # Initialize the video capture object
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set camera width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # Set camera height
        self.show_camera_feed()

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #frame = cv2.resize(frame, (960, 720))
            image = Image.fromarray(frame)
            #image = ImageTk.PhotoImage(image)
            image = ctk.CTkImage(image, size=(appWidth/2,(appWidth/2)*0.5625))

            self.camera_label.configure(image=image)
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
        output_string = ""
        for i in range(20):
            output_string += f"{math_expression}\n"
        self.output_label.configure(text=f"{output_string}")

    def recognize_math_expression(self, image):
        # Use your math expression recognition model to process the image
        # Replace this with your actual recognition code
        api_key = "AU2LAE-TE4HQU7YEP"
        input_eq = self.input_text.get()
        # format the input equation to be used in the API call, all notation needs to be replaced with the corresponding URL encoding
        input_eq = input_eq.replace(" ", "%20").replace("+", "%2B").replace("/", "%2F").replace("=", "%3D")
        api_call = f"http://api.wolframalpha.com/v2/query?appid={api_key}&input={input_eq}&output=json"
        res = self.get_data(api_call)
        
        return res
    
    def get_data(self, api_call):
        response = requests.get(f"{api_call}")
        if response.status_code == 200:
            print("sucessfully fetched the data")
            json_res = response.json()
            res = json_res['queryresult']['pods'][1]['subpods'][0]['plaintext']
            # if the result is a line, get the plot
            if res=='line':
                res = json_res['queryresult']['pods'][2]['subpods'][0]['plaintext']
            # FIX THIS
            
            return res
        else:
            print(f"An error occured while sending API call: {response.status_code}")
            return None

def main():
    root = ctk.CTk()
    app = MathExpressionRecognizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
