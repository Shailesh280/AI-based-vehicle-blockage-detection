import cv2
import numpy as np
from ultralytics import YOLO

def get_birds_eye_view(image, src_points):
    h, w = image.shape[:2]
    dst_points = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    warped = cv2.warpPerspective(image, matrix, (w, h))
    return warped, matrix

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    if xA >= xB or yA >= yB:
        return 0.0
    interArea = (xB - xA) * (yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return interArea / float(boxAArea + boxBArea - interArea)

def transform_box(box, matrix):
    x1, y1, x2, y2 = box
    pts = np.float32([
        [x1, y1],
        [x2, y1],
        [x2, y2],
        [x1, y2]
    ]).reshape(-1, 1, 2)
    transformed = cv2.perspectiveTransform(pts, matrix).reshape(-1, 2)
    tx1, ty1 = np.min(transformed, axis=0)
    tx2, ty2 = np.max(transformed, axis=0)
    return [tx1, ty1, tx2, ty2]

def detect_blocking(image_path):
    model = YOLO("yolov8n-seg.pt")  # Ensure model is present
    image = cv2.imread(image_path)
    results = model(image)[0]

    car_classes = [2, 5, 7]  # Car, bus, truck
    vehicle_boxes = []

    # Extract vehicle bounding boxes
    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id in car_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            vehicle_boxes.append([x1, y1, x2, y2])

    h, w = image.shape[:2]
    src_points = np.float32([
        [w * 0.25, h * 0.65],
        [w * 0.75, h * 0.65],
        [w * 0.95, h * 0.98],
        [w * 0.05, h * 0.98]
    ])
    _, matrix = get_birds_eye_view(image, src_points)

    transformed_boxes = [transform_box(box, matrix) for box in vehicle_boxes]

    blocked_status = [False] * len(vehicle_boxes)

    # Compare transformed boxes for overlap
    for i in range(len(transformed_boxes)):
        for j in range(len(transformed_boxes)):
            if i != j and iou(transformed_boxes[i], transformed_boxes[j]) > 0.25:
                blocked_status[i] = True

    # Annotate original image
    for i, box in enumerate(vehicle_boxes):
        x1, y1, x2, y2 = box
        color = (0, 0, 255) if blocked_status[i] else (0, 255, 0)
        label = "Blocked" if blocked_status[i] else "Not Blocked"
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    result_status = "Blocked" if any(blocked_status) else "Not Blocked"
    cv2.putText(image, f"Status: {result_status}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

    output_path = "car_blockage_output.jpg"
    cv2.imwrite(output_path, image)

    print(f"[✔] Processed. Saved to: {output_path}")
    return result_status
