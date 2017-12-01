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
parser.add_argument("--name", help="IoT Hub Name")
parser.add_argument("--key", help="IoT Hub (iothubowner) primary key")
parser.add_argument("--device-id", help="IoT Edge device Id")
parser.add_argument("--config-file", help="Full path to module config file")

if len(sys.argv) != 9:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

name = args.name  # IoT Hub name
key = args.key # IoT Hub primary key
deviceId = args.device_id # IoT Hub device id
configFile = args.config_file # Path to the configuration file

resourceURI = name + '.azure-devices.net'
tokenExpirationPeriod = 60
policyKeyName = 'iothubowner'
apiVersion = '2017-11-08-preview'
applyConfigurationURI = 'https://%s/devices/%s/applyConfigurationContent?api-version=%s' % (resourceURI, deviceId, apiVersion)

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

def get_config_file_contents(): 
    with open(args.config_file, 'r') as configFile:
        return configFile.read()

def apply_configuration():
    applyConfigurationResponse = requests.post(applyConfigurationURI, 
        headers={
            'Authorization': iotHubSasToken,
            'Content-Type': 'application/json'
        },
        data = get_config_file_contents()
    )

    print(applyConfigurationURI)
    print(applyConfigurationResponse.status_code)
    print(applyConfigurationResponse.text)

    if applyConfigurationResponse.status_code == 204:
        print("Configuration successfully applied.  Please run `docker logs edgeAgent -f` to see the change applied.")
    else:
        print("There was an error applying the configuration. You should see an error message above that indicates the issue.")

iotHubSasToken = get_iot_hub_sas_token(resourceURI, key, policyKeyName, tokenExpirationPeriod)
apply_configuration()