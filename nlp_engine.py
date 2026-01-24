from transformers import pipeline
import re

# ======================================================
# NLP ENGINE CLASS
# ======================================================

class PhishingNLPModule:
    def __init__(self):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-1"
        )

        self.labels = [
            "phishing attempt",
            "credential harvesting",
            "urgent request",
            "authority impersonation",
            "legitimate email"
        ]

        self.urgency_words = [
            "urgent", "immediately", "within", "suspended",
            "locked", "expire", "final warning", "action required"
        ]

        self.credential_patterns = [
            r"password", r"otp", r"verification code",
            r"login", r"credentials", r"pin"
        ]

    # --------------------------------------------------
    # Linguistic Cue Extraction
    # --------------------------------------------------
    def extract_linguistic_cues(self, text: str):
        cues = set()
        lower = text.lower()

        for word in self.urgency_words:
            if word in lower:
                cues.add("urgency")

        for pattern in self.credential_patterns:
            if re.search(pattern, lower):
                cues.add("credential_request")

        if re.search(r"admin|support|security team|bank|it desk", lower):
            cues.add("authority_impersonation")

        if re.search(r"click|verify|confirm|update|reset", lower):
            cues.add("action_request")

        return list(cues)

    # --------------------------------------------------
    # CORE NLP ANALYSIS (TEXT-BASED)
    # --------------------------------------------------
    def analyze_text(self, text: str) -> dict:
        """
        Generic NLP analysis for ANY text input
        (email body, voice transcript, chat message)
        """

        classification = self.classifier(text, self.labels)
        scores = dict(zip(classification["labels"], classification["scores"]))

        base_score = max(
            scores.get("phishing attempt", 0),
            scores.get("credential harvesting", 0),
            scores.get("authority impersonation", 0)
        )

        cues = self.extract_linguistic_cues(text)

        cue_weight = 0.15
        cue_score = min(len(cues) * cue_weight, 0.6)

        phishing_score = min(base_score + cue_score, 1.0)

        return {
            "phishing_score": round(phishing_score, 2),
            "detected_cues": cues,
            "top_intent": classification["labels"][0],
            "confidence": (
                "high" if phishing_score > 0.75
                else "medium" if phishing_score > 0.4
                else "low"
            )
        }

    # --------------------------------------------------
    # EMAIL-SPECIFIC HELPER (BACKWARD COMPATIBLE)
    # --------------------------------------------------
    def analyze_email(self, headers: dict, body: str) -> dict:
        combined_text = f"""
        From: {headers.get('from', '')}
        Subject: {headers.get('subject', '')}

        {body}
        """
        return self.analyze_text(combined_text)


# ======================================================
# MODULE-LEVEL WRAPPER (IMPORTANT)
# ======================================================

# Create ONE shared NLP engine instance
_nlp_engine = PhishingNLPModule()

def run_nlp(text: str) -> dict:
    """
    Unified NLP entry point used by module3_runner.py

    This abstraction allows:
    - Email analysis
    - Voice transcript analysis
    - Chat message analysis
    """
    return _nlp_engine.analyze_text(text)
