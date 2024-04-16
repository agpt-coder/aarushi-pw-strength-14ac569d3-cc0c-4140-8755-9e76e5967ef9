from typing import List

from pydantic import BaseModel


class PasswordAnalysisResponse(BaseModel):
    """
    Provides a detailed analysis of the submitted password, including its strength, potential vulnerabilities, and suggestions for improvement.
    """

    strength_score: int
    strength_category: str
    vulnerabilities: List[str]
    suggestions: List[str]


def analyze_password(password: str) -> PasswordAnalysisResponse:
    """
    Endpoint for evaluating the strength of a submitted password.

    Args:
        password (str): The user's password input to be analyzed for strength and security.

    Returns:
        PasswordAnalysisResponse: Provides a detailed analysis of the submitted password, including its strength, potential vulnerabilities, and suggestions for improvement.
    """
    strength_score = 0
    vulnerabilities = []
    suggestions = []
    if len(password) < 8:
        vulnerabilities.append("Password is too short.")
        suggestions.append("Use at least 8 characters.")
    else:
        strength_score += 1
    if not any((char.isdigit() for char in password)):
        vulnerabilities.append("Password lacks digits.")
        suggestions.append("Include at least one digit.")
    else:
        strength_score += 1
    if not any((char.isupper() for char in password)):
        vulnerabilities.append("Password lacks uppercase letters.")
        suggestions.append("Include at least one uppercase letter.")
    else:
        strength_score += 1
    if not any((char.islower() for char in password)):
        vulnerabilities.append("Password lacks lowercase letters.")
        suggestions.append("Include at least one lowercase letter.")
    else:
        strength_score += 1
    if not any((char in "!@#$%^&*()-_=+[]{};':,.<>?/" for char in password)):
        vulnerabilities.append("Password lacks special characters.")
        suggestions.append("Include at least one special character.")
    else:
        strength_score += 1
    common_patterns = ["123456", "password", "qwerty"]
    if any((pattern in password for pattern in common_patterns)):
        vulnerabilities.append("Password contains common patterns.")
        suggestions.append("Avoid using common patterns or sequences.")
    if strength_score >= 5:
        strength_category = "Very Strong"
    elif strength_score >= 4:
        strength_category = "Strong"
    elif strength_score >= 3:
        strength_category = "Medium"
    else:
        strength_category = "Weak"
    return PasswordAnalysisResponse(
        strength_score=strength_score,
        strength_category=strength_category,
        vulnerabilities=vulnerabilities,
        suggestions=suggestions,
    )
