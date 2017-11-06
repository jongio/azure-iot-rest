const common = require('../../common/common.js')
const util = require('util')
const request = require('request')
const uuidv1 = require('uuid/v1')
const fs = require('fs')

let resourceName = ''  // IoT Hub name
let resourceKey = '' // IoT Hub primary key
let deviceId = 'device11' // IoT Hub device id
let resourceURI = resourceName + '.azure-devices.net'
let tokenExpirationPeriod = 60
let policyKeyName = 'iothubowner'
let apiVersion = '2016-02-03'

let iotHubSasToken = common.getIoTHubSasToken(resourceURI, resourceKey, policyKeyName, tokenExpirationPeriod)
let fileUploadRequestURI = util.format('https://%s/devices/%s/files?api-version=%s', resourceURI, deviceId, apiVersion).toString()
let fileUploadURITemplate = 'https://%s/%s/%s%s'
let notificationURI = util.format('https://%s/devices/%s/files/notifications?api-version=%s', resourceURI, deviceId, apiVersion).toString()

let uploadFile = function (options) {
    // 1. GET FILE STORAGE URI
    request.post(
        {
            url: fileUploadRequestURI,
            body: JSON.stringify({ 'blobName': options.fileName }),
            headers: {
                'Authorization': iotHubSasToken,
                'Content-Type': 'application/json'
            }
        },
        function (error, response, body) {

            console.log(fileUploadRequestURI)
            console.log(response.statusCode)
            console.log(body)

            if (!error && response.statusCode == 200) {

                var fileParts = JSON.parse(body)

                let fileStorageURI = util.format(fileUploadURITemplate,
                    fileParts.hostName,
                    fileParts.containerName,
                    fileParts.blobName,
                    fileParts.sasToken)

                console.log(fileStorageURI)

                // 2. UPLOAD FILE TO BLOB STORAGE

                request.put(
                    {
                        url: fileStorageURI,
                        body: options.body,
                        headers: {
                            'Content-Type': options.contentType,
                            'Content-Length': options.contentLength,
                            'x-ms-blob-type': 'BlockBlob',
                        }
                    },
                    function (error, response, body) {

                        console.log(fileStorageURI)
                        console.log(response.statusCode)
                        console.log(body)

                        if (!error && response.statusCode == 201) {

                            // 3. GET UPLOAD FILE NOTIFICATION
                            request.post(
                                {
                                    url: notificationURI,
                                    body: JSON.stringify({ 'correlationId': fileParts.correlationId }),
                                    headers: {
                                        'Authorization': iotHubSasToken,
                                        'Content-Type': 'application/json'
                                    }
                                },
                                function (error, response, body) {

                                    console.log(notificationURI)
                                    console.log(response.statusCode)
                                    console.log(body)

                                    if (!error && response.statusCode == 204) {
                                        console.log('File successfully uploaded')
                                    } else {
                                        console.log(error)
                                        console.log(response)
                                    }
                                }
                            )
                        } else {
                            console.log(error)
                            console.log(response)
                        }
                    }
                )
            } else {
                console.log(error)
                console.log(response)
            }
        }
    )


}

let bodyText = JSON.stringify({ "device": "device1", "temp": 42 })
uploadFile({
    body: bodyText,
    fileName: uuidv1() + '.json',
    contentType: 'application/json', contentLength: bodyText.length
})

let binaryFile = "iot.png"
uploadFile({
    body: fs.createReadStream(binaryFile),
    fileName: uuidv1() + '.png',
    contentType: 'image/png', contentLength: fs.statSync(binaryFile).size
})