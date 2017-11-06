# pip install requests
import requests
import uuid
from base64 import b64encode, b64decode
from hashlib import sha256
from time import time
from urllib import quote_plus, urlencode
from hmac import HMAC

resourceName = ''  # IoT Hub name
resourceKey = '' # IoT Hub primary key
deviceId = 'device1' # IoT Hub device id
resourceURI = resourceName + '.azure-devices.net'
tokenExpirationPeriod = 60
policyKeyName = 'iothubowner'
apiVersion = '2016-02-03'

def get_iot_hub_sas_token(uri, key, policy_name, expiry=3600):
    ttl = time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
    signature = b64encode(HMAC(b64decode(key), sign_key, sha256).digest())

    rawtoken = {
        'sr' :  uri,
        'sig': signature,
        'se' : str(int(ttl))
    }

    if policy_name is not None:
        rawtoken['skn'] = policy_name

    return 'SharedAccessSignature ' + urlencode(rawtoken)

iotHubSasToken = get_iot_hub_sas_token(resourceURI, resourceKey, policyKeyName, tokenExpirationPeriod)
fileUploadRequestURI = 'https://%s/devices/%s/files?api-version=%s' % (resourceURI, deviceId, apiVersion)
fileUploadURITemplate = 'https://%s/%s/%s%s'
notificationURI = 'https://%s/devices/%s/files/notifications?api-version=%s' % (resourceURI, deviceId, apiVersion)

def upload_file(body, fileName, contentType, contentLength):

    # 1. GET FILE STORAGE URI
    fileUploadPartsResponse = requests.post(fileUploadRequestURI, 
        headers={
            'Authorization': iotHubSasToken,
            'Content-Type': 'application/json'
        },
        data = '{ "blobName": "%s"}' % (fileName)
    )

    print(fileUploadRequestURI)
    print(fileUploadPartsResponse.status_code)
    print(fileUploadPartsResponse.text)

    if fileUploadPartsResponse.status_code == 200:
 
        fileUploadParts = fileUploadPartsResponse.json()
        fileUploadURI = fileUploadURITemplate % (fileUploadParts["hostName"], fileUploadParts["containerName"], fileUploadParts["blobName"], fileUploadParts["sasToken"])
        
        # 2. UPLOAD FILE TO BLOB STORAGE
        uploadResponse = requests.put(fileUploadURI, 
            headers={
                'Content-Type': contentType,
                'Content-Length': contentLength,
                'x-ms-blob-type': 'BlockBlob',
                
            },
            data = body
        )

        print(fileUploadURI)
        print(uploadResponse.status_code)
        print(uploadResponse.text)
        
        if uploadResponse.status_code == 201:

            # 3. GET UPLOAD FILE NOTIFICATION
            notificationResponse = requests.post(notificationURI, 
                headers={
                    'Authorization': iotHubSasToken,
                    'Content-Type': 'application/json'
                },
                data = '{"correlationId": "%s" }' % (fileUploadParts["correlationId"])
            )
    
            print(notificationURI)
            print(notificationResponse.status_code)
            print(notificationResponse.text)

bodyText = '{ "device": "device1", "temp": 42 }'
upload_file(bodyText, str(uuid.uuid4()) + ".json", "application/json", str(len(bodyText)))

bodyBinary = open("iot.png", 'rb').read()
upload_file(bodyBinary, str(uuid.uuid4()) + ".png", "image/png", str(len(bodyBinary)))
