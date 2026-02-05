import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.match(email or ""))

def password_issues(password: str):
    issues = []
    pw = password or ""

    if len(pw) < 8:
        issues.append("Password must be at least 8 characters long.")
    if not any(c.islower() for c in pw):
        issues.append("Password must include at least one lowercase letter.")
    if not any(c.isupper() for c in pw):
        issues.append("Password must include at least one uppercase letter.")
    if not any(c.isdigit() for c in pw):
        issues.append("Password must include at least one number.")
    return issues
