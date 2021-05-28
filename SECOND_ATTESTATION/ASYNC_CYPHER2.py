def encrypt(k, m):
    return ''.join(map(chr, (x ^ k for x in map(ord, m))))


def decrypt(k, m):
    return ''.join(map(chr, (x ^ k for x in map(ord, m))))


code = input("Введите текст: ")
key = int(input("Введите смещение: "))
codecs = encrypt(key, code)
decodecs = decrypt(key, codecs)

print(code)
print(codecs)
print(decodecs) 