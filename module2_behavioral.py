import re
from urllib.parse import urlparse


# ======================================================
# BEHAVIORAL ANALYZER CLASS
# ======================================================

class BehavioralAnalyzer:
    def analyze(self, headers: dict, body: str) -> dict:
        flags = []
        score = 0.0

        # -------------------------------
        # From / Reply-To mismatch
        # -------------------------------
        from_addr = headers.get("from", "")
        reply_to = headers.get("reply-to", "")

        if reply_to and from_addr and reply_to != from_addr:
            flags.append("from_reply_to_mismatch")
            score += 0.2

        # -------------------------------
        # Suspicious URLs
        # -------------------------------
        urls = re.findall(r'https?://\S+', body)

        for url in urls:
            parsed = urlparse(url)

            # IP-based URLs
            if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc):
                flags.append("ip_based_link")
                score += 0.2

            # Shortened URLs
            if parsed.netloc in ["bit.ly", "tinyurl.com", "t.co"]:
                flags.append("shortened_url")
                score += 0.2

        score = min(score, 1.0)

        return {
            "behavioral_flags": flags,
            "behavioral_score": round(score, 2)
        }


# ======================================================
# MODULE-LEVEL WRAPPER (IMPORTANT)
# ======================================================

_behavior_engine = BehavioralAnalyzer()

def run_behavioral(headers: dict, body: str) -> dict:
    """
    Unified behavioral analysis entry point
    used by module3_runner.py
    """
    return _behavior_engine.analyze(headers, body)
