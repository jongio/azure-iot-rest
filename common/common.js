const crypto = require('crypto')

module.exports = {
    getIoTHubSasToken
}

function getIoTHubSasToken (resourceUri, signingKey, policyName, expiresInMins) {
    resourceUri = encodeURIComponent(resourceUri)

    // Set expiration in seconds
    let expires = (Date.now() / 1000) + expiresInMins * 60
    expires = Math.ceil(expires)
    let toSign = resourceUri + '\n' + expires

    // Use crypto
    let hmac = crypto.createHmac('sha256', new Buffer(signingKey, 'base64'))
    hmac.update(toSign)
    let base64UriEncoded = encodeURIComponent(hmac.digest('base64'))

    // Construct autorization string
    let token = "SharedAccessSignature sr=" + resourceUri + "&sig="
    + base64UriEncoded + "&se=" + expires
    if (policyName) token += "&skn="+policyName
    return token
}
