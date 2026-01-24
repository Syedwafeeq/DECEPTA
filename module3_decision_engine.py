# ======================================================
# DECISION ENGINE
# ======================================================

class DecisionEngine:
    def decide(self, nlp_result: dict, behavioral_result: dict) -> dict:
        """
        Combines NLP and behavioral analysis results
        to produce a final phishing decision.
        """

        # -------------------------------
        # Extract scores
        # -------------------------------
        nlp_score = nlp_result.get("phishing_score", 0.0)
        behavioral_score = behavioral_result.get("behavioral_score", 0.0)

        # Weighted final risk score
        final_risk_score = round(
            (0.7 * nlp_score) + (0.3 * behavioral_score), 2
        )

        # -------------------------------
        # Cue-based escalation (CRITICAL)
        # -------------------------------
        detected_cues = set(nlp_result.get("detected_cues", []))
        high_risk_cues = {
            "credential_request",
            "authority_impersonation",
            "urgency"
        }

        # -------------------------------
        # Decision Logic
        # -------------------------------
        if detected_cues & high_risk_cues:
            # Voice / social engineering escalation
            if final_risk_score >= 0.25:
                decision = "WARN"
            else:
                decision = "ALLOW"
        else:
            if final_risk_score >= 0.75:
                decision = "BLOCK"
            elif final_risk_score >= 0.4:
                decision = "WARN"
            else:
                decision = "ALLOW"

        # -------------------------------
        # Explanation Generation
        # -------------------------------
        explanation = []

        if detected_cues:
            explanation.append(
                "The message uses social engineering tactics such as: "
                + ", ".join(sorted(detected_cues))
            )

        if behavioral_result.get("behavioral_flags"):
            explanation.append(
                "Suspicious behavior detected: "
                + ", ".join(behavioral_result["behavioral_flags"])
            )

        if decision == "ALLOW":
            explanation.append(
                "No immediate high-risk phishing indicators were detected."
            )
        elif decision == "WARN":
            explanation.append(
                "This content shows signs of social engineering. "
                "Verify the source before taking any action."
            )
        else:
            explanation.append(
                "High confidence phishing detected. "
                "Do not interact with this content."
            )

        return {
            "final_risk_score": final_risk_score,
            "decision": decision,
            "user_explanation": explanation
        }


# ======================================================
# MODULE-LEVEL WRAPPER
# ======================================================

_decision_engine = DecisionEngine()

def run_decision_engine(nlp_result: dict, behavioral_result: dict) -> dict:
    """
    Unified decision engine entry point
    used by module3_runner.py
    """
    return _decision_engine.decide(nlp_result, behavioral_result)
