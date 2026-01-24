import email
from email import policy
from email.parser import BytesParser

def parse_eml(file_path):
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    headers = {
    "from": str(msg.get("From")),
    "to": str(msg.get("To")),
    "subject": str(msg.get("Subject")),
    "reply_to": str(msg.get("Reply-To")),
    "authentication-results": str(msg.get("Authentication-Results"))
}

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    return headers, body
