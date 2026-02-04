"""
Tasso Barcode Generator - Web Interface
Flask app for generating barcode PDFs via web upload
"""

import io
import os
from datetime import datetime

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

from tasso_barcode_generator import TassoBarcodeGenerator

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# Configure upload settings
ALLOWED_EXTENSIONS = {"csv"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def allowed_file(filename):
    """Check if file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Render the upload form."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generate PDF from uploaded CSV files."""
    # Check if files were uploaded
    if "csv_files" not in request.files:
        flash("No files selected", "error")
        return redirect(url_for("index"))

    files = request.files.getlist("csv_files")

    # Filter out empty file inputs
    files = [f for f in files if f.filename]

    if not files:
        flash("No files selected", "error")
        return redirect(url_for("index"))

    # Validate all files
    for file in files:
        if not allowed_file(file.filename):
            flash(f"Invalid file type: {file.filename}. Only CSV files are allowed.", "error")
            return redirect(url_for("index"))

    # Get options from form
    include_header = request.form.get("include_header") == "on"
    include_id = request.form.get("include_id") == "on"
    include_instruction = request.form.get("include_instruction") == "on"

    # Create temporary directory for processing
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save uploaded files
        csv_paths = []
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(tmpdir, filename)
            file.save(filepath)
            csv_paths.append(filepath)

        # Generate PDF to memory buffer
        output_buffer = io.BytesIO()

        # Create a temporary file for the PDF (reportlab needs a file path)
        pdf_path = os.path.join(tmpdir, "output.pdf")

        try:
            generator = TassoBarcodeGenerator(pdf_path)
            generator.generate(
                csv_paths,
                include_header=include_header,
                include_id=include_id,
                include_instruction=include_instruction,
            )

            # Read the generated PDF into buffer
            with open(pdf_path, "rb") as f:
                output_buffer.write(f.read())
            output_buffer.seek(0)

        except Exception as e:
            flash(f"Error generating PDF: {str(e)}", "error")
            return redirect(url_for("index"))

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if len(files) == 1:
        base_name = os.path.splitext(files[0].filename)[0]
        output_filename = f"{base_name}_{timestamp}.pdf"
    else:
        output_filename = f"tasso_barcodes_{timestamp}.pdf"

    return send_file(
        output_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=output_filename,
    )


@app.route("/health")
def health():
    """Health check endpoint for Heroku."""
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
