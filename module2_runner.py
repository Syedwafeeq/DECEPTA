from eml_parser import parse_eml
from nlp_engine import PhishingNLPModule
from module2_behavioral import BehavioralAnalyzer

def run_module_2(eml_path):
    headers, body = parse_eml(eml_path)
    nlp_engine = PhishingNLPModule()
    nlp_result = nlp_engine.analyze_email(headers, body)
    behavioral_engine = BehavioralAnalyzer()
    behavioral_result = behavioral_engine.analyze(headers, body)
    return {
        "nlp_analysis": nlp_result,
        "behavioral_analysis": behavioral_result
    }

if __name__ == "__main__":
    result = run_module_2("samples/sample_phishing.eml")
    print("\n=== MODULE 2 OUTPUT ===")
    print(result)
