from flask import Flask, render_template, request, redirect, url_for
import uuid
import os
from pypdf import PdfWriter

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# making directory for saving uploaded files 
UPLOAD_FILES = "/tmp/uploads"
if not os.path.exists(UPLOAD_FILES):
    os.makedirs(UPLOAD_FILES, exist_ok=True)

def save_uploaded_files(files):
    unique_id = str(uuid.uuid4())
    user_uploads = os.path.join(UPLOAD_FILES, unique_id)
    os.makedirs(user_uploads, exist_ok=True)

    saved_files = []
    for file in files:
        # if file name is empty
        if not file or file.filename == "":
            continue
        
        file_path = os.path.join(user_uploads, file.filename)
        file.save(file_path)
        saved_files.append(file_path)
        
    return unique_id, saved_files


@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == "POST":
        files = request.files.getlist("pdfs")
        
        # saving uploaded files 
        unique_id, saved_files = save_uploaded_files(files)

        # main logic
        writer = PdfWriter()
        for pdf in saved_files:
            writer.append(pdf)

        # saving system
        result_file = os.path.join(UPLOAD_FILES, unique_id, "result")
        os.makedirs(result_file, exist_ok=True)

        output_path = os.path.join(result_file, "merged.pdf")   # path for saving resultent file 
        writer.write(output_path)
        writer.close()
        
        return redirect(url_for("download", folder_id = unique_id))
    return render_template("merge.html")


# @app.route('/udfName(end_point)/<var (used to store from url)>')
@app.route('/download/<folder_id>')
def download(folder_id):
    return render_template("download.html")
app.run(debug=True)