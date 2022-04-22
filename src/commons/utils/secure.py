from cryptography.fernet import Fernet


class Crypt:
    """
    This class may be used encrypt/decrypt raw strings.

    Use `cryptography.fernet.Fernet.generate_key()` method to generate the secret.
    """

    def __init__(self, secret):
        self._secret = secret
        self._algorithm = Fernet(secret)

    def encrypt(self, raw):
        """
        Encrypt raw string.

        Parameters:
            raw (str, required): Raw string to encrypt.

        Returns:
            str
        """
        return self._algorithm.encrypt(raw.encode())

    def decrypt(self, encrypted):
        """
        Decrypt encrypted string.

        Parameters:
            encrypted (str, required): Encrypted string to decrypt.

        Returns:
            str
        """
        return self._algorithm.decrypt(encrypted.encode()).decode()
