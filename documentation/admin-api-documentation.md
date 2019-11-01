# Admin API Documentation

The admin API uses a REST interface using JSON responses. It uses standard HTTP response codes, verbs and authentication. All endpoints should use HTTPS for security and privacy.


## Status Codes

| Code | Short Description     | Long Description                                                                                 |
| ---- | --------------------- | ------------------------------------------------------------------------------------------------ |
| 200  | OK                    | Everything worked correctly as intended.                                                         |
| 201  | Created               | A new resource was successfully created.                                                         |
| 204  | No Content            | There is no content or a resource was successfully removed.                                      |
| 400  | Bad Request           | The request cannot be completed due to client error. Fix the errors before reattempting request. |
| 401  | Unauthorized          | The request cannot be completed because it fails some authorization requirement.                 |
| 403  | Forbidden             | The request cannot be completed because the application is refusing to take an action.           |
| 404  | Not Found             | The does not exist or is currently not available.                                                |
| 405  | Method Not Allowed    | The HTTP verb (GET, POST, etc.) is not supported by the requested resource.                      |
| 500  | Internal Server Error | There was an unexpected error on the server.                                                     |


## Endpoints

As a RESTful API, resource endpoints (URLs) are one of the most important parts of the interface. While the application describes "paths" to resources, these are not the complete endpoints. The system also prepends the protocol, domain name, and version information to the path to produce the final endpoint.

##### Format

```
{PROTOCOL}://{DOMAIN_NAME}/v/{VERSION_NUMBER}{PATH}
```

##### Example

For example, if the domain is "api.admin.domain.com", the API version is "1.0" and the path is "/users", then the endpoint would be (assuming HTTPS of course):

```
https://api.admin.domain.com/v/1.0/users
```


## Authorization
 
### Application Keys

All requests to any endpoint must contain a valid application key as a URL parameter. Application keys are 32 character strings created and provided by the system owner(s).

| HTTP       | Value                                     |
| ---------- | ----------------------------------------- | 
| Methods    | *                                         | 
| Path       | *                                         |
| Parameters | `app_key`: 32 character string (required) |

##### Errors

| Code | Description             | Solution                                                                                           |
| ---- | ----------------------- | -------------------------------------------------------------------------------------------------- |
| 401  | Bad application key     | Change the `app_key` parameter to a correct key. Request a new one from system owner if necessary. | 
| 401  | Missing application key | Add the `app_key` parameter to the endpoint.                                                       | 

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/users?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx
```

_For brevity the `app_key` URL parameter will be ignored for the rest of the documentation, but its requirements still apply._

### Access Tokens

User authentication is token based. A client makes a request to an authentication endpoint using valid username, password credentials and receives a time-based token. Subsequent requests should use this token for authorization instead of user credentials while the token is valid. Clients may request new tokens at any time. If an endpoint is public then it does not require an access token.

To obtain an access token, a client should send a Basic HTTP Authentication header with encoded user credentials to the token endpoint.

| HTTP       | Value                                                         |
| ---------- | ------------------------------------------------------------- | 
| Methods    | GET                                                           | 
| Path       | /token                                                        |
| Headers    | `Authorization`: 'Basic ' + base_64_encode(username:password) |

##### Response Payload

| Key          | Value                                               |
| ------------ | --------------------------------------------------- | 
| `expiration` | Lifetime (in seconds) for the newly granted token.  | 
| `token`      | The token itself.                                   |
| `user_id`    | The system id of the user the token was granted to. |
| `username`   | The username of the user the token was granted to.  |

##### Errors

| Code | Description      | Solution                                                                                                       |
| ---- | ---------------- | -------------------------------------------------------------------------------------------------------------- |
| 401  | Bad credentials  | Change user credentials, try again.                                                                            | 
| 401  | Account locked   | Authentication failed too many times during attempt window - wait for the lockout period to expire, try again. |
| 403  | Password expired | Request a password reset, follow the directions to reset password, try again.                                  |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/token -u username:password
```

###### Response

```json
{
  "expiration": 14400,
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg",
  "user_id": 1,
  "username": "username"
}
```

Once a token has been obtained, use the `token` in place of "username" in the Basic Auth header. Leave the password empty.

###### Following Request

```ssh
curl https://api.admin.domain.com/v/1.0/users -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

_For brevity the `Authorization` header will be ignored for the rest of the documentation, but its requirements still apply._
