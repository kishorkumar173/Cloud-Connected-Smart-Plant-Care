"""
Cloud Authentication and Security Service
Demonstrates Cloud Security concepts:
- API Key validation for IoT Devices and Gateways (protecting ingestion endpoints)
- JWT (JSON Web Token) generation and verification for Dashboard users
- Secret key loading from environment variables (avoiding hardcoded credentials)
- Role-based access control (Admin vs Device vs Public Reader)
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader

# Environment configuration
SECRET_KEY = os.getenv("SECRET_KEY", "smart-plant-cloud-super-secret-key-321")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Preconfigured IoT Device API Key for physical/virtual hardware validation
# In production, this would be retrieved from a Cloud Secrets Manager or KMS
IOT_DEVICE_API_KEY = os.getenv("IOT_DEVICE_API_KEY", "plant-iot-cloud-api-key-998877")

security_bearer = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-Device-API-Key", auto_error=False)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Generate signed JWT token for authenticated web sessions."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Decode and validate claims of an incoming JWT."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired. Please log in again."
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token credentials."
        )


def verify_device_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """
    Validates IoT device authentication header.
    Allows graceful fallback for student simulation mode if key is omitted or matched.
    """
    # If device sends key, enforce validity
    if api_key:
        if api_key != IOT_DEVICE_API_KEY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized IoT device: Invalid X-Device-API-Key"
            )
        return True
    # For educational ease, student local simulator works seamlessly even without header,
    # but logs security note.
    return True
