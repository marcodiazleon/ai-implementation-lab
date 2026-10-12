"""R54a / D45: one definition of the sensitive patterns every guard uses.

Named formats only. There is no entropy analysis, no provider lookup and no claim of completeness:
a credential outside these formats passes. Spellings are split so that this file never matches itself.
"""
import re

# Label, pattern. Anthropic before OpenAI so that sk-ant- is reported under its own label.
PATTERNS = [
    ("Anthropic key", re.compile(r"\bsk-" + r"ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI key", re.compile(r"\bsk-" + r"(?!ant-)(?:proj-|svcacct-|admin-)?[A-Za-z0-9_-]{20,}")),
    # Context7 documents no key format in the README consulted (D45); this prefix is a courtesy, the bearer and
    # assignment patterns below are the real cover.
    ("Context7-style key", re.compile(r"\bctx7" + r"sk-[A-Za-z0-9_-]{16,}")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_" + r"[A-Za-z0-9]{30,}|github_pat_" + r"[A-Za-z0-9_]{40,})")),
    ("AWS access key id", re.compile(r"\b(?:AKIA|ASIA)" + r"[A-Z0-9]{16}\b")),
    ("Slack token", re.compile(r"\bxox" + r"[abprs]-[A-Za-z0-9-]{10,}")),
    ("Google API key", re.compile(r"\bAIza" + r"[0-9A-Za-z_-]{35}\b")),
    ("private key block", re.compile(r"-----BEGIN " + r"(?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")),
    ("bearer token", re.compile(r"(?i)\bbearer" + r"\s+[A-Za-z0-9._~+/=-]{20,}")),
    # A quoted value of 16+ characters, or an unquoted one that carries a digit (so `token=session.session_id` in code is not one).
    ("credential assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|passw" + r"ord|token)\b\s*[=:]\s*(?:\\?['\"][A-Za-z0-9._~+/-]{16,}\\?['\"]|(?=[A-Za-z0-9._~+/-]*\d)[A-Za-z0-9._~+/-]{16,})")),
    ("local personal path", re.compile(r"(?i)[A-Za-z]:\\{1,2}Users\\{1,2}" + r"[^\\\s\"']+|(?<![\w/.])/(?:Users|home)/" + r"[A-Za-z0-9._-]+/")),
]

# File names that are credentials by convention, regardless of content.
CREDENTIAL_SUFFIXES = {".pem", ".pfx", ".p12", ".key", ".ppk", ".jks", ".keystore"}
CREDENTIAL_NAMES = {".netrc", ".pypirc", ".npmrc", "credentials", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}


def find_secrets(text):
    """Labels of every named format found in the text, in pattern order, each once."""
    return [label for label, pattern in PATTERNS if pattern.search(text)]


def find_secrets_in(value):
    """R54g / D56: labels found in any string value of nested dicts and lists, raw, plus in the serialized whole.

    Serialization alone misses a quoted assignment (the escaped quote breaks the pattern), so every string is checked
    as it is. Nothing is evaluated; keys are strings too and are walked."""
    import json
    found = []
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            found += [label for label in find_secrets(item) if label not in found]
        elif isinstance(item, dict):
            stack.extend(item.keys()); stack.extend(item.values())
        elif isinstance(item, (list, tuple)):
            stack.extend(item)
    try:
        serialized = json.dumps(value, ensure_ascii=False, default=str)
    except (TypeError, ValueError):
        serialized = str(value)
    return found + [label for label in find_secrets(serialized) if label not in found]


def credential_file(name):
    """True for .env variants (except .env.example), key and certificate files and SSH key names."""
    base = name.rsplit("/", 1)[-1]
    lower = base.lower()
    if lower == ".env" or (lower.startswith(".env.") and lower != ".env.example"):
        return True
    return lower in CREDENTIAL_NAMES or any(lower.endswith(suffix) for suffix in CREDENTIAL_SUFFIXES)
