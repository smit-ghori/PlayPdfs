from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import uuid
import os
from pypdf import PdfWriter

app = Flask(__name__)

# Upload folder (Render compatible)
UPLOAD_FILES = "/tmp/uploads"
os.makedirs(UPLOAD_FILES, exist_ok=True)


# Function to save uploaded files
def save_uploaded_files(files):
    unique_id = str(uuid.uuid4())
    user_uploads = os.path.join(UPLOAD_FILES, unique_id)
    os.makedirs(user_uploads, exist_ok=True)

    saved_files = []

    for file in files:
        if not file or file.filename == "":
            continue

        file_path = os.path.join(user_uploads, file.filename)
        file.save(file_path)
        saved_files.append(file_path)

    return unique_id, saved_files


# Home page
@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/compress')
def compress():
    return render_template("compress.html")


# Merge PDF
@app.route('/merge', methods=['GET', 'POST'])
def merge():

    if request.method == "POST":

        files = request.files.getlist("pdfs")

        unique_id, saved_files = save_uploaded_files(files)

        writer = PdfWriter()

        for pdf in saved_files:
            writer.append(pdf)

        result_folder = os.path.join(UPLOAD_FILES, unique_id, "result")
        os.makedirs(result_folder, exist_ok=True)

        output_path = os.path.join(result_folder, "merged.pdf")

        with open(output_path, "wb") as f:
            writer.write(f)

        writer.close()

        return redirect(url_for("download_page", folder_id=unique_id))

    return render_template("merge.html")


# Download page
@app.route('/download/<folder_id>')
def download_page(folder_id):
    return render_template("download.html", folder_id=folder_id)


# Actual download
@app.route('/getfile/<folder_id>')
def getfile(folder_id):

    result_folder = os.path.join(UPLOAD_FILES, folder_id, "result")

    return send_from_directory(result_folder, "merged.pdf", as_attachment=True)