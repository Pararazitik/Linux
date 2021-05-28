class FileCrypter:
    def __init__(self, key: int):
        self.key = key

    def encryption(self, message: str) -> str:
        return "".join([chr(ord(message[i]) ^ self.key) for i in range(len(message))])


class DiffieHellman:

    def __init__(self, a: int, p: int, g: int):
        self._a = a
        self._p = p
        self._g = g

    @property
    def mixed_key(self):
        return self._g ** self._a % self._p

    def generate_key(self, mixed_key):
        return mixed_key ** self._a % self._p

    @property
    def auth_keys(self):
        return self._p, self._g, self.mixed_key