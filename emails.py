def send_email(to: str, subject: str, body: str):
    print(f"Sending email to {to}: {subject} - {body}")


def send_prospect_email(email: str):
    subject = "Thank you for your interest"
    body = "We have received your lead and will get back to you soon."
    send_email(email, subject, body)


def send_attorney_email(attorney_email: str, lead):
    subject = "New lead submitted"
    body = f"A new lead has been submitted:\n\nFirst Name: {lead.first_name}\nLast Name: {lead.last_name}\nEmail: {lead.email}\nResume: {lead.resume_path}"
    send_email(attorney_email, subject, body)
