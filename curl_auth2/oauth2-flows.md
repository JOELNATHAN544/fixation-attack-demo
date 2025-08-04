# OAuth 2.0 Flows Implementation with Curl

This document provides step-by-step instructions for implementing various OAuth 2.0 flows using `curl` commands.

## Prerequisites

Before starting, ensure you have:
- `curl` installed on your system
- Access to an OAuth 2.0 provider (we'll use examples with common providers)
- Basic understanding of HTTP requests and responses

## Flow 1: Authorization Code Flow

The Authorization Code flow is the most secure OAuth 2.0 flow for web applications.

### Step 1: Generate Authorization URL

```bash
# Replace with your actual OAuth provider details
CLIENT_ID="your_client_id"
REDIRECT_URI="http://localhost:8080/callback"
SCOPE="openid profile email"
AUTH_ENDPOINT="https://your-provider.com/oauth/authorize"

# Generate authorization URL
AUTH_URL="${AUTH_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}&state=random_state_string"

echo "Authorization URL: ${AUTH_URL}"
```

### Step 2: Manual Authorization
1. Open the authorization URL in your browser
2. Log in with your credentials
3. Authorize the application
4. Copy the authorization code from the redirect URL

### Step 3: Exchange Code for Access Token

```bash
# Replace with actual values from your provider
AUTHORIZATION_CODE="code_from_redirect_url"
CLIENT_SECRET="your_client_secret"
TOKEN_ENDPOINT="https://your-provider.com/oauth/token"

curl -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "code=${AUTHORIZATION_CODE}" \
  -d "redirect_uri=${REDIRECT_URI}"
```

### Expected Response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200...",
  "scope": "openid profile email"
}
```

### Step 4: Use Access Token

```bash
ACCESS_TOKEN="your_access_token"
PROTECTED_RESOURCE="https://your-provider.com/api/userinfo"

curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  "${PROTECTED_RESOURCE}"
```

## Flow 2: Authorization Code Flow with PKCE

PKCE (Proof Key for Code Exchange) adds security for public clients.

### Step 1: Generate Code Verifier and Challenge

```bash
# Generate a random code verifier (base64url encoded)
CODE_VERIFIER=$(openssl rand -base64 32 | tr -d "=+/" | tr '[:upper:]' '[:lower:]')

# Generate code challenge (SHA256 hash of verifier, base64url encoded)
CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -binary -sha256 | openssl base64 -A | tr -d "=+/" | tr '[:upper:]' '[:lower:]')

echo "Code Verifier: ${CODE_VERIFIER}"
echo "Code Challenge: ${CODE_CHALLENGE}"
```

### Step 2: Generate Authorization URL with PKCE

```bash
AUTH_URL="${AUTH_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}&state=random_state_string&code_challenge=${CODE_CHALLENGE}&code_challenge_method=S256"

echo "Authorization URL with PKCE: ${AUTH_URL}"
```

### Step 3: Manual Authorization
1. Open the authorization URL in your browser
2. Log in and authorize
3. Copy the authorization code

### Step 4: Exchange Code for Access Token with PKCE

```bash
curl -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=${CLIENT_ID}" \
  -d "code=${AUTHORIZATION_CODE}" \
  -d "redirect_uri=${REDIRECT_URI}" \
  -d "code_verifier=${CODE_VERIFIER}"
```

## Flow 3: Client Credentials Flow

Used for server-to-server communication where the client acts on its own behalf.

### Step 1: Request Access Token

```bash
curl -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "scope=${SCOPE}"
```

### Expected Response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "openid profile email"
}
```

### Step 2: Use Access Token

```bash
curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  "${PROTECTED_RESOURCE}"
```

## Flow 4: Resource Owner Password Credentials (ROPC) Flow

**Note: This flow is not recommended for production use due to security concerns.**

### Step 1: Request Access Token with Username/Password

```bash
USERNAME="your_username"
PASSWORD="your_password"

curl -X POST "${TOKEN_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "username=${USERNAME}" \
  -d "password=${PASSWORD}" \
  -d "scope=${SCOPE}"
```

### Expected Response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "def50200...",
  "scope": "openid profile email"
}
```

### Step 2: Use Access Token

```bash
curl -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  "${PROTECTED_RESOURCE}"
```

## Flow 5: Device Authorization Flow (Bonus)

Used for devices with limited input capabilities.

### Step 1: Request Device Authorization

```bash
DEVICE_ENDPOINT="https://your-provider.com/oauth/device"

curl -X POST "${DEVICE_ENDPOINT}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=${CLIENT_ID}" \
  -d "scope=${SCOPE}"
```

### Expected Response:
```json
{
  "device_code": "GMMYHCGVY7Q",
  "user_code": "WDJB-MJHT",
  "verification_uri": "https://your-provider.com/device",
  "verification_uri_complete": "https://your-provider.com/device?user_code=WDJB-MJHT",
  "expires_in": 1800,
  "interval": 5
}
```

### Step 2: Display User Instructions

```bash
echo "Please visit: ${VERIFICATION_URI}"
echo "Enter code: ${USER_CODE}"
```

### Step 3: Poll for Token

```bash
DEVICE_CODE="device_code_from_response"
INTERVAL="5"

while true; do
  RESPONSE=$(curl -s -X POST "${TOKEN_ENDPOINT}" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "grant_type=urn:ietf:params:oauth:grant-type:device_code" \
    -d "client_id=${CLIENT_ID}" \
    -d "device_code=${DEVICE_CODE}")
  
  if echo "$RESPONSE" | grep -q "access_token"; then
    echo "Access token received:"
    echo "$RESPONSE" | jq '.'
    break
  fi
  
  echo "Waiting for authorization..."
  sleep $INTERVAL
done
```

## Testing with Mock OAuth Provider

For testing purposes, you can use:

1. **OIDC Debugger**: https://oidcdebugger.com
2. **Auth0**: Create a free account and application
3. **Keycloak**: Set up a local instance
4. **Mock OAuth Server**: Use tools like `oauth2-mock-server`

## Security Considerations

1. **Authorization Code Flow**: Most secure for web applications
2. **PKCE**: Essential for public clients (mobile apps, SPAs)
3. **Client Credentials**: For server-to-server communication
4. **ROPC**: Avoid in production - requires username/password
5. **Device Flow**: For devices with limited input

## Common HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

## Troubleshooting

1. **Invalid redirect URI**: Ensure it matches exactly what's registered
2. **Expired authorization code**: Codes typically expire in 10 minutes
3. **Invalid client credentials**: Check client_id and client_secret
4. **CORS issues**: Use appropriate headers for cross-origin requests
5. **Token expiration**: Use refresh tokens to get new access tokens

## Next Steps

1. Implement at least 3 flows successfully
2. Document your findings and responses
3. Create automation scripts if desired
4. Understand the security implications of each flow 