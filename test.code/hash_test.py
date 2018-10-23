import hashlib

user_password ="cookies"

hashpass = hashlib.md5(user_password.encode())

print(hashpass.hexdigest())
