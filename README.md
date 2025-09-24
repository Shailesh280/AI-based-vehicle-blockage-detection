# AI-Based Vehicle Blockage Detection System 🚗

### 📋 Project Overview

This project detects if a user's vehicle is blocked using a photo input and notifies the owner of the blocking vehicle.  
It uses computer vision and YOLOv8 for vehicle detection and sends automated email alerts with the image and location.

---

### 🧩 Features

- **Vehicle Blockage Detection:** Detects if a vehicle is blocking the user's car.  
- **Number Plate Input:** User can enter the number plate of the blocking vehicle.  
- **Automated Notification:** Sends an email with the image and location to the vehicle owner.  
- **User Input:** Works with photo uploads or images taken from the system.  

---

### ⚙️ Technologies Used

- **Computer Vision:** OpenCV and YOLO for vehicle detection  
- **Email Notifications:** SMTP for sending emails  
- **Location Detection:** Geolocation services to get coordinates of the image  
- **Web Framework / GUI:** Flask or Tkinter (depending on implementation)  

---

### 📁 Project Structure

```
AI-based-vehicle-blockage-detection/
│
├── app.py                # Main Flask application
├── database.py           # Database initialization and operations
├── detection.py          # Vehicle detection and segmentation logic
├── vehicles.py           # Vehicle data handling
├── yolov8n-seg.pt        # Pre-trained YOLOv8 model weights
│
└── templates/
    ├── index.html        # Main dashboard HTML
    └── detect.html       

```


### 🚀 Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Shailesh280/AI-based-vehicle-blockage-detection.git
   cd AI-based-vehicle-blockage-detection
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**

   ```bash
   python app.py
   ```

4. **Workflow:**

   - Upload/take a photo of the parking area  
   - The system detects if your vehicle is blocked  
   - If blocked:
     - Enter the number plate of the blocking vehicle  
     - Owner receives an email with the image and location  

---

### 📧 Email Configuration

- Update SMTP settings in `app.py` with your email credentials.  
- Ensure the sender email can send automated emails.

---

### 🛠️ Requirements

See [`requirements.txt`](./requirements.txt).

