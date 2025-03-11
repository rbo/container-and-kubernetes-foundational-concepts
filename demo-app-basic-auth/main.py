from flask import Flask, render_template_string, send_from_directory, request, Response
import os
import base64

port = int(os.environ.get("PORT", default=8080))
app = Flask(__name__)

# Load credentials from environment variables (set by Kubernetes Secret)
USERNAME = os.getenv("BASIC_AUTH_USER", "admin")
PASSWORD = os.getenv("BASIC_AUTH_PASS", "password")

# HTML template with a centered image and text
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Web App</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #000000;
        }
        img {
            max-width: 70%;
            height: auto;
            margin-bottom: 20px;
        }
        h1 {
            color: #f502d9;
        }
    </style>
</head>
<body>
    <img src="{{ image_url }}" alt="Centered Image">
    <h1>{{ message }}</h1>
</body>
</html>
"""

def check_auth(username, password):
    """Verify username and password from the request headers."""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Send a 401 response that enables Basic Auth."""
    return Response("Unauthorized", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.route("/")
def home():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    # Get the message and image path from environment variables or use defaults
    message = os.getenv("MESSAGE", "Hello, World!")
    image_path = os.getenv("IMAGE_PATH", "static/default.jpg")
    image_url = f"/images/{os.path.basename(image_path)}"
    print(f"Message: {message}, Image Path: {image_path}")  # Print to stdout
    return render_template_string(HTML_TEMPLATE, message=message, image_url=image_url)

@app.route("/images/<filename>")
def serve_image(filename):
    """Serve images from the static directory."""
    return send_from_directory("static", filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
