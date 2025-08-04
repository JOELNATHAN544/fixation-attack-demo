#!/bin/bash

# OAuth 2.0 Flows Implementation Examples
# This script provides practical examples for testing OAuth 2.0 flows

set -e

# Configuration - Replace with your actual OAuth provider details
CLIENT_ID="your_client_id"
CLIENT_SECRET="your_client_secret"
REDIRECT_URI="http://localhost:8080/callback"
SCOPE="openid profile email"
AUTH_ENDPOINT="https://your-provider.com/oauth/authorize"
TOKEN_ENDPOINT="https://your-provider.com/oauth/token"
USERINFO_ENDPOINT="https://your-provider.com/oauth/userinfo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== OAuth 2.0 Flows Implementation Examples ===${NC}\n"

# Function to print section headers
print_section() {
    echo -e "${GREEN}=== $1 ===${NC}\n"
}

# Function to print step headers
print_step() {
    echo -e "${YELLOW}Step $1: $2${NC}"
}

# Function to make curl requests and format output
make_request() {
    local description="$1"
    local curl_command="$2"
    
    echo -e "${BLUE}$description${NC}"
    echo "Command: $curl_command"
    echo "Response:"
    
    # Execute the curl command and capture output
    local response
    response=$(eval "$curl_command" 2>/dev/null || echo "Error: Request failed")
    
    # Try to format JSON if possible
    if command -v jq >/dev/null 2>&1; then
        echo "$response" | jq '.' 2>/dev/null || echo "$response"
    else
        echo "$response"
    fi
    echo -e "\n"
}

# Flow 1: Authorization Code Flow
print_section "Flow 1: Authorization Code Flow"

print_step "1" "Generate Authorization URL"
AUTH_URL="${AUTH_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}&state=random_state_string"
echo "Authorization URL: ${AUTH_URL}"
echo "Please open this URL in your browser, complete the authorization, and copy the authorization code from the redirect URL."
echo -e "\n"

print_step "2" "Exchange Authorization Code for Access Token"
echo "Replace AUTHORIZATION_CODE with the code you received:"
echo "curl -X POST \"${TOKEN_ENDPOINT}\" \\"
echo "  -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "  -d \"grant_type=authorization_code\" \\"
echo "  -d \"client_id=${CLIENT_ID}\" \\"
echo "  -d \"client_secret=${CLIENT_SECRET}\" \\"
echo "  -d \"code=AUTHORIZATION_CODE\" \\"
echo "  -d \"redirect_uri=${REDIRECT_URI}\""
echo -e "\n"

print_step "3" "Use Access Token"
echo "Replace ACCESS_TOKEN with the token you received:"
echo "curl -H \"Authorization: Bearer ACCESS_TOKEN\" \\"
echo "  \"${USERINFO_ENDPOINT}\""
echo -e "\n"

# Flow 2: Authorization Code Flow with PKCE
print_section "Flow 2: Authorization Code Flow with PKCE"

print_step "1" "Generate Code Verifier and Challenge"
echo "Generating PKCE parameters..."
CODE_VERIFIER=$(openssl rand -base64 32 | tr -d "=+/" | tr '[:upper:]' '[:lower:]')
CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -binary -sha256 | openssl base64 -A | tr -d "=+/" | tr '[:upper:]' '[:lower:]')

echo "Code Verifier: ${CODE_VERIFIER}"
echo "Code Challenge: ${CODE_CHALLENGE}"
echo -e "\n"

print_step "2" "Generate Authorization URL with PKCE"
AUTH_URL_PKCE="${AUTH_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}&state=random_state_string&code_challenge=${CODE_CHALLENGE}&code_challenge_method=S256"
echo "Authorization URL with PKCE: ${AUTH_URL_PKCE}"
echo "Please open this URL in your browser, complete the authorization, and copy the authorization code."
echo -e "\n"

print_step "3" "Exchange Code for Access Token with PKCE"
echo "Replace AUTHORIZATION_CODE with the code you received:"
echo "curl -X POST \"${TOKEN_ENDPOINT}\" \\"
echo "  -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "  -d \"grant_type=authorization_code\" \\"
echo "  -d \"client_id=${CLIENT_ID}\" \\"
echo "  -d \"code=AUTHORIZATION_CODE\" \\"
echo "  -d \"redirect_uri=${REDIRECT_URI}\" \\"
echo "  -d \"code_verifier=${CODE_VERIFIER}\""
echo -e "\n"

# Flow 3: Client Credentials Flow
print_section "Flow 3: Client Credentials Flow"

print_step "1" "Request Access Token"
echo "Requesting access token using client credentials..."
make_request "Client Credentials Token Request" \
    "curl -X POST \"${TOKEN_ENDPOINT}\" \
    -H \"Content-Type: application/x-www-form-urlencoded\" \
    -d \"grant_type=client_credentials\" \
    -d \"client_id=${CLIENT_ID}\" \
    -d \"client_secret=${CLIENT_SECRET}\" \
    -d \"scope=${SCOPE}\""

print_step "2" "Use Access Token"
echo "Replace ACCESS_TOKEN with the token you received:"
echo "curl -H \"Authorization: Bearer ACCESS_TOKEN\" \\"
echo "  \"${USERINFO_ENDPOINT}\""
echo -e "\n"

# Flow 4: Resource Owner Password Credentials Flow
print_section "Flow 4: Resource Owner Password Credentials Flow"

print_step "1" "Request Access Token with Username/Password"
echo "Replace USERNAME and PASSWORD with actual credentials:"
echo "curl -X POST \"${TOKEN_ENDPOINT}\" \\"
echo "  -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "  -d \"grant_type=password\" \\"
echo "  -d \"client_id=${CLIENT_ID}\" \\"
echo "  -d \"client_secret=${CLIENT_SECRET}\" \\"
echo "  -d \"username=USERNAME\" \\"
echo "  -d \"password=PASSWORD\" \\"
echo "  -d \"scope=${SCOPE}\""
echo -e "\n"

print_step "2" "Use Access Token"
echo "Replace ACCESS_TOKEN with the token you received:"
echo "curl -H \"Authorization: Bearer ACCESS_TOKEN\" \\"
echo "  \"${USERINFO_ENDPOINT}\""
echo -e "\n"

# Flow 5: Device Authorization Flow (Bonus)
print_section "Flow 5: Device Authorization Flow (Bonus)"

print_step "1" "Request Device Authorization"
echo "Requesting device authorization..."
DEVICE_ENDPOINT="${TOKEN_ENDPOINT%/*}/device"
make_request "Device Authorization Request" \
    "curl -X POST \"${DEVICE_ENDPOINT}\" \
    -H \"Content-Type: application/x-www-form-urlencoded\" \
    -d \"client_id=${CLIENT_ID}\" \
    -d \"scope=${SCOPE}\""

print_step "2" "Poll for Token"
echo "Replace DEVICE_CODE with the device code from the response:"
echo "while true; do"
echo "  RESPONSE=\$(curl -s -X POST \"${TOKEN_ENDPOINT}\" \\"
echo "    -H \"Content-Type: application/x-www-form-urlencoded\" \\"
echo "    -d \"grant_type=urn:ietf:params:oauth:grant-type:device_code\" \\"
echo "    -d \"client_id=${CLIENT_ID}\" \\"
echo "    -d \"device_code=DEVICE_CODE\")"
echo "  "
echo "  if echo \"\$RESPONSE\" | grep -q \"access_token\"; then"
echo "    echo \"Access token received:\""
echo "    echo \"\$RESPONSE\" | jq '.'"
echo "    break"
echo "  fi"
echo "  "
echo "  echo \"Waiting for authorization...\""
echo "  sleep 5"
echo "done"
echo -e "\n"

# Summary
print_section "Summary and Next Steps"

echo "To complete this project:"
echo "1. Replace the placeholder values with your actual OAuth provider details"
echo "2. Test at least 3 flows successfully"
echo "3. Document your findings and responses"
echo "4. Create automation scripts if desired"
echo "5. Understand the security implications of each flow"
echo -e "\n"

echo -e "${GREEN}=== OAuth 2.0 Flows Implementation Complete ===${NC}" 