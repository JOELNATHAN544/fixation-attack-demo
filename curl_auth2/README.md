# OAuth 2.0 Flows Implementation with Curl

This project demonstrates how to implement various OAuth 2.0 flows manually using `curl` commands, providing a practical understanding of OAuth 2.0 authentication mechanisms.

## Project Overview

The goal is to gain hands-on experience with OAuth 2.0 flows by implementing them step-by-step using `curl` commands, without relying on SDKs or libraries.

## Files in this Project

- `guideline.txt` - Project requirements and objectives
- `oauth2-flows.md` - Comprehensive implementation guide with step-by-step instructions
- `oauth2-examples.sh` - Practical examples and test scripts
- `README.md` - This file with project documentation

## OAuth 2.0 Flows Covered

### 1. Authorization Code Flow
- Most secure flow for web applications
- Involves browser-based authorization
- Exchanges authorization code for access token

### 2. Authorization Code Flow with PKCE
- Enhanced security for public clients
- Uses code verifier and challenge mechanism
- Suitable for mobile apps and SPAs

### 3. Client Credentials Flow
- Server-to-server communication
- Uses client credentials directly
- No user interaction required

### 4. Resource Owner Password Credentials (ROPC) Flow
- Direct username/password authentication
- **Not recommended for production use**
- Included for educational purposes

### 5. Device Authorization Flow (Bonus)
- For devices with limited input capabilities
- Uses device codes and polling mechanism

## Getting Started

### Prerequisites

1. **Install curl**: Ensure `curl` is installed on your system
   ```bash
   # Ubuntu/Debian
   sudo apt-get install curl
   
   # macOS
   brew install curl
   
   # Windows (with WSL or Git Bash)
   # curl is usually pre-installed
   ```

2. **Choose an OAuth Provider**: You'll need access to an OAuth 2.0 provider:
   - **Auth0** (free tier available)
   - **Keycloak** (self-hosted)
   - **OIDC Debugger** (for testing)
   - **Your own OAuth server**

3. **Get Client Credentials**: Register an application with your chosen provider to get:
   - Client ID
   - Client Secret
   - Authorization endpoint
   - Token endpoint

### Quick Start

1. **Read the implementation guide**:
   ```bash
   cat oauth2-flows.md
   ```

2. **Run the examples script**:
   ```bash
   ./oauth2-examples.sh
   ```

3. **Follow the step-by-step instructions** in `oauth2-flows.md`

## Implementation Steps

### For Each Flow:

1. **Understand the flow**: Read the explanation in `oauth2-flows.md`
2. **Set up your environment**: Configure your OAuth provider details
3. **Execute the commands**: Follow the curl examples
4. **Document your results**: Record responses and status codes
5. **Test the flow**: Verify you can access protected resources

### Example: Authorization Code Flow

```bash
# Step 1: Generate authorization URL
CLIENT_ID="your_client_id"
REDIRECT_URI="http://localhost:8080/callback"
AUTH_ENDPOINT="https://your-provider.com/oauth/authorize"

AUTH_URL="${AUTH_ENDPOINT}?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=openid profile"

# Step 2: Open URL in browser and complete authorization
# Step 3: Exchange code for token
curl -X POST "https://your-provider.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=your_client_secret" \
  -d "code=authorization_code_from_browser" \
  -d "redirect_uri=${REDIRECT_URI}"
```

## Expected Deliverables

As per the project requirements, you should submit:

1. **Documentation**: A markdown file (`oauth2-flows.md`) containing:
   - Step-by-step curl commands for each flow
   - Actual responses (JSON, tokens, status codes)
   - Brief explanations of what happened at each step

2. **Optional**: A shell script that automates one or more flows

## Success Criteria

- ✅ Proper understanding of when and how each flow is used
- ✅ Successful reproduction of at least 3 flows
- ✅ Ability to explain the security model behind each flow

## Security Considerations

### Authorization Code Flow
- **Use case**: Web applications with server-side code
- **Security**: High - authorization code is short-lived
- **Best practice**: Always use HTTPS

### PKCE Flow
- **Use case**: Public clients (mobile apps, SPAs)
- **Security**: High - prevents authorization code interception
- **Best practice**: Use strong code verifiers

### Client Credentials Flow
- **Use case**: Server-to-server communication
- **Security**: Medium - credentials must be kept secure
- **Best practice**: Store secrets securely

### ROPC Flow
- **Use case**: Legacy applications
- **Security**: Low - requires username/password
- **Best practice**: Avoid in production

## Troubleshooting

### Common Issues

1. **Invalid redirect URI**
   - Ensure the redirect URI matches exactly what's registered
   - Check for trailing slashes and protocol (http vs https)

2. **Expired authorization code**
   - Authorization codes typically expire in 10 minutes
   - Request a new authorization code

3. **Invalid client credentials**
   - Verify client_id and client_secret
   - Check if credentials are URL-encoded properly

4. **CORS issues**
   - Use appropriate headers for cross-origin requests
   - Consider using a proxy for testing

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid parameters
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error

## Testing Providers

### Free OAuth Providers for Testing

1. **Auth0** (https://auth0.com)
   - Free tier available
   - Comprehensive documentation
   - Easy setup

2. **OIDC Debugger** (https://oidcdebugger.com)
   - No registration required
   - Perfect for testing
   - Immediate results

3. **Keycloak** (https://www.keycloak.org/)
   - Self-hosted option
   - Full control over configuration
   - Docker setup available

## Next Steps

After completing this project:

1. **Deepen your understanding**: Read OAuth 2.0 RFC specifications
2. **Explore advanced topics**: JWT tokens, refresh tokens, scopes
3. **Practice with real applications**: Integrate with actual APIs
4. **Learn about OIDC**: OpenID Connect builds on OAuth 2.0
5. **Security best practices**: Understand common vulnerabilities

## Resources

- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [OAuth 2.0 Security Best Practices](https://tools.ietf.org/html/draft-ietf-oauth-security-topics)
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)
- [OAuth 2.0 Playground](https://oauth2.thephpleague.com/)

## License

This project is for educational purposes. Feel free to use and modify as needed. 