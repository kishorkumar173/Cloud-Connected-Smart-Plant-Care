"""
Security Utilities for Input Sanitization and Rate Limiting
"""

import html
import re

def sanitize_string(text: str, max_length: int = 255) -> str:
    """Escapes HTML and strips dangerous characters to prevent XSS and injection."""
    if not text:
        return ""
    clean = html.escape(text.strip())
    # Remove control characters
    clean = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', clean)
    return clean[:max_length]
