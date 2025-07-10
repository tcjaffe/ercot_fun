"""A small client for interacting with ERCOT's REST API."""

from datetime import datetime, timedelta
import os
import requests

SUBSCRIPTION_KEY = os.getenv('ERCOT_SUBSCRIPTION_KEY')
USERNAME = os.getenv('ERCOT_USERNAME')
PASSWORD = os.getenv('ERCOT_PASSWORD')

# Authorization URL for signing into ERCOT Public API account
AUTH_URL = "https://ercotb2c.b2clogin.com/ercotb2c.onmicrosoft.com/B2C_1_PUBAPI-ROPC-FLOW/\
oauth2/v2.0/token\
?username={username}\
&password={password}\
&grant_type=password\
&scope=openid+fec253ea-0d06-4272-a5e6-b478baeecd70+offline_access\
&client_id=fec253ea-0d06-4272-a5e6-b478baeecd70\
&response_type=id_token"

# URL to pull LMPs for loading zones, hubs and nodes.
LMPS_NODES_ZONES_HUBS = "https://api.ercot.com/api/public-reports/np6-788-cd/lmp_node_zone_hub\
?SCEDTimestampFrom={sced_from}\
&SCEDTimestampTo={sced_to}\
&settlementPoint={settlement_point}"


def _get_headers(access_token: str) -> dict[str, str]:
    return {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        "Authorization": f"Bearer {access_token}",
    }


def _to_sced_format(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def get_token() -> str:
    """Returns a token for the current ERCOT session.  Lasts one hour."""
    # Sign In/Authenticate
    auth_response = requests.post(
        AUTH_URL.format(
            username=USERNAME,
            password=PASSWORD),
        timeout=30)

    # Retrieve access token
    return auth_response.json().get("access_token")


def get_lmps_for_nodes_zones_and_hubs(
        access_token: str,
        sced_from: datetime,
        sced_to: datetime,
        settlement_point: str) -> list:
    """Returns a list of lmps for a given timestamp range and settlement_point, eg 'LZ_NORTH'"""

    response = requests.get(
        headers=_get_headers(access_token),
        url=LMPS_NODES_ZONES_HUBS.format(
            sced_from=_to_sced_format(sced_from),
            sced_to=_to_sced_format(sced_to),
            settlement_point=settlement_point
        ),
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(response.json())

    return response.json()['data']


# Get the token first so you can use it in subsequent API calls.
token = get_token()

# I query for a 30 minute datetime range from the prior day.
# In the future I should incorporate timezone logic so I don't need to do prior day.
sced_to_dt = datetime.now() - timedelta(minutes=5, days=1)
sced_from_dt = sced_to_dt - timedelta(minutes=30)

for lz in ['LZ_NORTH', 'LZ_SOUTH', 'LZ_WEST', 'LZ_HOUSTON']:
    print(f'LMPs for load zone {lz}:')
    lz_houston_lmps = get_lmps_for_nodes_zones_and_hubs(
        access_token=token,
        sced_from=sced_from_dt,
        sced_to=sced_to_dt,
        settlement_point=lz)

    for lmp in lz_houston_lmps:
        print(lmp)
