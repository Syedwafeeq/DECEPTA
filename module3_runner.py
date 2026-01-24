"""
Module 3 Runner
----------------
This file orchestrates:
- NLP analysis (Module 1)
- Behavioral analysis (Module 2)
- Decision engine (Module 3)

It supports BOTH:
- Email (.eml) based analysis
- Direct text analysis (voice/chat transcripts)
"""

from eml_parser import parse_eml
from nlp_engine import run_nlp
from module2_behavioral import run_behavioral
from module3_decision_engine import run_decision_engine


# ======================================================
# EMAIL-BASED ENTRY POINT
# ======================================================

def run_module_3(eml_file_path: str) -> dict:
    """
    Full phishing detection pipeline for EMAIL input
    """
    headers, body = parse_eml(eml_file_path)
    full_text = build_text_from_email(headers, body)

    nlp_result = run_nlp(full_text)
    behavioral_result = run_behavioral(headers, body)
    decision = run_decision_engine(nlp_result, behavioral_result)

    return {
        "nlp_analysis": nlp_result,
        "behavioral_analysis": behavioral_result,
        "decision_engine": decision
    }


# ======================================================
# TEXT-ONLY ENTRY POINT (VOICE / CHAT)
# ======================================================

def run_module_3_from_text(text: str) -> dict:
    """
    Full phishing detection pipeline for TEXT input
    (used for voice transcripts and chat messages)
    """
    nlp_result = run_nlp(text)

    # For voice/chat, behavioral signals are limited
    behavioral_result = {
        "behavioral_flags": [],
        "behavioral_score": 0.0
    }

    decision = run_decision_engine(nlp_result, behavioral_result)

    return {
        "nlp_analysis": nlp_result,
        "behavioral_analysis": behavioral_result,
        "decision_engine": decision
    }


# ======================================================
# HELPER
# ======================================================

def build_text_from_email(headers: dict, body: str) -> str:
    """
    Combine important email fields into one text blob
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
