from app.auth.password import hash_password

password = "Password@123"

hashed_password = hash_password(password)

print(hashed_password)