import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from app.extensions import db
from app.models.prescription import Prescription
from app.utils.file_validation import (
    is_allowed_file,
    get_file_type,
    generate_safe_filename,
    MAX_FILE_SIZE_BYTES,
)

prescriptions_bp = Blueprint("prescriptions", __name__)


@prescriptions_bp.route("/prescriptions/upload", methods=["GET", "POST"])
@login_required
def upload_prescription():
    # Only patients (or their profile) can upload prescriptions for themselves.
    # Caregiver-on-behalf-of-patient uploads are a future enhancement.
    if current_user.role != "patient" or not current_user.patient_profile:
        flash("Only patients with a completed profile can upload prescriptions.", "error")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        if "prescription_file" not in request.files:
            flash("No file selected.", "error")
            return redirect(url_for("prescriptions.upload_prescription"))

        file = request.files["prescription_file"]

        if file.filename == "":
            flash("No file selected.", "error")
            return redirect(url_for("prescriptions.upload_prescription"))

        if not is_allowed_file(file.filename):
            flash("Invalid file type. Only PNG, JPG, and PDF are allowed.", "error")
            return redirect(url_for("prescriptions.upload_prescription"))

        # Check file size by reading into memory position
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE_BYTES:
            flash("File is too large. Maximum size is 10 MB.", "error")
            return redirect(url_for("prescriptions.upload_prescription"))

        safe_filename = generate_safe_filename(file.filename)
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, safe_filename)
        file.save(file_path)

        prescription = Prescription(
            patient_id=current_user.patient_profile.id,
            original_filename=file.filename,
            stored_filename=safe_filename,
            file_type=get_file_type(file.filename),
            status="uploaded",
        )
        db.session.add(prescription)
        db.session.commit()

        flash("Prescription uploaded successfully.", "success")
        return redirect(url_for("prescriptions.my_prescriptions"))

    return render_template("upload_prescription.html")


@prescriptions_bp.route("/prescriptions")
@login_required
def my_prescriptions():
    if current_user.role != "patient" or not current_user.patient_profile:
        flash("Only patients can view prescriptions.", "error")
        return redirect(url_for("auth.dashboard"))

    prescriptions = (
        Prescription.query
        .filter_by(patient_id=current_user.patient_profile.id)
        .order_by(Prescription.uploaded_at.desc())
        .all()
    )
    return render_template("my_prescriptions.html", prescriptions=prescriptions)