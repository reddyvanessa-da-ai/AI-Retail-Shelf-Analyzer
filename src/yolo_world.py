from ultralytics import YOLO
from collections import Counter
import cv2
import os
import pandas as pd

# Load YOLO-World model
model = YOLO("yolov8s-world.pt")

# Define retail classes
model.set_classes([
    "snack bag",
    "potato chips",
    "biscuit packet",
    "drink can",
    "juice carton",
    "plastic bottle"
])

# Run detection
results = model.predict(
    source="data/raw/shelf.jpg",
    imgsz=1600,
    conf=0.08,
    iou=0.5,
    save=False
)

result = results[0]

# Read image
img = cv2.imread("data/raw/shelf.jpg")   # Change to shelf.jpeg if needed

counts = Counter()
inventory = []

# Draw detections
for box in result.boxes:

    cls = int(box.cls[0])
    label = result.names[cls]
    confidence = float(box.conf[0])
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    counts[label] += 1

    inventory.append({
        "Product": label,
        "Confidence": round(confidence, 2)
    })

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.putText(
        img,
        f"{label} {confidence:.2f}",
        (x1, y1 - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 0),
        2,
    )

# Create folders
os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/reports", exist_ok=True)

# Save detected image
cv2.imwrite("outputs/images/detected_shelf.jpg", img)

# Save CSV
df = pd.DataFrame(inventory)

label_map = {
    "snack bag": "Snack Packet",
    "drink can": "Beverage Can",
    "potato chips": "Potato Chips",
    "biscuit packet": "Biscuit Packet",
    "plastic bottle": "Plastic Bottle",
    "juice carton": "Juice Carton"
}

df["Product"] = df["Product"].replace(label_map)
df.to_csv("outputs/reports/inventory.csv", index=False)

# Print summary
print("\n========== INVENTORY SUMMARY ==========")

for item, count in counts.items():
    print(f"{item:<20} : {count}")

print("\nTotal Products Detected :", len(inventory))

print("\nFiles Saved Successfully")
print("Image : outputs/images/detected_shelf.jpg")
print("CSV   : outputs/reports/inventory.csv")