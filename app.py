from flask import Flask, render_template, request, redirect, url_for, session
import os

from eml_parser import parse_eml
from module3_runner import run_module_3
from voice_runner import run_voice_analysis

from database import (
    init_db,
    init_user_table,
    init_exception_table,
    save_analysis,
    create_user,
    authenticate_user,
    add_exception,
    is_exception
)

# ---------------- APP SETUP ----------------

app = Flask(__name__)
app.secret_key = "hackathon-secret-key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DB INIT ----------------

init_db()
init_user_table()
init_exception_table()

# ---------------- AUTH DECORATOR ----------------

def login_required(func):
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# ---------------- AUTH ROUTES ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if authenticate_user(email, password):
            session["user"] = email
            return redirect(url_for("index"))
        else:
            error = "Invalid email or password"

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if create_user(email, password):
            return redirect(url_for("login"))
        else:
            error = "User already exists"

    return render_template("register.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- USER EXCEPTION ----------------

@app.route("/add_exception", methods=["POST"])
@login_required
def add_sender_exception():
    sender = request.form.get("sender")
    if sender:
        add_exception(session["user"], sender)
    return redirect(url_for("index"))

# ---------------- MAIN DASHBOARD ----------------

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    result = None
    email_preview = None
    dashboard = None

    if request.method == "POST":
        file = request.files.get("eml_file")

        if file and file.filename.endswith(".eml"):
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            headers, body = parse_eml(path)
            sender = headers.get("from", "")

            email_preview = {
                "from": sender,
                "to": headers.get("to", ""),
                "subject": headers.get("subject", ""),
                "body": body
            }

            # ---- CHECK USER EXCEPTION FIRST ----
            if is_exception(session["user"], sender):
                result = {
                    "nlp_analysis": {
                        "detected_cues": [],
                        "phishing_score": 0.0,
                        "top_intent": "trusted sender",
                        "confidence": "high"
                    },
                    "behavioral_analysis": {
                        "behavioral_flags": [],
                        "behavioral_score": 0.0
                    },
                    "decision_engine": {
                        "decision": "ALLOW",
                        "final_risk_score": 0.0,
                        "user_explanation": [
                            "Marked as exception by the user."
                        ]
                    }
                }
            else:
                result = run_module_3(path)

            save_analysis(headers, body, result)

            dashboard = {
                "nlp": {
                    "Urgency Language": "urgency" in result["nlp_analysis"]["detected_cues"],
                    "Authority Impersonation": "authority_impersonation" in result["nlp_analysis"]["detected_cues"],
                    "Credential Request": "credential_request" in result["nlp_analysis"]["detected_cues"],
                    "Action Forcing": "action_request" in result["nlp_analysis"]["detected_cues"]
                },
                "behavioral": {
                    "From / Reply-To Mismatch":
                        "from_reply_to_mismatch" in result["behavioral_analysis"]["behavioral_flags"],
                    "Suspicious Links":
                        any(flag in result["behavioral_analysis"]["behavioral_flags"]
                            for flag in ["shortened_url", "ip_based_link"])
                }
            }

    return render_template(
        "index.html",
        result=result,
        email_preview=email_preview,
        dashboard=dashboard,
        user=session["user"]
    )

# ---------------- VOICE PHISHING ROUTE ----------------

@app.route("/voice", methods=["POST"])
@login_required
def voice():
    file = request.files.get("voice_file")

    if not file:
        return redirect(url_for("index"))

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    transcript, result = run_voice_analysis(path)

    email_preview = {
        "from": "Voice Call",
        "to": "User",
        "subject": "Voice Phishing Transcript",
        "body": transcript
    }

    dashboard = {
        "nlp": {
            "Urgency Language": "urgency" in result["nlp_analysis"]["detected_cues"],
            "Authority Impersonation": "authority_impersonation" in result["nlp_analysis"]["detected_cues"],
            "Credential Request": "credential_request" in result["nlp_analysis"]["detected_cues"],
            "Action Forcing": "action_request" in result["nlp_analysis"]["detected_cues"]
        },
        "behavioral": {}
    }

    return render_template(
        "index.html",
        result=result,
        email_preview=email_preview,
        dashboard=dashboard,
        user=session["user"]
    )

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
