"""
Funciones de seguridad: hashing y verificación de contraseñas.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """
    Genera un hash seguro para una contraseña.

    Args:
        password (str): Contraseña en texto plano a hashear.

    Returns:
        str: Contraseña hasheada usando bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con un hash.

    Args:
        plain_password (str): Contraseña en texto plano a verificar.
        hashed_password (str): Hash de la contraseña almacenado.

    Returns:
        bool: True si coinciden, False en caso contrario.
    """
    return pwd_context.verify(plain_password, hashed_password)
