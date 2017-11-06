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

1. Open either `data-plane/files/upload-file.js` or `data-plane/files/upload-file.py` 
2. Set your IoT Hub name, IoT Hub key and Device Id
3. Open a terminal 
4. Navigate to `data-plane/files`
5. Execute one of the following:

```
node .\upload-file.js
```

```
python .\upload-file.py
```
