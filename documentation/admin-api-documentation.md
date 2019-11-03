# Admin API Documentation - Version 1.0

The admin API uses a REST interface using JSON responses. It uses standard HTTP response codes, verbs and authentication. All endpoints should use HTTPS for security and privacy.

<br><br>

## Definitions

### HTTP Status Codes

The following table describes the HTTP status codes supported by this API.

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


### Endpoints

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


### Timestamps

Timestamps should all be formatted to the ISO 8601 datetime standard: `%Y-%m-%dT%H:%M:%S%z`

##### Example

```
2018-11-01T00:00:00+0000
```


### Resource Status Codes

Most resources have a status code associated with them to determine their availability. Note that these are separate from the HTTP status codes described above for endpoints. Below is the table of available status codes.

| Code | Label    | Description                                                                                   |
| ---- | -------- | --------------------------------------------------------------------------------------------- | 
| 1    | Enabled  | Generally available to the public.                                                            |
| 2    | Disabled | Temporarily unavailable to the public.                                                        |
| 3    | Archived | Removed long-term from both the public and administrators, but not deleted.                   |
| 4    | Deleted  | Removed from both the public and administrators, flagged for eventual permanent deletion.     |
| 5    | Pending  | Currently unavailable to the public, pending some action from an administrator or the system. |

<br><br>

## Authentication
 
### Application Keys

All requests to any endpoint must contain a valid application key as a URL parameter. Application keys are 32 character strings created and provided by the system owner(s).

##### Request

| HTTP       | Value                                       |
| ---------- | ------------------------------------------- | 
| Methods    | *                                           | 
| Paths      | *                                           |
| Parameters | - `app_key`: 32 character string (required) |

##### Errors

| Code | Description             | Notes                                                                                              |
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
| Method     | GET                                                           | 
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
 
| Code | Description       | Notes                                                                                                                           |
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

<br><br>

## User Account

### Read User Account Data

Use the following to read the account information for the currently logged in user.

##### Request

| HTTP       | Value          |
| ---------- | -------------- | 
| Method     | GET            | 
| Path       | /user_account  |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 500  | Server error | Generic application error. Check application logs. |

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

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | PUT                              |
| Path       | /user_account                    |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key                   | Value                     | Validation                                                                                     |
| --------------------- | ------------------------- | ---------------------------------------------------------------------------------------------- | 
| `email`               | The user's email address. | Required; Unique; Valid email address format                                                   | 
| `first_name`          | The user's first name.    | Required; Length: 1-40 chars                                                                   |
| `last_name`           | The user's last name.     | Required; Length: 2-40 chars                                                                   |
| `username`            | The user's username.      | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only |

##### Response Codes
 
| Code | Description  | Notes                                                                                                               |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| 200  | OK           | Update successful.                                                                                                  |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `errors` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                  |

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
    -d '{
        "email": "admin1a@test.com",
        "first_name": "Thomas",
        "last_name": "Luhnd",
        "username": "admin1a"
    }' \
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

<br><br>

## User Password

### Update User Password

Use the following to update the password for the currently logged in user.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | PUT                              |
| Path       | /user_account/password           |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key                   | Value                                     | Validation                                                                                                 |
| --------------------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------- | 
| `previous_password`   | The user's current password.              | Required; Must match current password.                                                                     | 
| `password1`           | The new password.                         | Required; Length: 8-40 chars; Must have 3 out of 4: (lowercase char, uppercase char, number, special char) |
| `password2`           | The new password again, for confirmation. | Required; Must match `password1` value                                                                     |

##### Response Codes
 
| Code | Description  | Notes                                                                                                               |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| 200  | OK           | Update successful.                                                                                                  |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `errors` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                  |

##### Response Payload

| Key       | Value  |
| --------- | ------ | 
| `success` | 'true' | 

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "previous_password": "admin1pass",
        "password1": "admin1Pass2",
        "password2": "admin1Pass2"
    }' \
    https://api.admin.domain.com/v/1.0/user_account/password?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "success": "true"
}
```

<br><br>

## Application Keys

### List Application Keys

Use the following to read a list of application keys. By default the page numbering starts at 1 and the limit is 10 results per page.

##### Request

| HTTP       | Value                                                                                                                                                                               |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | 
| Method     | GET                                                                                                                                                                                 | 
| Paths      | /app_keys<br>/app_keys/{int:page}<br>/app_keys/{int:page}/{int:limit}                                                                                                               |
| Parameters | - `status`: Resource status code to filter results by (optional)<br>- `order_by`: How to order results (optional; values: [`id.asc`, `id.desc`, `application.asc`, `application.desc`]) |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no application keys on this page.        |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                              | Value                                                                      |
| -------------------------------- | -------------------------------------------------------------------------- | 
| `app_keys`                       | The top-level application key list resource.                               | 
| `app_keys`[].`application`       | List item property: The name of the application assigned to the app key.   | 
| `app_keys`[].`created_at`        | List item property: The datetime the app key was created.                  |
| `app_keys`[].`id`                | List item property: The app key's system id.                               |
| `app_keys`[].`key`               | List item property: The application key itself.                            |
| `app_keys`[].`status`            | List item property: The status of the app key.                             |
| `app_keys`[].`status_changed_at` | List item property: The datetime of the last time the status was changed.  |
| `app_keys`[].`updated_at`        | List item property: The datetime of the last time the app key was updated. |
| `limit`                          | The limit of items to show on a single page.                               |
| `next_uri`                       | The URI of the next page of results, if available.                         |
| `page`                           | The current list page number.                                              |
| `previous_uri`                   | The URI of the previous page of results, if available.                     |
| `total`                          | The total count of items found.                                            |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/app_keys/1/3?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "app_keys": [
    {
      "application": "Application 1", 
      "created_at": "2019-10-23T15:03:37+0000", 
      "id": 1, 
      "key": "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW", 
      "status": 1, 
      "status_changed_at": "2019-10-30T13:38:47+0000", 
      "updated_at": "2019-10-30T13:38:47+0000"
    }, 
    {
      "application": "Application 2", 
      "created_at": "2019-10-23T15:03:37+0000", 
      "id": 2, 
      "key": "cvBtQGgL9gNnSZk4DmKnva4QMcpTV7Mx", 
      "status": 1, 
      "status_changed_at": "2018-01-05T00:00:00+0000", 
      "updated_at": "2019-10-23T15:03:37+0000"
    }, 
    {
      "application": "Application 3", 
      "created_at": "2019-10-23T15:03:37+0000", 
      "id": 3, 
      "key": "9CR45hFpTahbqDvmZFJdENAKz5VPqLG3", 
      "status": 2, 
      "status_changed_at": "2018-01-10T00:00:00+0000", 
      "updated_at": "2019-10-30T13:18:10+0000"
    }
  ], 
  "limit": 3, 
  "next_uri": "https://api.admin.domain.com/v/1.0/app_keys/2/3", 
  "page": 1, 
  "total": 4
}
```

### Read Application Key Data

Use the following to read the information for a specific application key.

##### Request

| HTTP       | Value             |
| ---------- | ----------------- | 
| Method     | GET               | 
| Path       | /app_key/{int:id} |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 404  | Not Found    | No app key matching the supplied ID was found.     |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                           | Value                                                  |
| ----------------------------- | ------------------------------------------------------ | 
| `app_key`                     | The top-level application key resource.                | 
| `app_key`.`application`       | The name of the application assigned to the app key.   | 
| `app_key`.`created_at`        | The datetime the app key was created.                  |
| `app_key`.`id`                | The app key's system id.                               |
| `app_key`.`key`               | The application key itself.                            |
| `app_key`.`status`            | The status of the app key.                             |
| `app_key`.`status_changed_at` | The datetime of the last time the status was changed.  |
| `app_key`.`updated_at`        | The datetime of the last time the app key was updated. |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/app_key/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "app_key": {
    "application": "Application 1", 
    "created_at": "2019-10-23T15:03:37+0000", 
    "id": 1, 
    "key": "7sv3aPS45Ck8URGRKUtBdMWgKFN4ahfW", 
    "status": 1, 
    "status_changed_at": "2019-10-30T13:38:47+0000", 
    "updated_at": "2019-10-30T13:38:47+0000"
  }
}
```

### Create an Application Key

Use the following to create a new application key.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | POST                             | 
| Path       | /app_keys                        |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key           | Value                                                | Validation                          |
| ------------- | ---------------------------------------------------- | ----------------------------------- | 
| `application` | The name of the application assigned to the app key. | Required; Length: 2-200 chars       | 
| `key`         | The application key itself.                          | Required; Unique; Length: 32 chars; |
| `status`      | The status of the app key.                           | Required; Must be an integer        |

##### Response Codes
 
| Code | Description  | Notes                                                                                                               |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| 201  | Created      | Resource successfully created.                                                                                      |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `errors` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                  |

##### Response Payload

| Key                           | Value                                                  |
| ----------------------------- | ------------------------------------------------------ | 
| `app_key`                     | The top-level application key resource.                | 
| `app_key`.`application`       | The name of the application assigned to the app key.   | 
| `app_key`.`created_at`        | The datetime the app key was created.                  |
| `app_key`.`id`                | The app key's system id.                               |
| `app_key`.`key`               | The application key itself.                            |
| `app_key`.`status`            | The status of the app key.                             |
| `app_key`.`status_changed_at` | The datetime of the last time the status was changed.  |
| `app_key`.`updated_at`        | The datetime of the last time the app key was updated. |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "application": "Some Application Name",
        "key": "AHvy6Wk5kqrFzAe3HVKzxfVtqwPK3ELZ",
        "status": 1
    }' \
    https://api.admin.domain.com/v/1.0/app_keys?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "app_key": {
    "application": "Some Application Name", 
    "created_at": "2019-11-03T00:37:29+0000", 
    "id": 7, 
    "key": "AHvy6Wk5kqrFzAe3HVKzxfVtqwPK3ELZ", 
    "status": 1, 
    "status_changed_at": "2019-11-03T00:37:29+0000", 
    "updated_at": "2019-11-03T00:37:29+0000"
  }
}
```

### Update an Application Key

Use the following to update an existing application key.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | PUT                              | 
| Path       | /app_key/{int:id}                |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key           | Value                                                | Validation                          |
| ------------- | ---------------------------------------------------- | ----------------------------------- | 
| `application` | The name of the application assigned to the app key. | Required; Length: 2-200 chars       | 
| `key`         | The application key itself.                          | Required; Unique; Length: 32 chars; |
| `status`      | The status of the app key.                           | Required; Must be an integer        |

##### Response Codes
 
| Code | Description  | Notes                                                                                                               |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| 200  | OK           | Update successful.                                                                                                  |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `errors` field and resubmit. |
| 404  | Not Found    | No app key matching the supplied ID was found.                                                                      |
| 500  | Server error | Generic application error. Check application logs.                                                                  |

##### Response Payload

| Key                           | Value                                                  |
| ----------------------------- | ------------------------------------------------------ | 
| `app_key`                     | The top-level application key resource.                | 
| `app_key`.`application`       | The name of the application assigned to the app key.   | 
| `app_key`.`created_at`        | The datetime the app key was created.                  |
| `app_key`.`id`                | The app key's system id.                               |
| `app_key`.`key`               | The application key itself.                            |
| `app_key`.`status`            | The status of the app key.                             |
| `app_key`.`status_changed_at` | The datetime of the last time the status was changed.  |
| `app_key`.`updated_at`        | The datetime of the last time the app key was updated. |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "application": "Application 1 A",
        "key": "ERgZwgDUtSgN5dLxAdXdAPQJ6tCyVGQH",
        "status": 2
    }' \
    https://api.admin.domain.com/v/1.0/app_key/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "app_key": {
    "application": "Application 1 A", 
    "created_at": "2019-10-23T15:03:37+0000", 
    "id": 1, 
    "key": "ERgZwgDUtSgN5dLxAdXdAPQJ6tCyVGQH", 
    "status": 2, 
    "status_changed_at": "2019-11-03T00:55:25+0000", 
    "updated_at": "2019-11-03T00:55:25+0000"
  }
}
```

### Delete an Application Key

Use the following to permanently delete an existing application key.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | DELETE                           | 
| Path       | /app_key/{int:id}                |

##### Response Codes
 
| Code | Description  | Notes                                                                                                               |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------- |
| 204  | No Content   | Delete successful.                                                                                                  |
| 404  | Not Found    | No app key matching the supplied ID was found.                                                                      |
| 500  | Server error | Generic application error. Check application logs.                                                                  |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/app_key/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```
