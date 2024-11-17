import secrets

# Generate a 256-bit secret key (32 bytes long)
secret_key = secrets.token_hex(32)
print(f"Generated Secret Key: {secret_key}")
