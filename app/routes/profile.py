from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.patient import Patient
from app.models.caregiver import Caregiver

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/create-profile", methods=["GET", "POST"])
@login_required
def create_profile():
    # Prevent creating a duplicate profile for the same role
    if current_user.role == "patient" and current_user.patient_profile:
        flash("You already have a patient profile.", "error")
        return redirect(url_for("auth.dashboard"))

    if current_user.role == "caregiver" and current_user.caregiver_profile:
        flash("You already have a caregiver profile.", "error")
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        phone_number = request.form.get("phone_number", "").strip()

        if current_user.role == "patient":
            emergency_name = request.form.get("emergency_contact_name", "").strip()
            emergency_phone = request.form.get("emergency_contact_phone", "").strip()

            new_patient = Patient(
                user_id=current_user.id,
                phone_number=phone_number,
                emergency_contact_name=emergency_name,
                emergency_contact_phone=emergency_phone,
            )
            db.session.add(new_patient)

        else:  # caregiver
            relationship_to_patient = request.form.get("relationship_to_patient", "").strip()

            new_caregiver = Caregiver(
                user_id=current_user.id,
                phone_number=phone_number,
                relationship_to_patient=relationship_to_patient,
            )
            db.session.add(new_caregiver)

        db.session.commit()
        flash("Profile created successfully.", "success")
        return redirect(url_for("auth.dashboard"))

    return render_template("create_profile.html", role=current_user.role)