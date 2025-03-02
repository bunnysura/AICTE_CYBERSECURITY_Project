from flask import Flask, render_template, request, send_file
import cv2
import os

# Initialize Flask app
app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads/"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Encoding function (Image + Message to Secret Image)
def encode_message(img_path, msg):
    img = cv2.imread(img_path)
    d = {}
    c = {}
    
    # Create mappings for encoding and decoding
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    m = 0
    n = 0
    z = 0
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    encrypted_path = os.path.join(UPLOAD_FOLDER, "encryptedImage.jpg")
    cv2.imwrite(encrypted_path, img)
    return encrypted_path

# Decoding function (Extract Message from Image)
def decode_message(img_path, password, entered_password):
    if password != entered_password:
        return "YOU ARE NOT AUTHORIZED"
    
    img = cv2.imread(img_path)
    message = ""
    n = 0
    m = 0
    z = 0
    c = {}
    
    for i in range(255):
        c[i] = chr(i)

    for i in range(len(msg)):
        message += c[img[n, m, z]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3
    return message

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        password = request.form["password"]
        entered_password = request.form["entered_password"]

        # Handle Encoding
        if action == "Encode":
            if "image" not in request.files or "message" not in request.form:
                return "Error: Image and message are required"
            
            file = request.files["image"]
            message = request.form["message"]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Encode message in image
            encoded_path = encode_message(file_path, message)
            return send_file(encoded_path, as_attachment=True)

        # Handle Decoding
        elif action == "Decode":
            if "image" not in request.files:
                return "Error: Image is required"
            
            file = request.files["image"]
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Decode message from image
            decoded_message = decode_message(file_path, password, entered_password)
            return f"<h2>Decoded Message:</h2><p>{decoded_message}</p>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
