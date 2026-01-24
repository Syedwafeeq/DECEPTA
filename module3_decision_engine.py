class DecisionEngine:
    def decide(self, nlp_result: dict, behavioral_result: dict) -> dict:

        nlp_score = nlp_result.get("phishing_score", 0.0)
        behavioral_score = behavioral_result.get("behavioral_score", 0.0)

        final_risk_score = round(
            (0.7 * nlp_score) + (0.3 * behavioral_score), 2
        )

        detected_cues = set(nlp_result.get("detected_cues", []))
        high_risk_cues = {
            "credential_request",
            "authority_impersonation",
            "urgency"
        }

        if detected_cues & high_risk_cues:
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

_decision_engine = DecisionEngine()

def run_decision_engine(nlp_result: dict, behavioral_result: dict) -> dict:
    return _decision_engine.decide(nlp_result, behavioral_result)
