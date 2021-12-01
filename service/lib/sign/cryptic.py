# import hashlib
import rsa


# hash = rsa.compute_hash(message, 'SHA-1')
# def digest(to_digest: bytes) -> bytes:
#    """Creates a sha256 hash."""
#    return hashlib.sha256(to_digest).digest()


def generate_key_pair(bits: int) -> ():
    public_key, private_key = rsa.newkeys(nbits=bits, poolsize=8)
    return public_key, private_key


# signature = rsa.sign_hash(hash, privkey, 'SHA-1')
def encrypt_with_private_key(message: bytes, public_key) -> bytes:
    encrypted_msg = rsa.encrypt(message, public_key)
    return encrypted_msg


def decrypt_with_public_key(encrypted_msg, private_key) -> bytes:
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    return decrypted_msg


def sign(message: bytes, private_key):
    return rsa.sign(message, private_key, "SHA-256")


def str_to_raw(string):
    return fr"{string}"


# this function overwrites the file if it already exists,
# and creates a new file if it does not exist
def write_to_file(filename: str, content: bytes):
    with open(filename, "wb") as file:
        bytes_written = file.write(content)
    return bytes_written


def read_from_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        content = file.read()
    return content


def read_key_from_file(filename):
    with open(filename, mode="rb") as file:
        key_data = file.read()
    return rsa.PrivateKey.load_pkcs1(key_data)


if __name__ == "__main__":
    keys = generate_key_pair(2048)

    public = keys[0]
    private = keys[1]

    write_to_file(r"/home/levi/public_key_file", public.save_pkcs1(format="PEM"))
    write_to_file(r"/home/levi/private_key_file", private.save_pkcs1(format="PEM"))

