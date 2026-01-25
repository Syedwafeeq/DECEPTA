# ======================================================
# MODULE 3 RUNNER
# Unified entry point for Email, Voice, and Chat analysis
# ======================================================

from eml_parser import parse_eml
from nlp_engine import run_nlp
from module2_behavioral import run_behavioral
from module3_decision_engine import run_decision_engine


# ======================================================
# EMAIL PIPELINE
# ======================================================

def run_module_3(eml_file_path: str) -> dict:
    """
    Full phishing detection pipeline for EMAIL input (.eml files)
    """

    # Parse email
    headers, body = parse_eml(eml_file_path)

    # Build combined text for NLP
    full_text = build_text_from_email(headers, body)

    # Run NLP analysis
    nlp_result = run_nlp(full_text)

    # Run behavioral analysis (email-specific)
    behavioral_result = run_behavioral(headers, body)

    # Final decision
    decision = run_decision_engine(nlp_result, behavioral_result)

    return {
        "nlp_analysis": nlp_result,
        "behavioral_analysis": behavioral_result,
        "decision_engine": decision
    }


# ======================================================
# TEXT PIPELINE (VOICE TRANSCRIPTS / CHAT MESSAGES)
# ======================================================

def run_module_3_from_text(text: str) -> dict:
    """
    Full phishing detection pipeline for TEXT input
    Used for:
    - Live voice transcripts
    - Chat messages
    """

    # Run NLP analysis
    nlp_result = run_nlp(text)

    # Behavioral analysis is minimal for voice/chat
    behavioral_result = {
        "behavioral_flags": [],
        "behavioral_score": 0.0
    }

    # Final decision
    decision = run_decision_engine(nlp_result, behavioral_result)

    return {
        "nlp_analysis": nlp_result,
        "behavioral_analysis": behavioral_result,
        "decision_engine": decision
    }


# ======================================================
# HELPER FUNCTION
# ======================================================

def build_text_from_email(headers: dict, body: str) -> str:
    """
    Combine important email fields into a single text blob
    for NLP analysis
    """

    subject = headers.get("subject", "")
    sender = headers.get("from", "")
    receiver = headers.get("to", "")

    combined_text = f"""
From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""

    return combined_text.strip()
