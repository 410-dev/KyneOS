import base64
import random
import sys
if sys.platform == "darwin":
    from Cryptodome.Cipher import PKCS1_OAEP
    from Cryptodome.PublicKey import RSA
    from Cryptodome.Hash import SHA256
    from Cryptodome.Protocol.KDF import PBKDF2
else:
    from Crypto.Cipher import PKCS1_OAEP
    from Crypto.PublicKey import RSA
    from Crypto.Hash import SHA256
    from Crypto.Protocol.KDF import PBKDF2

def Encrypt(content: str, pubk: str) -> str:
    """Encrypt the content using the provided public key."""
    public_key = RSA.import_key(pubk)
    cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    encrypted = cipher.encrypt(content.encode())
    return base64.b64encode(encrypted).decode()


def Decrypt(content: str, prik: str) -> str:
    """Decrypt the content using the provided private key."""
    private_key = RSA.import_key(prik)
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    encrypted = base64.b64decode(content.encode())
    decrypted = cipher.decrypt(encrypted)
    return decrypted.decode()


def derive_deterministic_seed(password: str, salt: str, key_length: int = 32) -> bytes:
    """Derive a deterministic seed from the password and salt."""
    return PBKDF2(password.encode(), salt.encode(), dkLen=key_length, count=1000000, hmac_hash_module=SHA256)


def generate_consistent_rsa_key(seed: bytes) -> RSA.RsaKey:
    """Generate a consistent RSA key pair using the provided seed."""
    # Create a deterministic random number generator
    random.seed(seed)

    def deterministic_random(n):
        return bytes(random.randint(0, 255) for _ in range(n))

    # Generate the key using the deterministic random function
    key = RSA.generate(2048, randfunc=deterministic_random)
    return key


def MakeKeyPair(password: str, salt: str):
    """Generate and return both private and public keys as strings."""
    seed = derive_deterministic_seed(password, salt)
    key = generate_consistent_rsa_key(seed)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    return private_key, public_key


def GetPrivateKey(password: str, salt: str) -> str:
    """Get the private key as a string."""
    private_key, _ = MakeKeyPair(password, salt)
    return private_key


def GetPublicKey(password: str, salt: str) -> str:
    """Get the public key as a string."""
    _, public_key = MakeKeyPair(password, salt)
    return public_key


def get_key_hash(key: str) -> str:
    """Get a short hash of the key for easy comparison."""
    return SHA256.new(key.encode()).hexdigest()[:32]
