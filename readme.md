# Azure IoT REST

This repo contains sample code that will help you use the Azure IoT REST APIs.

## Prerequisites

### Azure Requirements
1. Azure IoT Hub
1. Azure IoT Hub Device
1. Azure Storage Account (to store the uploaded files, see [this blog post](http://blog.jongallant.com/2017/01/azure-iot-hub-file-upload-python/) for instructions on how to set this up)

### Dev Machine Requirements
1. Install [Python 2.7+](https://www.python.org/downloads/)
2. Run Python 2: `pip install requests` or Python 3: `pip3 install requests`
3. Clone this repo `git clone https://github.com/jonbgallant/azure-iot-rest.git`
4. Execute the scripts as indicated below.

### Authentication

#### Data Plane
The Azure IoT REST APIs hosted on azure-devices.net require a SAS Token Authorization header. You can find Python, Node and C# samples [here](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-security#security-tokens).

#### Control Plane
The Azure REST APIs hosted on management.azure.com require a Bearer Token Authorization header. See [Azure REST APIs with Postman in 2 Minutes](http://blog.jongallant.com/azure-rest-apis-postman) for instructions on how to generate a Bearer Token.

## APIs
### Devices
#### Configuration

IoT Edge devices are configured with metadata such as module paths and route settings.  That configuration is applied via the `applyConfigurationContent` API.  You can read more about Edge configuration [here](https://github.com/jonbgallant/azure-iot-edge-config).

Here's how to apply a configuration update:

##### Script

```
python data-plane/devices/device-conf.py --name [iothubname] --key [iothubkey] --device-id [deviceid] --config-file [path to module config]
```

##### REST API

```
POST /devices/{{deviceId}}/applyConfigurationContent?api-version=2017-11-08-preview HTTP/1.1
Host: {{iot-hub-name}}.azure-devices.net
Authorization: {{sas-token}}
Content-Type: application/json
```

The POST payload needs to be the modified version of the moduleconfig.json file found [here](https://github.com/jonbgallant/azure-iot-edge-config/blob/master/config/moduleconfig.json).

#### File Upload

The Azure IoT File Upload process is as follows:

1. Make a request to get the blob storage URI that includes the SAS Token
2. Put the file at the blob storage URI you received in the previous step
3. Call the notification URI to check the status of the upload

Here's how to upload a file:

##### Script

> Make sure you have the storage account setup as indicated above in the [prerequisites](#prerequisites).

```
python data-plane/devices/files/file-upload.py --name [iothubname] --key [iothubkey] --device-id [deviceid]
```

This script will upload a couple of sample files to prove it works.  Feel free to customize the script to suit your needs.

#### File Upload Notifications

Please reference the following article to learn how to handle the File Upload Notification event on the server-side.  This is helpful when you want to kick-off a backend process when a file has been uploaded.

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-java-java-file-upload#receive-a-file-upload-notification