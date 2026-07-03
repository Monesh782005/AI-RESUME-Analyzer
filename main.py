import os
import fitz
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from analyse_pdf import analyse_resume_gemini

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def extract_text_from_resume(pdf_path):
    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyse", methods=["POST"])
def analyse():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please choose a PDF"

    filename = secure_filename(file.filename)

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    resume_text = extract_text_from_resume(filepath)

    job_description = request.form["job_description"]

    result = analyse_resume_gemini(
        resume_text,
        job_description
    )

    return render_template(
        "result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)