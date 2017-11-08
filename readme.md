# Azure IoT REST

This repo contains sample code that will help you use the Azure IoT REST APIs.

## APIs

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