import requests
import os

SUBSCRIPTION_KEY = os.getenv('ERCOT_SUBSCRIPTION_KEY')
USER_EMAIL = os.getenv('ERCOT_USERNAME')
USER_PASSWORD = os.getenv('ERCOT_PASSWORD')

# Authorization URL for signing into ERCOT Public API account
AUTH_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token\
?username={username}\
&password={password}\
&grant_type=password\
&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access\
&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70\
&response_type=id_token"

def get_token() -> str:
    # Sign In/Authenticate
    auth_response = requests.post(AUTH_URL.format(username = USER_EMAIL, password=USER_PASSWORD))

    # Retrieve access token
    access_token = auth_response.json().get("access_token")
    return access_token

print(get_token())
