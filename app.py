from flask import Flask, render_template, request, redirect, url_for, flash
from detection import detect_blocking
from database import get_owner_by_vehicle
import os
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Persistent SMTP for faster emails ---
SENDER_EMAIL = "sender_mail@gmail.com"
SENDER_PASSWORD = "App_password"
smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp_server.login(SENDER_EMAIL, SENDER_PASSWORD)

# Update notifier.send_email to use persistent SMTP
def send_email_persistent(to_email, subject, body, image_path=None):
    try:
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(image_path)}",
                )
                msg.attach(part)

        smtp_server.send_message(msg)
        return True
    except Exception as e:
        print("Email sending error:", e)
        return False


# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ---------------- DETECT PAGE ----------------
@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            flash("No image selected.")
            return redirect(request.url)

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        status = detect_blocking(path)

        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")

        return render_template(
            "detect.html",
            image=file.filename,
            status=status,
            latitude=latitude,
            longitude=longitude,
        )

    return render_template("detect.html")


# ---------------- NOTIFY OWNER ----------------
@app.route("/notify", methods=["POST"])
def notify():
    vehicle_number = request.form.get("vehicle_number")
    owner = get_owner_by_vehicle(vehicle_number)

    image_name = request.form.get("image_path")
    image_path = os.path.join(UPLOAD_FOLDER, image_name) if image_name else None

    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    if owner:
        gps_link = (
            f"https://www.google.com/maps?q={latitude},{longitude}"
            if latitude and longitude else "Location not available"
        )

        body = f"""Dear {owner['owner']},
Your vehicle ({vehicle_number}) is blocking another.
Please move it.

Location: {gps_link}
"""
        if send_email_persistent(owner['email'], "Your vehicle is blocking another", body, image_path):
            flash("Notification sent successfully.", "success")
        else:
            flash("Failed to send notification.", "danger")
    else:
        flash("Owner not found in database.", "danger")

    return redirect(url_for("detect"))


if __name__ == "__main__":
    app.run(debug=True)
