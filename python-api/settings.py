import secrets

STATE = secrets.token_hex(16)

APP_ID = "2029698570782722"
SECRET_KEY = "Cbvbqlgxi8nObJjGGLlPkMhOpi1mt5js"
URI_REDIRECT = "https://www.google.com.br"

CODE_ID = "TG-67cf8a9f90667b0001b42d92-194398780"

AUTH_URL = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={APP_ID}&redirect_uri={URI_REDIRECT}"


AUTHORIZATION_DICT = {
'access_token': 'APP_USR-2029698570782722-031020-3de356a87fc793ec4b97a95619bff504-194398780',
 'token_type': 'Bearer',
 'expires_in': 21600,
 'scope': 'offline_access read write',
 'user_id': 194398780,
 'refresh_token': 'TG-67cf8ab55298d3000197d759-194398780'}