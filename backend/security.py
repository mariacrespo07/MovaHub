import hashlib
import hmac
import os

ITERACOES = 200_000


def hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES)
    return f"pbkdf2_sha256${ITERACOES}${salt.hex()}${dk.hex()}"


def verificar_senha(senha: str, armazenado: str) -> bool:
    if not armazenado:
        return False

    # senha criptografada (criada pelo criar_usuario.py)
    if armazenado.startswith("pbkdf2_sha256$"):
        try:
            _, iteracoes, salt_hex, hash_hex = armazenado.split("$")
            dk = hashlib.pbkdf2_hmac(
                "sha256", senha.encode("utf-8"), bytes.fromhex(salt_hex), int(iteracoes)
            )
            return hmac.compare_digest(dk.hex(), hash_hex)
        except (ValueError, AttributeError):
            return False

    # senha em texto puro (como nos usuários de teste do banco)
    return hmac.compare_digest(senha.encode("utf-8"), armazenado.encode("utf-8"))