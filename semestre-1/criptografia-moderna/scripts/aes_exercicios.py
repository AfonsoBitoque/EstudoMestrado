#!/usr/bin/env python3
"""Scripts para exercícios 39–41 (Prof. Daniel Graça). Requer: pip install cryptography"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def aes_ecb(key: bytes, plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    enc = cipher.encryptor()
    return enc.update(plaintext) + enc.finalize()


def aes_cbc(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor()
    return enc.update(plaintext) + enc.finalize()


def main() -> None:
    key = b"\x00" * 32  # AES-256

    # Ex 39: 16 bytes ASCII 'A' (interpretação comum de 32 hex 'A' = 16 bytes 0xAA)
    msg39_a = b"A" * 16
    msg39_b = bytes.fromhex("A" * 32)
    print("Ex 39 (16x 'A' ASCII):", aes_ecb(key, msg39_a).hex())
    print("Ex 39 (16 bytes 0xAA):  ", aes_ecb(key, msg39_b).hex())

    # Ex 40: 128 bytes 'A' ECB
    msg40 = b"A" * 128
    ct40 = aes_ecb(key, msg40)
    print("Ex 40 (first block):    ", ct40[:16].hex())
    print("Ex 40 (blocks equal):   ", len(set(ct40[i : i + 16] for i in range(0, 128, 16))) == 1)

    # Ex 41: CBC, IV = 32 hex '8' = 16 bytes 0x88
    iv = bytes.fromhex("8" * 32)
    ct41 = aes_cbc(key, iv, msg40)
    print("Ex 41 (first block):    ", ct41[:16].hex())


if __name__ == "__main__":
    main()
