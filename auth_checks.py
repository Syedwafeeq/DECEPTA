import re

class EmailAuthAnalyzer:
    def __init__(self):
        pass

    def analyze(self, headers):
        auth_results = headers.get("arc-authentication-results", "")
        auth_results = auth_results.lower() if auth_results else ""

        spf = self._extract_result(auth_results, "spf")
        dkim = self._extract_result(auth_results, "dkim")
        dmarc = self._extract_result(auth_results, "dmarc")

        risk_flags = []
        score = 0.0

        if spf == "fail":
            risk_flags.append("spf_fail")
            score += 0.2

        if dkim == "fail":
            risk_flags.append("dkim_fail")
            score += 0.2

        if dmarc == "fail":
            risk_flags.append("dmarc_fail")
            score += 0.3

        return {
            "auth_results": {
                "spf": spf,
                "dkim": dkim,
                "dmarc": dmarc
            },
            "auth_risk_score": min(score, 1.0),
            "auth_flags": risk_flags
        }

    def _extract_result(self, text, key):
        match = re.search(rf"{key}=(pass|fail|none)", text)
        return match.group(1) if match else "unknown"
