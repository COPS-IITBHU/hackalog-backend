import pyAesCrypt
from os import stat
# encryption/decryption buffer size - 64K
# with stream-oriented functions, setting buffer size is mandatory
bufferSize = 64 * 1024
password = "please-use-a-long-random-password"

# encrypt
if password != "please-use-a-long-random-password":
    with open("firebase_admin.json", "rb") as fIn:
        with open("firebase_admin.aes", "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
else:
    raise ValueError("You cannot use template password, please use a long random password for encryption.\n\tYou are advised to edit the password(line: 6) before encrypting.")

# get encrypted file size
encFileSize = stat("firebase_admin.aes").st_size
print("FIREBASE_DECRYPT_SIZE =", encFileSize)

