from eml_parser import parse_eml
from nlp_engine import PhishingNLPModule

def run_module_1(eml_path):
    headers, body = parse_eml(eml_path)
    nlp_engine = PhishingNLPModule()
    return nlp_engine.analyze_email(headers, body)

if __name__ == "__main__":
    eml_file = "samples/sample_phishing.eml"
    result = run_module_1(eml_file)
    print("\n=== MODULE 1 OUTPUT ===")
    print(result)
