# Admin API Documentation - Version 1.0

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


## Authentication
 
### Application Keys

All requests to any endpoint must contain a valid application key as a URL parameter. Application keys are 32 character strings created and provided by the system owner(s).

##### Request

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

User authentication is token based. A client makes a request to an authentication endpoint using valid username, password credentials and receives a time-based token. Subsequent requests should use this token for authentication instead of user credentials while the token is valid. Clients may request new tokens at any time. If an endpoint is public then it does not require an access token.

To obtain an access token, a client should send a Basic HTTP Authentication header with encoded user credentials to the token endpoint.

##### Request

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
 
| Code | Description       | Solution                                                                                                                        |
| ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 401  | Bad credentials   | Change user credentials, try again.                                                                                             | 
| 401  | Account locked    | Authentication failed too many times during attempt window - wait for the lockout period to expire, try again.                  |
| 403  | Password expired  | Request a password reset, follow the directions to reset password, try again.                                                   |
| 403  | Permission denied | The current user does not have permission to access the resource. This is most likely caused by using a non-administrator user. |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/token?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx -u admin1:admin1pass
```

###### Response

```json
{
  "expiration": 14400,
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg",
  "user_id": 1,
  "username": "admin1"
}
```

Once a token has been obtained, use the `token` in place of "username" in the Basic Auth header. Leave the password empty.

###### Following Request

```ssh
curl https://api.admin.domain.com/v/1.0/users?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

_For brevity the `Authorization` header will be ignored for the rest of the documentation, but its requirements still apply._


## User Account

### Read User Account Data

Use the following to read the account information for the currently logged in user.

##### Request

| HTTP       | Value          |
| ---------- | -------------- | 
| Methods    | GET            | 
| Path       | /user_account  |

##### Response Codes
 
| Code | Description | Solution            |
| ---- | ----------- | ------------------- |
| 200  | OK          | Request successful. |

##### Response Payload

| Key                                  | Value                                           |
| ------------------------------------ | ----------------------------------------------- | 
| `user_account`                       | The top-level user account resource.            | 
| `user_account`.`email`               | The user's email address.                       | 
| `user_account`.`first_name`          | The user's first name.                          |
| `user_account`.`id`                  | The user's system id.                           |
| `user_account`.`joined_at`           | The datetime the user joined the system.        |
| `user_account`.`last_name`           | The user's last name.                           |
| `user_account`.`password_changed_at` | The last time the user changed their password.  |
| `user_account`.`uri`                 | The API endpoint for the user's resource.       |
| `user_account`.`username`            | The user's username.                            |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/user_account?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user_account": {
    "email": "admin1@test.com", 
    "first_name": "Tommy", 
    "id": 1, 
    "joined_at": "2018-11-01T00:00:00+0000", 
    "last_name": "Lund", 
    "password_changed_at": "2019-10-28T07:55:14+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/administrator/1", 
    "username": "admin1"
  }
}
```

### Update User Account Data

Use the following to update the account information for the currently logged in user.

##### Request

| HTTP       | Value          |
| ---------- | -------------- | 
| Methods    | PUT            | 
| Path       | /user_account  |

##### Request Payload

| Key                   | Value                     | Validation                                                                                     |
| --------------------- | ------------------------- | ---------------------------------------------------------------------------------------------- | 
| `email`               | The user's email address. | Required; Unique; Valid email address format                                                   | 
| `first_name`          | The user's first name.    | Required; Length: 1-40 chars                                                                   |
| `last_name`           | The user's last name.     | Required; Length: 2-40 chars                                                                   |
| `username`            | The user's username.      | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only |

##### Response Codes
 
| Code | Description | Solution                                                                                                            |
| ---- | ----------- | ------------------------------------------------------------------------------------------------------------------- |
| 200  | OK          | Update successful.                                                                                                  |
| 400  | Bad Request | Could not complete the request due to bad client data. Fix the errors mentioned in the `errors` field and resubmit. |

##### Response Payload

| Key                                  | Value                                           |
| ------------------------------------ | ----------------------------------------------- | 
| `user_account`                       | The top-level user account resource.            | 
| `user_account`.`email`               | The user's email address.                       | 
| `user_account`.`first_name`          | The user's first name.                          |
| `user_account`.`id`                  | The user's system id.                           |
| `user_account`.`joined_at`           | The datetime the user joined the system.        |
| `user_account`.`last_name`           | The user's last name.                           |
| `user_account`.`password_changed_at` | The last time the user changed their password.  |
| `user_account`.`uri`                 | The API endpoint for the user's resource.       |
| `user_account`.`username`            | The user's username.                            |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{"email":"admin1a@test.com","first_name":"Thomas","last_name":"Luhnd","username":"admin1a"}'\
    https://api.admin.domain.com/v/1.0/user_account?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user_account": {
    "email": "admin1a@test.com", 
    "first_name": "Thomas", 
    "id": 1, 
    "joined_at": "2018-11-01T00:00:00+0000", 
    "last_name": "Luhnd", 
    "password_changed_at": "2019-10-28T07:55:14+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/administrator/1", 
    "username": "admin1a"
  }
}
```
