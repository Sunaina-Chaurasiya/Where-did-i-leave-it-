import cv2
from ultralytics import YOLO
from datetime import datetime
from database import save_item_to_db

# Load the YOLOv8 model (you can replace this with your trained model path)
model = YOLO("yolov8s.pt")

# This function is called from Flask while streaming video
def detect_objects(frame):
    results = model(frame, verbose=False)

    for result in results:
        if result.boxes:
            names = model.names
            for box in result.boxes:
                cls_id = int(box.cls[0])
                label = names[cls_id]
                confidence = float(box.conf[0])
                detected_item = label
                detected_location = f"({box.xyxy[0][0]:.2f}, {box.xyxy[0][1]:.2f})"

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                    (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                    (0, 255, 0),
                    2
                )

                # Label with item name and confidence
                cv2.putText(
                    frame,
                    f"{label} ({confidence:.2f})",
                    (int(box.xyxy[0][0]), int(box.xyxy[0][1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

                # Save to database
                save_item_to_db(detected_item, detected_location)
                print(f"✅ Saved: {detected_item} at {detected_location} at {datetime.now()}")

    return frame

