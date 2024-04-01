import secrets

token: str = secrets.token_urlsafe(32)

print(f'TOKEN JWT: {token}')