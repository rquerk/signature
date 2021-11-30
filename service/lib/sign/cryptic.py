import hashlib
import rsa


def digest(to_digest: bytes) -> bytes:
    """Creates a sha256 hash."""
    return hashlib.sha256(to_digest).digest()


def generate_key_pair(bits) -> ():
    public_key, private_key = rsa.newkeys(bits)
    return public_key, private_key


def encrypt_with_private_key(message: bytes, public_key) -> bytes:
    encrypted_msg = rsa.encrypt(message, public_key)
    return encrypted_msg


def decrypt_with_public_key(encrypted_msg, private_key) -> bytes:
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    return decrypted_msg


def str_to_raw(string):
    return fr"{string}"


# this function overwrites the file if it already exists,
# and creates a new file if it does not exist
def write_to_file(filename: str, content: str):
    with open(str_to_raw(filename), "w") as file:
        bytes_written = file.write(content)
    return bytes_written


def read_from_file(filename):
    with open(filename, "r") as file:
        content = file.read()
    return content
