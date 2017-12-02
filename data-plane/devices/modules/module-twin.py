# Python 2.7: Run 'pip install requests' first
# Python 3: Run 'pip3 install requests' first

import requests
import uuid
import sys
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from hmac import HMAC
import argparse

if sys.version_info.major >= 3:
    from urllib.parse import quote, urlencode
else:
    from urllib import quote, urlencode

parser = argparse.ArgumentParser(description="")
parser.add_argument("--name", help="IoT Hub Name", required=True)
parser.add_argument("--key", help="IoT Hub (iothubowner) primary key", required=True)
parser.add_argument("--device-id", help="IoT Edge device Id", required=True)
parser.add_argument("--module-id", help="IoT Edge device module Id, i.e. $edgeHub", required=True)
parser.add_argument("--key-name", help="IoT Hub policy key name, defaults to %(default)s", default="iothubowner")
parser.add_argument("--api-version", help="IoT Hub REST API version, defaults to %(default)s", default="2017-11-08-preview")

args = parser.parse_args()

name = args.name  # IoT Hub name
key = args.key # IoT Hub primary key
deviceId = args.device_id # IoT Hub device id
moduleId = args.module_id # IoT Hub device module id

resourceURI = name + '.azure-devices.net'
tokenExpirationPeriod = 60
policyKeyName = args.key_name
apiVersion = args.api_version

moduleTwinURI = 'https://%s/twins/%s/modules/%s?api-version=%s' % (resourceURI, deviceId, moduleId, apiVersion)

def get_iot_hub_sas_token(uri, key, policy_name, expiry=3600):
    ttl = time() + expiry
    sign_key = "%s\n%d" % ((quote(uri)), int(ttl))
    signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest())

    rawtoken = {
        'sr' :  uri,
        'sig': signature,
        'se' : str(int(ttl))
    }

    if policy_name is not None:
        rawtoken['skn'] = policy_name

    return 'SharedAccessSignature ' + urlencode(rawtoken)

def get_module_twin():
    moduleTwinResponse = requests.get(moduleTwinURI, 
        headers={
            'Authorization': iotHubSasToken,
            'Content-Type': 'application/json'
        }
    )

    print(moduleTwinURI)
    print(moduleTwinResponse.status_code)
    print(moduleTwinResponse.text)

iotHubSasToken = get_iot_hub_sas_token(resourceURI, key, policyKeyName, tokenExpirationPeriod)
get_module_twin()