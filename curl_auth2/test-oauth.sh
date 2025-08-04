#!/bin/bash

# Simple OAuth 2.0 Test Script
# This script helps you test OAuth 2.0 flows with minimal setup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== OAuth 2.0 Quick Test Script ===${NC}\n"

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is not installed. Please install curl first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ curl is installed${NC}\n"

# Test basic HTTP request
echo -e "${YELLOW}Testing basic HTTP connectivity...${NC}"
if curl -s --max-time 10 https://httpbin.org/get > /dev/null; then
    echo -e "${GREEN}✓ Internet connectivity is working${NC}"
else
    echo -e "${RED}✗ Internet connectivity issues detected${NC}"
fi

echo -e "\n${BLUE}=== OAuth 2.0 Provider Options ===${NC}"
echo "1. OIDC Debugger (https://oidcdebugger.com) - No setup required"
echo "2. Auth0 (https://auth0.com) - Free tier available"
echo "3. Keycloak (https://www.keycloak.org/) - Self-hosted"
echo "4. Custom OAuth server"

echo -e "\n${YELLOW}Recommended for quick testing:${NC}"
echo "Use OIDC Debugger (option 1) for immediate testing without registration."

echo -e "\n${BLUE}=== Next Steps ===${NC}"
echo "1. Choose an OAuth provider from the options above"
echo "2. Get your client credentials (client_id, client_secret)"
echo "3. Update the configuration in oauth2-examples.sh"
echo "4. Run: ./oauth2-examples.sh"
echo "5. Follow the step-by-step instructions in oauth2-flows.md"

echo -e "\n${GREEN}=== Configuration Template ===${NC}"
echo "Update these variables in oauth2-examples.sh:"
echo "CLIENT_ID=\"your_client_id\""
echo "CLIENT_SECRET=\"your_client_secret\""
echo "AUTH_ENDPOINT=\"https://your-provider.com/oauth/authorize\""
echo "TOKEN_ENDPOINT=\"https://your-provider.com/oauth/token\""

echo -e "\n${YELLOW}Ready to start testing OAuth 2.0 flows!${NC}" 