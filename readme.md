# Azure IoT REST

This repo contains sample code that will help you use the Azure IoT REST APIs.

## APIs

### Device Configuration

IoT Edge devices are configured with metadata such as module paths and route settings.  That configuration is applied via the `applyConfigurationContent` API.  You can read more about Edge configuration here: https://github.com/jonbgallant/azure-iot-edge-config

#### device-conf Script

This repo contains a script called `device-conf` that will assist you in creating automation scripts to apply these settings.  The script simply wraps the REST API.

Here's how to use it:

1\. Clone this repo.
2\. Navigate to `data-plane\devices`
3\. Run `pip install requests`
4\. Execute the device-conf script:

```
python device-conf.py --name [iothubname] --key [iothubkey] --device-id [deviceid] --config-file [path to module config]
```

#### REST API

You can also apply the config change via the Azure IoT REST API itself, the URI is: 

```
POST /devices/{{deviceId}}/applyConfigurationContent?api-version=2017-11-08-preview HTTP/1.1
Host: {{iot-hub-name}}.azure-devices.net
Authorization: {{sas-token}}
Content-Type: application/json
```

Payload needs to be the modified version of the moduleconfig.json file found [here](https://github.com/jonbgallant/azure-iot-edge-config/blob/master/config/moduleconfig.json).

### File Upload

#### Prerequisites
1. Azure IoT Hub
1. Azure IoT Hub Device
1. Azure Storage Account (to store the uploaded files, see [this blog post](http://blog.jongallant.com/2017/01/azure-iot-hub-file-upload-python/) for instructions on how to set this up)

The Azure IoT File Upload process is as follows:

1. Make a request to get the blob storage URI that includes the SAS Token
2. Put the file at the blob storage URI you received in the previous step
3. Call the notification URI to check the status of the upload

To run the sample:

#### Python
1. Open `data-plane/files/upload-file.py` 
1. Set your IoT Hub name, IoT Hub key and Device Id
1. Open a terminal 
1. Navigate to the root of this project
1. Execute the following to install the `requests` pip

```
pip install requests
```

1. Navigate to `data-plane/files`
1. Execute the following to upload a sample text and binary file to your blob storage

```
python .\upload-file.py
```

#### Node

1. Open `data-plane/files/upload-file.js`
1. Set your IoT Hub name, IoT Hub key and Device Id
1. Open a terminal 
1. Navigate to the root of this project
1. Execute the following to install dependencies

```
npm install
```

1. Navigate to `data-plane/files`
1. Execute the following to upload a sample text and binary file to your blob storage

```
node .\upload-file.js
```

#### File Upload Notifications

Please reference the following article to learn how to handle the File Upload Notification event on the server-side.  This is helpful when you want to kick-off a backend process when a file has been uploaded.

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-java-java-file-upload#receive-a-file-upload-notification