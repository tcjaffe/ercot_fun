import datetime
import requests
import os

SCED_DT_FORMAT = 'yyyy-MM-ddTH24:mm:ss'

SUBSCRIPTION_KEY = os.getenv('ERCOT_SUBSCRIPTION_KEY')
USERNAME = os.getenv('ERCOT_USERNAME')
PASSWORD = os.getenv('ERCOT_PASSWORD')

# Authorization URL for signing into ERCOT Public API account
AUTH_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/oauth2/v2.0/token\
?username={username}\
&password={password}\
&grant_type=password\
&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access\
&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70\
&response_type=id_token"

LMP_BY_ELECTRICAL_BUS = "https://api.ercot.com/api/public-reports/np6-787-cd/lmp_electrical_bus\
?SCEDTimestampFrom={sced_from}\
&SCEDTimestampTo={sced_to}"

def get_token() -> str:
    # Sign In/Authenticate
    auth_response = requests.post(AUTH_URL.format(username = USERNAME, password=PASSWORD))

    # Retrieve access token
    access_token = auth_response.json().get("access_token")
    return access_token

def get_lmps_by_bus(access_token) -> str:
    token = get_token()
    
    sced_from = '2025-07-07T05:00:00'
    sced_to = '2025-07-07T05:30:00'
    bus = 'LZ_SOUTH'

    lmp_response = requests.get(
        headers={'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY, "Authorization": "Bearer " + access_token,},
        url=LMP_BY_ELECTRICAL_BUS.format(sced_from=sced_from, sced_to=sced_to))
    
    print(lmp_response)
    
    print(lmp_response.json())

    raise NotImplementedError()

access_token = get_token()
print(access_token)
get_lmps_by_bus(access_token)
