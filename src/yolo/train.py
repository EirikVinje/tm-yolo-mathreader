from ultralytics import YOLO
import argparse

def train():

    model = YOLO("yolov8s.pt") 

    model.train(data="/home/eirikmv/cv_project2/config.yaml", 
                epochs=10,
                imgsz=640,
                batch=32,
                device=0,
                project=f"runs/",
                name="run1",
                patience=100)

if __name__ == "__main__":
    
    train()
