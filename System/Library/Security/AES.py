import inspect
import os.path
import base64
import hashlib
import random
from Crypto.Cipher import AES as AESLocal
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2


def AESEncrypt(data: str, key: str) -> str:
    # Ensure the key is 16, 24, or 32 bytes long
    key = key.encode('utf-8')
    key = key.ljust(32, b'\0')[:32]

    # Convert data to bytes
    data = data.encode('utf-8')

    # Create cipher object and encrypt
    cipher = AESLocal.new(key, AESLocal.MODE_ECB)
    encrypted = cipher.encrypt(pad(data, AESLocal.block_size))

    # Encode the encrypted data as base64
    return base64.b64encode(encrypted).decode('utf-8')


def AESDecrypt(encrypted_data: str, key: str) -> str:
    # Ensure the key is 16, 24, or 32 bytes long
    key = key.encode('utf-8')
    key = key.ljust(32, b'\0')[:32]

    # Decode the base64 encrypted data
    encrypted = base64.b64decode(encrypted_data)

    # Create cipher object and decrypt
    cipher = AESLocal.new(key, AESLocal.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted), AESLocal.block_size)

    # Convert decrypted data back to string
    return decrypted.decode('utf-8')