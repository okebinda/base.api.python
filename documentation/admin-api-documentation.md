# Admin API Documentation - Version 1.0

The admin API uses a REST interface using JSON responses. It uses standard HTTP response codes, verbs and authentication. All endpoints should use HTTPS for security and privacy.

<br><br>

## Table of Contents

* [Definitions](#definitions)
* [Authentication](#authentication)

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
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

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
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

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

Use the following to read a list of application keys.

##### Request

| HTTP            | Value                                                                                                                                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                       |
| Paths           | /app_keys<br>/app_keys/{page}<br>/app_keys/{page}/{limit}                                                                                                                                                                 |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                 |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'application.asc', 'application.desc']; Default: 'id.asc' |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no application keys on this page.        |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                              | Value                                                  |
| -------------------------------- | ------------------------------------------------------ | 
| `app_keys`                       | The top-level application key list resource.           | 
| `app_keys`[].`application`       | The name of the application assigned to the app key.   | 
| `app_keys`[].`created_at`        | The datetime the app key was created.                  |
| `app_keys`[].`id`                | The app key's system id.                               |
| `app_keys`[].`key`               | The application key itself.                            |
| `app_keys`[].`status`            | The status of the app key.                             |
| `app_keys`[].`status_changed_at` | The datetime of the last time the status was changed.  |
| `app_keys`[].`updated_at`        | The datetime of the last time the app key was updated. |
| `limit`                          | The limit of items to show on a single page.           |
| `next_uri`                       | The URI of the next page of results, if available.     |
| `page`                           | The current list page number.                          |
| `previous_uri`                   | The URI of the previous page of results, if available. |
| `total`                          | The total count of items found.                        |

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

### Read an Application Key

Use the following to read the information for a specific application key.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | GET                                             | 
| Path            | /app_key/{id}                                   |
| Path Parameters | - `id`: Integer; The system ID for the resource |

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
| `status`      | The status of the app key.                           | Required; Integer                   |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

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

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /app_key/{id}                                   |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key           | Value                                                | Validation                          |
| ------------- | ---------------------------------------------------- | ----------------------------------- | 
| `application` | The name of the application assigned to the app key. | Required; Length: 2-200 chars       | 
| `key`         | The application key itself.                          | Required; Unique; Length: 32 chars; |
| `status`      | The status of the app key.                           | Required; Integer                   |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No app key matching the supplied ID was found.                                                                     |
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

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /app_key/{id}                                   |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 204  | No Content   | Delete successful.                                 |
| 404  | Not Found    | No app key matching the supplied ID was found.     |
| 500  | Server error | Generic application error. Check application logs. |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/app_key/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## User Roles

### List User Roles

Use the following to read a list of user roles.

##### Request

| HTTP            | Value                                                                                                                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                         |
| Paths           | /roles<br>/roles/{page}<br>/roles/{page}/{limit}<br>/roles/{type}<br>/roles/{type}/{page}                                                                                                                   |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10<br>- `type`: String; The type of role to filter by (values: ['admin', 'user'])    |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'name.asc', 'name.desc']; Default: 'id.asc' |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no roles on this page.                   |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                | Value                                                                                                             |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- | 
| `roles`                            | The top-level role list resource.                                                                                 |  
| `roles`[].`created_at`             | The datetime the role was created.                                                                                |
| `roles`[].`id`                     | The role's system id.                                                                                             |
| `roles`[].`is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    |
| `roles`[].`login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            |
| `roles`[].`login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              |
| `roles`[].`login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              |
| `roles`[].`login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 |
| `roles`[].`login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   |
| `roles`[].`name`                   | The name of the role.                                                                                             |
| `roles`[].`password_policy`        | 'true' if the password policy is enabled.                                                                         |
| `roles`[].`password_reset_days`    | Number of days a password is valid until user must change it.                                                     |
| `roles`[].`password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            |
| `roles`[].`priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. |
| `roles`[].`updated_at`             | The datetime of the last time the app key was updated.                                                            |
| `limit`                            | The limit of items to show on a single page.                                                                      |
| `next_uri`                         | The URI of the next page of results, if available.                                                                |
| `page`                             | The current list page number.                                                                                     |
| `previous_uri`                     | The URI of the previous page of results, if available.                                                            |
| `total`                            | The total count of items found.                                                                                   |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/roles?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 10, 
  "page": 1, 
  "roles": [
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "is_admin_role": false, 
      "login_ban_by_ip": true, 
      "login_ban_time": 1800, 
      "login_lockout_policy": false, 
      "login_max_attempts": 10, 
      "login_timeframe": 600, 
      "name": "USER", 
      "password_policy": false, 
      "password_reset_days": 365, 
      "password_reuse_history": 10, 
      "priority": 100, 
      "updated_at": "2019-11-05T02:16:56+0000"
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "is_admin_role": true, 
      "login_ban_by_ip": true, 
      "login_ban_time": 1800, 
      "login_lockout_policy": true, 
      "login_max_attempts": 5, 
      "login_timeframe": 300, 
      "name": "SUPER_ADMIN", 
      "password_policy": true, 
      "password_reset_days": 90, 
      "password_reuse_history": 24, 
      "priority": 10, 
      "updated_at": "2019-11-05T02:16:56+0000"
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 3, 
      "is_admin_role": false, 
      "login_ban_by_ip": true, 
      "login_ban_time": 1800, 
      "login_lockout_policy": true, 
      "login_max_attempts": 5, 
      "login_timeframe": 300, 
      "name": "SERVICE", 
      "password_policy": true, 
      "password_reset_days": 365, 
      "password_reuse_history": 24, 
      "priority": 50, 
      "updated_at": "2019-11-05T02:16:56+0000"
    }
  ], 
  "total": 3
}
```

### Read a User Role

Use the following to read the information for a specific role.

##### Request

| HTTP            | Value                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------- | 
| Method          | GET                                                                                           | 
| Path            | /role/{id}<br>/role/{name}                                                                    |
| Path Parameters | - `id`: Integer; The system ID for the resource<br>- `name`: String; The name of the resource |

##### Response Codes
 
| Code | Description  | Notes                                               |
| ---- | ------------ | --------------------------------------------------- |
| 200  | OK           | Request successful.                                 |
| 404  | Not Found    | No role matching the supplied ID or name was found. |
| 500  | Server error | Generic application error. Check application logs.  |

##### Response Payload

| Key                             | Value                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | 
| `role`                          | The top-level role resource.                                                                                      | 
| `role`.`created_at`             | The datetime the role was created.                                                                                |
| `role`.`id`                     | The role's system id.                                                                                             |
| `role`.`is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    |
| `role`.`login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            |
| `role`.`login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              |
| `role`.`login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              |
| `role`.`login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 |
| `role`.`login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   |
| `role`.`name`                   | The name of the role.                                                                                             |
| `role`.`password_policy`        | 'true' if the password policy is enabled.                                                                         |
| `role`.`password_reset_days`    | Number of days a password is valid until user must change it.                                                     |
| `role`.`password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            |
| `role`.`priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. |
| `role`.`updated_at`             | The datetime of the last time the app key was updated.                                                            |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/role/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "role": {
    "created_at": "2019-11-05T02:16:56+0000", 
    "id": 1, 
    "is_admin_role": false, 
    "login_ban_by_ip": true, 
    "login_ban_time": 1800, 
    "login_lockout_policy": false, 
    "login_max_attempts": 10, 
    "login_timeframe": 600, 
    "name": "USER", 
    "password_policy": false, 
    "password_reset_days": 365, 
    "password_reuse_history": 10, 
    "priority": 100, 
    "updated_at": "2019-11-05T02:16:56+0000"
  }
}
```

### Create a User Role

Use the following to create a new role.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | POST                             | 
| Path       | /roles                           |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key                      | Value                                                                                                             | Validation                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    | Required; Boolean                    |
| `login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            | Required; Boolean                    |
| `login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              | Required; Integer                    |
| `login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              | Required; Boolean                    |
| `login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 | Required; Integer                    |
| `login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   | Required; Integer                    |
| `name`                   | The name of the role.                                                                                             | Required; Unique; Length: 2-32 chars |
| `password_policy`        | 'true' if the password policy is enabled.                                                                         | Required; Boolean                    |
| `password_reset_days`    | Number of days a password is valid until user must change it.                                                     | Required; Integer                    |
| `password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            | Required; Integer                    |
| `priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. | Required; Integer                    |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                             | Value                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | 
| `role`                          | The top-level role resource.                                                                                      | 
| `role`.`created_at`             | The datetime the role was created.                                                                                |
| `role`.`id`                     | The role's system id.                                                                                             |
| `role`.`is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    |
| `role`.`login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            |
| `role`.`login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              |
| `role`.`login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              |
| `role`.`login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 |
| `role`.`login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   |
| `role`.`name`                   | The name of the role.                                                                                             |
| `role`.`password_policy`        | 'true' if the password policy is enabled.                                                                         |
| `role`.`password_reset_days`    | Number of days a password is valid until user must change it.                                                     |
| `role`.`password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            |
| `role`.`priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. |
| `role`.`updated_at`             | The datetime of the last time the app key was updated.                                                            |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "is_admin_role": false,
        "login_ban_by_ip": true,
        "login_ban_time": 3600,
        "login_lockout_policy": true,
        "login_max_attempts": 10,
        "login_timeframe": 900,
        "name": "TEST_ROLE",
        "password_policy": true,
        "password_reset_days": 180,
        "password_reuse_history": 10,
        "priority": 200
    }' \
    https://api.admin.domain.com/v/1.0/roles?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "role": {
    "created_at": "2019-11-05T03:14:39+0000", 
    "id": 4, 
    "is_admin_role": false, 
    "login_ban_by_ip": true, 
    "login_ban_time": 3600, 
    "login_lockout_policy": true, 
    "login_max_attempts": 10, 
    "login_timeframe": 900, 
    "name": "TEST_ROLE", 
    "password_policy": true, 
    "password_reset_days": 180, 
    "password_reuse_history": 10, 
    "priority": 200, 
    "updated_at": "2019-11-05T03:14:39+0000"
  }
}
```

### Update a User Role

Use the following to update an existing role.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /role/{id}                                      |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key                      | Value                                                                                                             | Validation                           |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    | Required; Boolean                    |
| `login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            | Required; Boolean                    |
| `login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              | Required; Integer                    |
| `login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              | Required; Boolean                    |
| `login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 | Required; Integer                    |
| `login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   | Required; Integer                    |
| `name`                   | The name of the role.                                                                                             | Required; Unique; Length: 2-32 chars |
| `password_policy`        | 'true' if the password policy is enabled.                                                                         | Required; Boolean                    |
| `password_reset_days`    | Number of days a password is valid until user must change it.                                                     | Required; Integer                    |
| `password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            | Required; Integer                    |
| `priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. | Required; Integer                    |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No role matching the supplied ID was found.                                                                        |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                             | Value                                                                                                             |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- | 
| `role`                          | The top-level role resource.                                                                                      | 
| `role`.`created_at`             | The datetime the role was created.                                                                                |
| `role`.`id`                     | The role's system id.                                                                                             |
| `role`.`is_admin_role`          | 'true' if role is applicable to admin users, 'false' if role is applicable to non-admin users.                    |
| `role`.`login_ban_by_ip`        | 'true' if lockout policy uses client IP to ban further login attempts.                                            |
| `role`.`login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              |
| `role`.`login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              |
| `role`.`login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 |
| `role`.`login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   |
| `role`.`name`                   | The name of the role.                                                                                             |
| `role`.`password_policy`        | 'true' if the password policy is enabled.                                                                         |
| `role`.`password_reset_days`    | Number of days a password is valid until user must change it.                                                     |
| `role`.`password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            |
| `role`.`priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. |
| `role`.`updated_at`             | The datetime of the last time the app key was updated.                                                            |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "is_admin_role": false,
        "login_ban_by_ip": false,
        "login_ban_time": 7200,
        "login_lockout_policy": true,
        "login_max_attempts": 15,
        "login_timeframe": 1200,
        "name": "TEST_ROLE_A",
        "password_policy": false,
        "password_reset_days": 90,
        "password_reuse_history": 5,
        "priority": 250
    }' \
    https://api.admin.domain.com/v/1.0/role/4?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "role": {
    "created_at": "2019-11-05T03:14:39+0000", 
    "id": 4, 
    "is_admin_role": false, 
    "login_ban_by_ip": false, 
    "login_ban_time": 7200, 
    "login_lockout_policy": true, 
    "login_max_attempts": 15, 
    "login_timeframe": 1200, 
    "name": "TEST_ROLE_A", 
    "password_policy": false, 
    "password_reset_days": 90, 
    "password_reuse_history": 5, 
    "priority": 250, 
    "updated_at": "2019-11-05T03:20:38+0000"
  }
}
```

### Delete a User Role

Use the following to permanently delete an existing role.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /role/{id}                                      |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 204  | No Content   | Delete successful.                                 |
| 404  | Not Found    | No role matching the supplied ID was found.        |
| 500  | Server error | Generic application error. Check application logs. |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/role/4?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## Administrators

### List Administrators

Use the following to read a list of administrators.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                                                                    |
| Paths           | /administrators<br>/administrators/{page}<br>/administrators/{page}/{limit}                                                                                                                                                                                                                                            |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                                                                              |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'username.asc', 'username.desc', 'joined_at.asc', 'joined_at.desc']; Default: 'id.asc'<br>- `role`: Integer; ID of role to filter results by; Optional |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no administrators on this page.          |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                      | Value                                                    |
| ---------------------------------------- | -------------------------------------------------------- | 
| `administrators`                         | The top-level administrator list resource.               |  
| `administrators`[].`created_at`          | The datetime the administrator was created.              |
| `administrators`[].`email`               | The administrator's email address.                       |
| `administrators`[].`first_name`          | The administrator's first name.                          |
| `administrators`[].`id`                  | The administrator's system id.                           |
| `administrators`[].`joined_at`           | The datetime the user joined the system.                 |
| `administrators`[].`last_name`           | The administrator's last name.                           |
| `administrators`[].`password_changed_at` | The last time the administrator changed their password.  |
| `administrators`[].`roles`               | List of the administrator's roles.                       |
| `administrators`[].`roles`[].`id`        | The role's system ID.                                    |
| `administrators`[].`roles`[].`name`      | The role's name.                                         |
| `administrators`[].`status`              | The status of the administrator.                         |
| `administrators`[].`status_changed_at`   | The datetime of the last time the status was changed.    |
| `administrators`[].`updated_at`          | The datetime of the last time administrator was updated. |
| `administrators`[].`uri`                 | The API endpoint for the administrator's resource.       |
| `administrators`[].`username`            | The administrator's username.                            |
| `limit`                                  | The limit of items to show on a single page.             |
| `next_uri`                               | The URI of the next page of results, if available.       |
| `page`                                   | The current list page number.                            |
| `previous_uri`                           | The URI of the previous page of results, if available.   |
| `total`                                  | The total count of items found.                          |


##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/administrators/2/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "administrators": [
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "email": "admin3@test.com", 
      "first_name": "Victor", 
      "id": 3, 
      "joined_at": "2018-11-15T00:00:00+0000", 
      "last_name": "Landon", 
      "password_changed_at": "2019-11-05T02:16:29+0000", 
      "roles": [], 
      "status": 1, 
      "status_changed_at": "2018-11-15T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "uri": "https://api.admin.domain.com/v/1.0/administrator/3", 
      "username": "admin3"
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "email": "admin4@test.com", 
      "first_name": "Tamela", 
      "id": 4, 
      "joined_at": "2018-11-20T00:00:00+0000", 
      "last_name": "Coburn", 
      "password_changed_at": "2019-11-05T02:16:32+0000", 
      "roles": [
        {
          "id": 2, 
          "name": "SUPER_ADMIN"
        }
      ], 
      "status": 2, 
      "status_changed_at": "2018-11-20T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "uri": "https://api.admin.domain.com/v/1.0/administrator/4", 
      "username": "admin4"
    }
  ], 
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/administrators/3/2", 
  "page": 2, 
  "previous_uri": "https://api.admin.domain.com/v/1.0/administrators/1/2", 
  "total": 5
}
```

### Read an Administrator

Use the following to read the information for a specific administrator.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | GET                                             | 
| Path            | /administrator/{id}                             |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                        |
| ---- | ------------ | ------------------------------------------------------------ |
| 200  | OK           | Request successful.                                          |
| 404  | Not Found    | No administrator matching the supplied ID or name was found. |
| 500  | Server error | Generic application error. Check application logs.           |

##### Response Payload

| Key                                   | Value                                                    |
| ------------------------------------- | -------------------------------------------------------- | 
| `administrator`                       | The top-level administrator list resource.               |  
| `administrator`.`created_at`          | The datetime the administrator was created.              |
| `administrator`.`email`               | The administrator's email address.                       |
| `administrator`.`first_name`          | The administrator's first name.                          |
| `administrator`.`id`                  | The administrator's system id.                           |
| `administrator`.`joined_at`           | The datetime the user joined the system.                 |
| `administrator`.`last_name`           | The administrator's last name.                           |
| `administrator`.`password_changed_at` | The last time the administrator changed their password.  |
| `administrator`.`roles`               | List of the administrator's roles.                       |
| `administrator`.`roles`[].`id`        | The role's system ID.                                    |
| `administrator`.`roles`[].`name`      | The role's name.                                         |
| `administrator`.`status`              | The status of the administrator.                         |
| `administrator`.`status_changed_at`   | The datetime of the last time the status was changed.    |
| `administrator`.`updated_at`          | The datetime of the last time administrator was updated. |
| `administrator`.`uri`                 | The API endpoint for the administrator's resource.       |
| `administrator`.`username`            | The administrator's username.                            |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/administrator/1?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "administrator": {
    "created_at": "2019-11-05T02:16:56+0000", 
    "email": "admin1@test.com", 
    "first_name": "Tommy", 
    "id": 1, 
    "joined_at": "2018-11-01T00:00:00+0000", 
    "last_name": "Lund", 
    "password_changed_at": "2019-11-05T02:16:25+0000", 
    "roles": [
      {
        "id": 2, 
        "name": "SUPER_ADMIN"
      }
    ], 
    "status": 1, 
    "status_changed_at": "2018-11-01T00:00:00+0000", 
    "updated_at": "2019-11-05T02:16:56+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/administrator/1", 
    "username": "admin1"
  }
}
```

### Create an Administrator

Use the following to create a administrator.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- | 
| Method     | POST                             | 
| Path       | /administrators                  |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key          | Value                                    | Validation                                                                                                 |
| ------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `email`      | The administrator's email address.       | Required; Unique; Valid email address format                                                               |
| `first_name` | The administrator's first name.          | Required; Length: 1-40 chars                                                                               |
| `joined_at`  | The datetime the user joined the system. | Required; Datetime                                                                                         |
| `last_name`  | The administrator's last name.           | Required; Length: 2-40 chars                                                                               |
| `password`   | The administrator's password.            | Required; Length: 8-40 chars; Must have 3 out of 4: (lowercase char, uppercase char, number, special char) |
| `roles`      | List of the administrator's role IDs.    | Required; List literal of Role IDs (integers)                                                              |
| `status`     | The status of the administrator.         | Required; Integer                                                                                          |
| `username`   | The administrator's username.            | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only             |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                   | Value                                                    |
| ------------------------------------- | -------------------------------------------------------- | 
| `administrator`                       | The top-level administrator list resource.               |  
| `administrator`.`created_at`          | The datetime the administrator was created.              |
| `administrator`.`email`               | The administrator's email address.                       |
| `administrator`.`first_name`          | The administrator's first name.                          |
| `administrator`.`id`                  | The administrator's system id.                           |
| `administrator`.`joined_at`           | The datetime the user joined the system.                 |
| `administrator`.`last_name`           | The administrator's last name.                           |
| `administrator`.`password_changed_at` | The last time the administrator changed their password.  |
| `administrator`.`roles`               | List of the administrator's roles.                       |
| `administrator`.`roles`[].`id`        | The role's system ID.                                    |
| `administrator`.`roles`[].`name`      | The role's name.                                         |
| `administrator`.`status`              | The status of the administrator.                         |
| `administrator`.`status_changed_at`   | The datetime of the last time the status was changed.    |
| `administrator`.`updated_at`          | The datetime of the last time administrator was updated. |
| `administrator`.`uri`                 | The API endpoint for the administrator's resource.       |
| `administrator`.`username`            | The administrator's username.                            |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "email": "admin8@test.com",
        "first_name": "Zena",
        "joined_at": "2019-11-02T12:00:00+0000",
        "last_name": "Clyde",
        "password": "admin8Pass",
        "roles": [2],
        "status": 5,
        "username": "admin8"
    }' \
    https://api.admin.domain.com/v/1.0/administrators?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "administrator": {
    "created_at": "2019-11-05T04:22:04+0000", 
    "email": "admin8@test.com", 
    "first_name": "Zena", 
    "id": 8, 
    "joined_at": "2019-11-02T12:00:00+0000", 
    "last_name": "Clyde", 
    "password_changed_at": "2019-11-05T04:22:06+0000", 
    "roles": [
      {
        "id": 2, 
        "name": "SUPER_ADMIN"
      }
    ], 
    "status": 5, 
    "status_changed_at": "2019-11-05T04:22:04+0000", 
    "updated_at": "2019-11-05T04:22:04+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/administrator/8", 
    "username": "admin8"
  }
}
```

### Update an Administrator

Use the following to update an existing administrator.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /administrator/{id}                             |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key          | Value                                    | Validation                                                                                                 |
| ------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `email`      | The administrator's email address.       | Required; Unique; Valid email address format                                                               |
| `first_name` | The administrator's first name.          | Required; Length: 1-40 chars                                                                               |
| `joined_at`  | The datetime the user joined the system. | Required; Datetime                                                                                         |
| `last_name`  | The administrator's last name.           | Required; Length: 2-40 chars                                                                               |
| `password`   | The administrator's password.            | Optional; Length: 8-40 chars; Must have 3 out of 4: (lowercase char, uppercase char, number, special char) |
| `roles`      | List of the administrator's role IDs.    | Required; List literal of Role IDs (integers)                                                              |
| `status`     | The status of the administrator.         | Required; Integer                                                                                          |
| `username`   | The administrator's username.            | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only             |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No administrator matching the supplied ID was found.                                                               |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                   | Value                                                    |
| ------------------------------------- | -------------------------------------------------------- | 
| `administrator`                       | The top-level administrator list resource.               |  
| `administrator`.`created_at`          | The datetime the administrator was created.              |
| `administrator`.`email`               | The administrator's email address.                       |
| `administrator`.`first_name`          | The administrator's first name.                          |
| `administrator`.`id`                  | The administrator's system id.                           |
| `administrator`.`joined_at`           | The datetime the user joined the system.                 |
| `administrator`.`last_name`           | The administrator's last name.                           |
| `administrator`.`password_changed_at` | The last time the administrator changed their password.  |
| `administrator`.`roles`               | List of the administrator's roles.                       |
| `administrator`.`roles`[].`id`        | The role's system ID.                                    |
| `administrator`.`roles`[].`name`      | The role's name.                                         |
| `administrator`.`status`              | The status of the administrator.                         |
| `administrator`.`status_changed_at`   | The datetime of the last time the status was changed.    |
| `administrator`.`updated_at`          | The datetime of the last time administrator was updated. |
| `administrator`.`uri`                 | The API endpoint for the administrator's resource.       |
| `administrator`.`username`            | The administrator's username.                            |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "email": "admin8a@test.com",
        "first_name": "Zeena",
        "joined_at": "2019-11-03T12:00:00+0000",
        "last_name": "Clide",
        "password": "admin8Pass",
        "roles": [2],
        "status": 1,
        "username": "admin8a"
    }' \
    https://api.admin.domain.com/v/1.0/administrator/8?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "administrator": {
    "created_at": "2019-11-05T04:22:04+0000", 
    "email": "admin8a@test.com", 
    "first_name": "Zeena", 
    "id": 8, 
    "joined_at": "2019-11-03T12:00:00+0000", 
    "last_name": "Clide", 
    "password_changed_at": "2019-11-05T04:33:16+0000", 
    "roles": [
      {
        "id": 2, 
        "name": "SUPER_ADMIN"
      }
    ], 
    "status": 1, 
    "status_changed_at": "2019-11-05T04:33:16+0000", 
    "updated_at": "2019-11-05T04:33:14+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/administrator/8", 
    "username": "admin8a"
  }
}
```

### Delete an Administrator

Use the following to permanently delete an existing administrator.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /administrator/{id}                             |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                |
| ---- | ------------ | ---------------------------------------------------- |
| 204  | No Content   | Delete successful.                                   |
| 404  | Not Found    | No administrator matching the supplied ID was found. |
| 500  | Server error | Generic application error. Check application logs.   |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/administrator/8?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## Users

### List Users

Use the following to read a list of users.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                               |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                                 |
| Paths           | /users<br>/users/{page}<br>/users/{page}/{limit}                                                                                                                                                                                                                                    |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                                           |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'username.asc', 'username.desc']; Default: 'id.asc'<br>- `role`: Integer; ID of role to filter results by; Optional |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no users on this page.                   |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                                          | Value                                                                                                                  |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | 
| `limit`                                                      | The limit of items to show on a single page.                                                                           |
| `next_uri`                                                   | The URI of the next page of results, if available.                                                                     |
| `page`                                                       | The current list page number.                                                                                          |
| `previous_uri`                                               | The URI of the previous page of results, if available.                                                                 |
| `total`                                                      | The total count of items found.                                                                                        |
| `users`                                                      | The top-level users list resource.                                                                                     | 
| `users`[].`created_at`                                       | The datetime the user was created.                                                                                     |
| `users`[].`email`                                            | The user's email address.                                                                                              |
| `users`[].`id`                                               | The user's system id.                                                                                                  |
| `users`[].`is_verified`                                      | 'true' if user has been verified - this determination is for the system owner to define, and can be ignored if unused. |
| `users`[].`password_changed_at`                              | The last time the user changed their password.                                                                         |
| `users`[].`profile`                                          | The user's profile object.                                                                                             |
| `users`[].`profile`.`first_name`                             | The user's first name.                                                                                                 |
| `users`[].`profile`.`joined_at`                              | The datetime the user joined the system.                                                                               |
| `users`[].`profile`.`last_name`                              | The user's last name.                                                                                                  |
| `users`[].`roles`                                            | List of the user's roles.                                                                                              |
| `users`[].`roles`[].`id`                                     | The role's system ID.                                                                                                  |
| `users`[].`roles`[].`name`                                   | The role's name.                                                                                                       |
| `users`[].`status`                                           | The status of the user.                                                                                                |
| `users`[].`status_changed_at`                                | The datetime of the last time the status was changed.                                                                  |
| `users`[].`terms_of_services`                                | List of Terms of Services the user has accepted.                                                                       |
| `users`[].`terms_of_services`[].`accept_date`                | The datetime the user accepted the Terms of Service.                                                                   |
| `users`[].`terms_of_services`[].`ip_address`                 | The IP address of the system the user accepted the Terms of Service on.                                                |
| `users`[].`terms_of_services`[].`terms_of_service`           | The Terms of Service object.                                                                                           |
| `users`[].`terms_of_services`[].`terms_of_service`.`id`      | The Terms of Service system id.                                                                                        |
| `users`[].`terms_of_services`[].`terms_of_service`.`version` | The Terms of Service version number.                                                                                   |
| `users`[].`updated_at`                                       | The datetime of the last time user was updated.                                                                        |
| `users`[].`uri`                                              | The API endpoint for the user's resource.                                                                              |
| `users`[].`username`                                         | The user's username.                                                                                                   |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/users/2/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/users/3/2", 
  "page": 2, 
  "previous_uri": "https://api.admin.domain.com/v/1.0/users/1/2", 
  "total": 7, 
  "users": [
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "email": "user3@test.com", 
      "id": 3, 
      "is_verified": true, 
      "password_changed_at": "2019-11-05T02:16:45+0000", 
      "profile": {
        "first_name": "Duane", 
        "joined_at": "2018-12-15T00:00:00+0000", 
        "last_name": "Hargrave"
      }, 
      "roles": [
        {
          "id": 1, 
          "name": "USER"
        }
      ], 
      "status": 1, 
      "status_changed_at": "2018-12-15T00:00:00+0000", 
      "terms_of_services": [
        {
          "accept_date": "2019-01-02T00:00:00+0000", 
          "ip_address": "1.1.1.3", 
          "terms_of_service": {
            "id": 2, 
            "version": "1.1"
          }
        }
      ], 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "uri": "https://api.admin.domain.com/v/1.0/user/3", 
      "username": "user3"
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "email": "user5@test.com", 
      "id": 5, 
      "is_verified": false, 
      "password_changed_at": "2019-11-05T02:16:49+0000", 
      "profile": {
        "first_name": "Elroy", 
        "joined_at": "2018-12-20T00:00:00+0000", 
        "last_name": "Hunnicutt"
      }, 
      "roles": [
        {
          "id": 1, 
          "name": "USER"
        }
      ], 
      "status": 2, 
      "status_changed_at": "2018-12-25T00:00:00+0000", 
      "terms_of_services": [], 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "uri": "https://api.admin.domain.com/v/1.0/user/5", 
      "username": "user5"
    }
  ]
}
```

### Read a User

Use the following to read the information for a specific user.

##### Request

| HTTP            | Value                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------- | 
| Method          | GET                                                                                           | 
| Path            | /user/{id}<br>/user/{username}                                                                |
| Path Parameters | - `id`: Integer; The system ID for the resource<br>- `username`: String; The user's username. |

##### Response Codes
 
| Code | Description  | Notes                                               |
| ---- | ------------ | --------------------------------------------------- |
| 200  | OK           | Request successful.                                 |
| 404  | Not Found    | No user matching the supplied ID or name was found. |
| 500  | Server error | Generic application error. Check application logs.  |

##### Response Payload

| Key                                                       | Value                                                                                                                  |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | 
| `user`                                                    | The top-level users resource.                                                                                          | 
| `user`.`created_at`                                       | The datetime the user was created.                                                                                     |
| `user`.`email`                                            | The user's email address.                                                                                              |
| `user`.`id`                                               | The user's system id.                                                                                                  |
| `user`.`is_verified`                                      | 'true' if user has been verified - this determination is for the system owner to define, and can be ignored if unused. |
| `user`.`password_changed_at`                              | The last time the user changed their password.                                                                         |
| `user`.`profile`                                          | The user's profile object.                                                                                             |
| `user`.`profile`.`first_name`                             | The user's first name.                                                                                                 |
| `user`.`profile`.`joined_at`                              | The datetime the user joined the system.                                                                               |
| `user`.`profile`.`last_name`                              | The user's last name.                                                                                                  |
| `user`.`roles`                                            | List of the user's roles.                                                                                              |
| `user`.`roles`[].`id`                                     | The role's system ID.                                                                                                  |
| `user`.`roles`[].`name`                                   | The role's name.                                                                                                       |
| `user`.`status`                                           | The status of the user.                                                                                                |
| `user`.`status_changed_at`                                | The datetime of the last time the status was changed.                                                                  |
| `user`.`terms_of_services`                                | List of Terms of Services the user has accepted.                                                                       |
| `user`.`terms_of_services`[].`accept_date`                | The datetime the user accepted the Terms of Service.                                                                   |
| `user`.`terms_of_services`[].`ip_address`                 | The IP address of the system the user accepted the Terms of Service on.                                                |
| `user`.`terms_of_services`[].`terms_of_service`           | The Terms of Service object.                                                                                           |
| `user`.`terms_of_services`[].`terms_of_service`.`id`      | The Terms of Service system id.                                                                                        |
| `user`.`terms_of_services`[].`terms_of_service`.`version` | The Terms of Service version number.                                                                                   |
| `user`.`updated_at`                                       | The datetime of the last time user was updated.                                                                        |
| `user`.`uri`                                              | The API endpoint for the user's resource.                                                                              |
| `user`.`username`                                         | The user's username.                                                                                                   |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/user/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user": {
    "created_at": "2019-11-05T02:16:56+0000", 
    "email": "user2@test.com", 
    "id": 2, 
    "is_verified": true, 
    "password_changed_at": "2019-11-05T02:16:43+0000", 
    "profile": {
      "first_name": "Lynne", 
      "joined_at": "2018-12-10T00:00:00+0000", 
      "last_name": "Harford"
    }, 
    "roles": [
      {
        "id": 1, 
        "name": "USER"
      }
    ], 
    "status": 1, 
    "status_changed_at": "2018-12-10T00:00:00+0000", 
    "terms_of_services": [
      {
        "accept_date": "2019-01-06T00:00:00+0000", 
        "ip_address": "1.1.1.2", 
        "terms_of_service": {
          "id": 2, 
          "version": "1.1"
        }
      }, 
      {
        "accept_date": "2018-12-10T00:00:00+0000", 
        "ip_address": "1.1.1.2", 
        "terms_of_service": {
          "id": 1, 
          "version": "1.0"
        }
      }
    ], 
    "updated_at": "2019-11-05T02:16:56+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/user/2", 
    "username": "user2"
  }
}
```

### Create a User

Use the following to create a user.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- |
| Method     | POST                             |
| Path       | /users                           |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key                    | Value                                    | Validation                                                                                                 |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `email`                | The user's email address.                | Required; Unique; Valid email address format                                                               |
| `is_verified`          | 'true' if user has been verified         | Required; Boolean                                                                                          |
| `password`             | The users's password.                    | Required; Length: 8-40 chars; Must have 3 out of 4: (lowercase char, uppercase char, number, special char) |
| `profile`              | The user's profile object.               | Optional; Object                                                                                           |
| `profile`.`first_name` | The user's first name.                   | Required; Length: 1-40 chars                                                                               |
| `profile`.`joined_at`  | The datetime the user joined the system. | Required; Datetime                                                                                         |
| `profile`.`last_name`  | The user's last name.                    | Required; Length: 2-40 chars                                                                               |
| `roles`                | List of the users's role IDs.            | Required; List literal of Role IDs (integers)                                                              |
| `status`               | The status of the user.                  | Required; Integer                                                                                          |
| `username`             | The user's username.                     | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only             |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                                       | Value                                                                                                                  |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | 
| `user`                                                    | The top-level users list resource.                                                                                     | 
| `user`.`created_at`                                       | The datetime the user was created.                                                                                     |
| `user`.`email`                                            | The user's email address.                                                                                              |
| `user`.`id`                                               | The user's system id.                                                                                                  |
| `user`.`is_verified`                                      | 'true' if user has been verified - this determination is for the system owner to define, and can be ignored if unused. |
| `user`.`password_changed_at`                              | The last time the user changed their password.                                                                         |
| `user`.`profile`                                          | The user's profile object.                                                                                             |
| `user`.`profile`.`first_name`                             | The user's first name.                                                                                                 |
| `user`.`profile`.`joined_at`                              | The datetime the user joined the system.                                                                               |
| `user`.`profile`.`last_name`                              | The user's last name.                                                                                                  |
| `user`.`roles`                                            | List of the user's roles.                                                                                              |
| `user`.`roles`[].`id`                                     | The role's system ID.                                                                                                  |
| `user`.`roles`[].`name`                                   | The role's name.                                                                                                       |
| `user`.`status`                                           | The status of the user.                                                                                                |
| `user`.`status_changed_at`                                | The datetime of the last time the status was changed.                                                                  |
| `user`.`terms_of_services`                                | List of Terms of Services the user has accepted.                                                                       |
| `user`.`terms_of_services`[].`accept_date`                | The datetime the user accepted the Terms of Service.                                                                   |
| `user`.`terms_of_services`[].`ip_address`                 | The IP address of the system the user accepted the Terms of Service on.                                                |
| `user`.`terms_of_services`[].`terms_of_service`           | The Terms of Service object.                                                                                           |
| `user`.`terms_of_services`[].`terms_of_service`.`id`      | The Terms of Service system id.                                                                                        |
| `user`.`terms_of_services`[].`terms_of_service`.`version` | The Terms of Service version number.                                                                                   |
| `user`.`updated_at`                                       | The datetime of the last time user was updated.                                                                        |
| `user`.`uri`                                              | The API endpoint for the user's resource.                                                                              |
| `user`.`username`                                         | The user's username.                                                                                                   |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "email": "user10@test.com",
        "is_verified": false,
        "password": "user10Pass",
        "profile": {
            "first_name": "Vivyan",
            "joined_at": "2019-05-21T08:30:00+0000",
            "last_name": "Joyce"
        },
        "roles": [1],
        "status": 5,
        "username": "user10"
    }' \
    https://api.admin.domain.com/v/1.0/users?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user": {
    "created_at": "2019-11-05T11:03:56+0000", 
    "email": "user10@test.com", 
    "id": 10, 
    "is_verified": false, 
    "password_changed_at": "2019-11-05T11:03:58+0000", 
    "profile": {
      "first_name": "Vivyan", 
      "joined_at": "2019-05-21T08:30:00+0000", 
      "last_name": "Joyce"
    }, 
    "roles": [
      {
        "id": 1, 
        "name": "USER"
      }
    ], 
    "status": 5, 
    "status_changed_at": "2019-11-05T11:03:56+0000", 
    "terms_of_services": [], 
    "updated_at": "2019-11-05T11:03:56+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/user/10", 
    "username": "user10"
  }
}
```

### Update a User

Use the following to update an existing user.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /user/{id}                                      |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key                    | Value                                    | Validation                                                                                                 |
| ---------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `email`                | The user's email address.                | Required; Unique; Valid email address format                                                               |
| `is_verified`          | 'true' if user has been verified         | Required; Boolean                                                                                          |
| `password`             | The users's password.                    | Optional; Length: 8-40 chars; Must have 3 out of 4: (lowercase char, uppercase char, number, special char) |
| `profile`              | The user's profile object.               | Optional; Object                                                                                           |
| `profile`.`first_name` | The user's first name.                   | Required; Length: 1-40 chars                                                                               |
| `profile`.`joined_at`  | The datetime the user joined the system. | Required; Datetime                                                                                         |
| `profile`.`last_name`  | The user's last name.                    | Required; Length: 2-40 chars                                                                               |
| `roles`                | List of the users's role IDs.            | Required; List literal of Role IDs (integers)                                                              |
| `status`               | The status of the user.                  | Required; Integer                                                                                          |
| `username`             | The user's username.                     | Required; Unique; Length: 2-40 chars; Not a number; Alphanumeric chars and the underscore only             |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No user matching the supplied ID was found.                                                                        |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                                       | Value                                                                                                                  |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | 
| `user`                                                    | The top-level users list resource.                                                                                     | 
| `user`.`created_at`                                       | The datetime the user was created.                                                                                     |
| `user`.`email`                                            | The user's email address.                                                                                              |
| `user`.`id`                                               | The user's system id.                                                                                                  |
| `user`.`is_verified`                                      | 'true' if user has been verified - this determination is for the system owner to define, and can be ignored if unused. |
| `user`.`password_changed_at`                              | The last time the user changed their password.                                                                         |
| `user`.`profile`                                          | The user's profile object.                                                                                             |
| `user`.`profile`.`first_name`                             | The user's first name.                                                                                                 |
| `user`.`profile`.`joined_at`                              | The datetime the user joined the system.                                                                               |
| `user`.`profile`.`last_name`                              | The user's last name.                                                                                                  |
| `user`.`roles`                                            | List of the user's roles.                                                                                              |
| `user`.`roles`[].`id`                                     | The role's system ID.                                                                                                  |
| `user`.`roles`[].`name`                                   | The role's name.                                                                                                       |
| `user`.`status`                                           | The status of the user.                                                                                                |
| `user`.`status_changed_at`                                | The datetime of the last time the status was changed.                                                                  |
| `user`.`terms_of_services`                                | List of Terms of Services the user has accepted.                                                                       |
| `user`.`terms_of_services`[].`accept_date`                | The datetime the user accepted the Terms of Service.                                                                   |
| `user`.`terms_of_services`[].`ip_address`                 | The IP address of the system the user accepted the Terms of Service on.                                                |
| `user`.`terms_of_services`[].`terms_of_service`           | The Terms of Service object.                                                                                           |
| `user`.`terms_of_services`[].`terms_of_service`.`id`      | The Terms of Service system id.                                                                                        |
| `user`.`terms_of_services`[].`terms_of_service`.`version` | The Terms of Service version number.                                                                                   |
| `user`.`updated_at`                                       | The datetime of the last time user was updated.                                                                        |
| `user`.`uri`                                              | The API endpoint for the user's resource.                                                                              |
| `user`.`username`                                         | The user's username.                                                                                                   |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "email": "user10a@test.com",
        "is_verified": true,
        "profile": {
            "first_name": "Vivian",
            "joined_at": "2019-06-21T08:30:00+0000",
            "last_name": "Joycee"
        },
        "roles": [1],
        "status": 2,
        "username": "user10a"
    }' \
    https://api.admin.domain.com/v/1.0/user/10?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user": {
    "created_at": "2019-11-05T11:03:56+0000", 
    "email": "user10a@test.com", 
    "id": 10, 
    "is_verified": true, 
    "password_changed_at": "2019-11-05T11:03:58+0000", 
    "profile": {
      "first_name": "Vivian", 
      "joined_at": "2019-06-21T08:30:00+0000", 
      "last_name": "Joycee"
    }, 
    "roles": [
      {
        "id": 1, 
        "name": "USER"
      }
    ], 
    "status": 2, 
    "status_changed_at": "2019-11-05T11:35:31+0000", 
    "terms_of_services": [], 
    "updated_at": "2019-11-05T11:35:31+0000", 
    "uri": "https://api.admin.domain.com/v/1.0/user/10", 
    "username": "user10a"
  }
}
```

### Delete a User

Use the following to permanently delete an existing user.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /user/{id}                                      |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                |
| ---- | ------------ | ---------------------------------------------------- |
| 204  | No Content   | Delete successful.                                   |
| 404  | Not Found    | No user matching the supplied ID was found.          |
| 500  | Server error | Generic application error. Check application logs.   |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/user/10?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## User Profiles

User profiles can be managed on their own or via the `profile` property of a User resource.

### List User Profiles

Use the following to read a list of user profiles.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                  |
| Paths           | /user_profiles<br>/user_profiles/{page}<br>/user_profiles/{page}/{limit}                                                                                                                                                                             |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                            |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'user_id.asc', 'user_id.desc', 'joined_at.asc', 'joined_at.desc']; Default: 'id.asc' |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no user profiles on this page.           |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                   | Value                                                     |
| ------------------------------------- | --------------------------------------------------------- | 
| `limit`                               | The limit of items to show on a single page.              |
| `next_uri`                            | The URI of the next page of results, if available.        |
| `page`                                | The current list page number.                             |
| `previous_uri`                        | The URI of the previous page of results, if available.    |
| `total`                               | The total count of items found.                           |
| `user_profiles`                       | The top-level user profile list resource.                 | 
| `user_profiles`[].`created_at`        | The datetime the user profile was created.                |
| `user_profiles`[].`first_name`        | The user's first name.                                    |
| `user_profiles`[].`id`                | The user profile's system id.                             |
| `user_profiles`[].`joined_at`         | The datetime the user joined the system.                  |
| `user_profiles`[].`last_name`         | The user's last name.                                     |
| `user_profiles`[].`status`            | The status of the user profile.                           |
| `user_profiles`[].`status_changed_at` | The datetime of the last time the status was changed.     |
| `user_profiles`[].`updated_at`        | The datetime of the last time user profile was updated.   |
| `user_profiles`[].`user_id`           | The system id of the user the profile is associated with. |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/user_profiles/2/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/user_profiles/3/2", 
  "page": 2, 
  "previous_uri": "https://api.admin.domain.com/v/1.0/user_profiles/1/2", 
  "total": 6, 
  "user_profiles": [
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "first_name": "Duane", 
      "id": 3, 
      "joined_at": "2018-12-15T00:00:00+0000", 
      "last_name": "Hargrave", 
      "status": 1, 
      "status_changed_at": "2018-12-15T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user_id": 3
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "first_name": "Elroy", 
      "id": 5, 
      "joined_at": "2018-12-20T00:00:00+0000", 
      "last_name": "Hunnicutt", 
      "status": 2, 
      "status_changed_at": "2018-12-25T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user_id": 5
    }
  ]
}
```

### Read a User Profile

Use the following to read the information for a specific user profile.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- |
| Method          | GET                                             |
| Path            | /user_profile/{id}                              |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                       |
| ---- | ------------ | ----------------------------------------------------------- |
| 200  | OK           | Request successful.                                         |
| 404  | Not Found    | No user profile matching the supplied ID or name was found. |
| 500  | Server error | Generic application error. Check application logs.          |

##### Response Payload

| Key                                 | Value                                                    |
| ----------------------------------- | -------------------------------------------------------- |
| `user_profile`                     | The top-level user profile resource.                      |
| `user_profile`.`created_at`        | The datetime the user profile was created.                |
| `user_profile`.`first_name`        | The user's first name.                                    |
| `user_profile`.`id`                | The user profile's system id.                             |
| `user_profile`.`joined_at`         | The datetime the user joined the system.                  |
| `user_profile`.`last_name`         | The user's last name.                                     |
| `user_profile`.`status`            | The status of the user profile.                           |
| `user_profile`.`status_changed_at` | The datetime of the last time the status was changed.     |
| `user_profile`.`updated_at`        | The datetime of the last time user profile was updated.   |
| `user_profile`.`user_id`           | The system id of the user the profile is associated with. |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/user_profile/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user_profile": {
    "created_at": "2019-11-05T02:16:56+0000", 
    "first_name": "Lynne", 
    "id": 2, 
    "joined_at": "2018-12-10T00:00:00+0000", 
    "last_name": "Harford", 
    "status": 1, 
    "status_changed_at": "2018-12-10T00:00:00+0000", 
    "updated_at": "2019-11-05T02:16:56+0000", 
    "user_id": 2
  }
}
```

### Create a User Profile

Use the following to create a user profile.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- |
| Method     | POST                             |
| Path       | /user_profiles                   |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key          | Value                                                     | Validation                   |
| ------------ | --------------------------------------------------------- | -----------------------------|
| `first_name` | The user's first name.                                    | Required; Length: 1-40 chars |
| `joined_at`  | The datetime the user joined the system.                  | Required; Datetime           |
| `last_name`  | The user's last name.                                     | Required; Length: 2-40 chars |
| `status`     | The status of the user profile.                           | Required; Integer            |
| `user_id`    | The system id of the user the profile is associated with. | Required; Integer            |


##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                 | Value                                                    |
| ----------------------------------- | -------------------------------------------------------- |
| `user_profile`                     | The top-level user profile resource.                      |
| `user_profile`.`created_at`        | The datetime the user profile was created.                |
| `user_profile`.`first_name`        | The user's first name.                                    |
| `user_profile`.`id`                | The user profile's system id.                             |
| `user_profile`.`joined_at`         | The datetime the user joined the system.                  |
| `user_profile`.`last_name`         | The user's last name.                                     |
| `user_profile`.`status`            | The status of the user profile.                           |
| `user_profile`.`status_changed_at` | The datetime of the last time the status was changed.     |
| `user_profile`.`updated_at`        | The datetime of the last time user profile was updated.   |
| `user_profile`.`user_id`           | The system id of the user the profile is associated with. |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "first_name": "Vivyan",
        "joined_at": "2019-05-21T08:30:00+0000",
        "last_name": "Joyce",
        "status": 5,
        "user_id": 9
    }' \
    https://api.admin.domain.com/v/1.0/user_profiles?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user_profile": {
    "created_at": "2019-11-05T13:59:07+0000", 
    "first_name": "Vivyan", 
    "id": 10, 
    "joined_at": "2019-05-21T08:30:00+0000", 
    "last_name": "Joyce", 
    "status": 5, 
    "status_changed_at": "2019-11-05T13:59:07+0000", 
    "updated_at": "2019-11-05T13:59:07+0000", 
    "user_id": 9
  }
}
```

### Update a User Profile

Use the following to update an existing user profile.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /user_profile/{id}                              |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key          | Value                                                     | Validation                   |
| ------------ | --------------------------------------------------------- | -----------------------------|
| `first_name` | The user's first name.                                    | Required; Length: 1-40 chars |
| `joined_at`  | The datetime the user joined the system.                  | Required; Datetime           |
| `last_name`  | The user's last name.                                     | Required; Length: 2-40 chars |
| `status`     | The status of the user profile.                           | Required; Integer            |
| `user_id`    | The system id of the user the profile is associated with. | Required; Integer            |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No user profile matching the supplied ID was found.                                                                |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                | Value                                                     |
| ---------------------------------- | --------------------------------------------------------- |
| `user_profile`                     | The top-level user profile resource.                      |
| `user_profile`.`created_at`        | The datetime the user profile was created.                |
| `user_profile`.`first_name`        | The user's first name.                                    |
| `user_profile`.`id`                | The user profile's system id.                             |
| `user_profile`.`joined_at`         | The datetime the user joined the system.                  |
| `user_profile`.`last_name`         | The user's last name.                                     |
| `user_profile`.`status`            | The status of the user profile.                           |
| `user_profile`.`status_changed_at` | The datetime of the last time the status was changed.     |
| `user_profile`.`updated_at`        | The datetime of the last time user profile was updated.   |
| `user_profile`.`user_id`           | The system id of the user the profile is associated with. |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "first_name": "Vivian",
        "joined_at": "2019-06-21T08:30:00+0000",
        "last_name": "Joycee",
        "status": 2,
        "user_id": 9
    }' \
    https://api.admin.domain.com/v/1.0/user_profile/10?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "user_profile": {
    "created_at": "2019-11-05T13:59:07+0000", 
    "first_name": "Vivian", 
    "id": 10, 
    "joined_at": "2019-06-21T08:30:00+0000", 
    "last_name": "Joycee", 
    "status": 2, 
    "status_changed_at": "2019-11-05T14:03:05+0000", 
    "updated_at": "2019-11-05T14:03:05+0000", 
    "user_id": 9
  }
}
```

### Delete a User Profile

Use the following to permanently delete an existing user profile.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /user_profile/{id}                              |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                |
| ---- | ------------ | ---------------------------------------------------- |
| 204  | No Content   | Delete successful.                                   |
| 404  | Not Found    | No user profile matching the supplied ID was found.  |
| 500  | Server error | Generic application error. Check application logs.   |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/user_profile/10?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## Terms of Services

### List Terms of Service

Use the following to read a list of terms of services.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                      |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                        |
| Paths           | /terms_of_services<br>/terms_of_services/{page}<br>/terms_of_services/{page}/{limit}                                                                                                                                                                       |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                  |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'publish_date.asc', 'publish_date.desc', 'version.asc', 'version.desc']; Default: 'id.asc' |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no terms of services on this page.       |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                       | Value                                                       |
| ----------------------------------------- | ----------------------------------------------------------- | 
| `limit`                                   | The limit of items to show on a single page.                |
| `next_uri`                                | The URI of the next page of results, if available.          |
| `page`                                    | The current list page number.                               |
| `previous_uri`                            | The URI of the previous page of results, if available.      |
| `terms_of_services`                       | The top-level terms of service list resource.               | 
| `terms_of_services`[].`created_at`        | The datetime the terms of service was created.              |
| `terms_of_services`[].`id`                | The terms of service's system id.                           |
| `terms_of_services`[].`publish_date`      | The datetime the terms of service was published.            |
| `terms_of_services`[].`status`            | The status of the terms of service.                         |
| `terms_of_services`[].`status_changed_at` | The datetime of the last time the status was changed.       |
| `terms_of_services`[].`text`              | The full text of the terms of service.                      |
| `terms_of_services`[].`updated_at`        | The datetime of the last time terms of service was updated. |
| `terms_of_services`[].`version`           | The version number of the terms of service.                 |
| `total`                                   | The total count of items found.                             |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/terms_of_services/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/terms_of_services/2/2", 
  "page": 1, 
  "terms_of_services": [
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "publish_date": "2018-06-15T00:00:00+0000", 
      "status": 1, 
      "status_changed_at": "2018-06-15T00:00:00+0000", 
      "text": "This is TOS 1", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "version": "1.0"
    }, 
    {
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "publish_date": "2019-01-01T00:00:00+0000", 
      "status": 1, 
      "status_changed_at": "2019-01-01T00:00:00+0000", 
      "text": "This is TOS 2", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "version": "1.1"
    }
  ], 
  "total": 4
}
```

### Read a Terms of Service

Use the following to read the information for a specific terms of service.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- |
| Method          | GET                                             |
| Path            | /terms_of_service/{id}                          |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                           |
| ---- | ------------ | --------------------------------------------------------------- |
| 200  | OK           | Request successful.                                             |
| 404  | Not Found    | No terms of service matching the supplied ID or name was found. |
| 500  | Server error | Generic application error. Check application logs.              |

##### Response Payload

| Key                                    | Value                                                       |
| -------------------------------------- | ----------------------------------------------------------- | 
| `terms_of_service`                     | The top-level terms of service resource.                    | 
| `terms_of_service`.`created_at`        | The datetime the terms of service was created.              |
| `terms_of_service`.`id`                | The terms of service's system id.                           |
| `terms_of_service`.`publish_date`      | The datetime the terms of service was published.            |
| `terms_of_service`.`status`            | The status of the terms of service.                         |
| `terms_of_service`.`status_changed_at` | The datetime of the last time the status was changed.       |
| `terms_of_service`.`text`              | The full text of the terms of service.                      |
| `terms_of_service`.`updated_at`        | The datetime of the last time terms of service was updated. |
| `terms_of_service`.`version`           | The version number of the terms of service.                 |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/terms_of_service/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "terms_of_service": {
    "created_at": "2019-11-05T02:16:56+0000", 
    "id": 2, 
    "publish_date": "2019-01-01T00:00:00+0000", 
    "status": 1, 
    "status_changed_at": "2019-01-01T00:00:00+0000", 
    "text": "This is TOS 2", 
    "updated_at": "2019-11-05T02:16:56+0000", 
    "version": "1.1"
  }
}
```
### Create a Terms of Service

Use the following to create a terms of service.

##### Request

| HTTP       | Value                            |
| ---------- | -------------------------------- |
| Method     | POST                             |
| Path       | /terms_of_services               |
| Headers    | `Content-Type`: application/json |

##### Request Payload

| Key            | Value                                            | Validation                   |
| -------------- | ------------------------------------------------ | -----------------------------|
| `publish_date` | The datetime the terms of service was published. | Required; Datetime           |
| `status`       | The status of the terms of service.              | Required; Integer            |
| `text`         | The full text of the terms of service.           | Required; Text               |
| `version`      | The version number of the terms of service.      | Required; Length: 1-10 chars |


##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 201  | Created      | Resource successfully created.                                                                                     |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                    | Value                                                       |
| -------------------------------------- | ----------------------------------------------------------- | 
| `terms_of_service`                     | The top-level terms of service resource.                    | 
| `terms_of_service`.`created_at`        | The datetime the terms of service was created.              |
| `terms_of_service`.`id`                | The terms of service's system id.                           |
| `terms_of_service`.`publish_date`      | The datetime the terms of service was published.            |
| `terms_of_service`.`status`            | The status of the terms of service.                         |
| `terms_of_service`.`status_changed_at` | The datetime of the last time the status was changed.       |
| `terms_of_service`.`text`              | The full text of the terms of service.                      |
| `terms_of_service`.`updated_at`        | The datetime of the last time terms of service was updated. |
| `terms_of_service`.`version`           | The version number of the terms of service.                 |

##### Example

###### Request

```ssh
curl -X POST -H "Content-Type: application/json" \
    -d '{
        "publish_date": "2019-10-31T20:30:00+0000",
        "status": 5,
        "text": "This is TOS 7",
        "version": "2.1"
    }' \
    https://api.admin.domain.com/v/1.0/terms_of_services?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "terms_of_service": {
    "created_at": "2019-11-05T15:21:16+0000", 
    "id": 7, 
    "publish_date": "2019-10-31T20:30:00+0000", 
    "status": 5, 
    "status_changed_at": "2019-11-05T15:21:16+0000", 
    "text": "This is TOS 7", 
    "updated_at": "2019-11-05T15:21:16+0000", 
    "version": "2.1"
  }
}
```

### Update a Terms of Service

Use the following to update an existing terms of service.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | PUT                                             | 
| Path            | /terms_of_service/{id}                          |
| Path Parameters | - `id`: Integer; The system ID for the resource |
| Headers         | `Content-Type`: application/json                |

##### Request Payload

| Key            | Value                                            | Validation                   |
| -------------- | ------------------------------------------------ | -----------------------------|
| `publish_date` | The datetime the terms of service was published. | Required; Datetime           |
| `status`       | The status of the terms of service.              | Required; Integer            |
| `text`         | The full text of the terms of service.           | Required; Text               |
| `version`      | The version number of the terms of service.      | Required; Length: 1-10 chars |

##### Response Codes
 
| Code | Description  | Notes                                                                                                              |
| ---- | ------------ | ------------------------------------------------------------------------------------------------------------------ |
| 200  | OK           | Update successful.                                                                                                 |
| 400  | Bad Request  | Could not complete the request due to bad client data. Fix the errors mentioned in the `error` field and resubmit. |
| 404  | Not Found    | No terms of service matching the supplied ID was found.                                                            |
| 500  | Server error | Generic application error. Check application logs.                                                                 |

##### Response Payload

| Key                                    | Value                                                       |
| -------------------------------------- | ----------------------------------------------------------- | 
| `terms_of_service`                     | The top-level terms of service resource.                    | 
| `terms_of_service`.`created_at`        | The datetime the terms of service was created.              |
| `terms_of_service`.`id`                | The terms of service's system id.                           |
| `terms_of_service`.`publish_date`      | The datetime the terms of service was published.            |
| `terms_of_service`.`status`            | The status of the terms of service.                         |
| `terms_of_service`.`status_changed_at` | The datetime of the last time the status was changed.       |
| `terms_of_service`.`text`              | The full text of the terms of service.                      |
| `terms_of_service`.`updated_at`        | The datetime of the last time terms of service was updated. |
| `terms_of_service`.`version`           | The version number of the terms of service.                 |

##### Example

###### Request

```ssh
curl -X PUT -H "Content-Type: application/json" \
    -d '{
        "publish_date": "2019-11-01T00:00:00+0000",
        "status": 2,
        "text": "This is TOS 7a",
        "version": "3.0"
    }' \
    https://api.admin.domain.com/v/1.0/terms_of_service/7?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "terms_of_service": {
    "created_at": "2019-11-05T15:21:16+0000", 
    "id": 7, 
    "publish_date": "2019-11-01T00:00:00+0000", 
    "status": 2, 
    "status_changed_at": "2019-11-05T15:26:09+0000", 
    "text": "This is TOS 7a", 
    "updated_at": "2019-11-05T15:26:09+0000", 
    "version": "3.0"
  }
}
```

### Delete a Terms of Service

Use the following to permanently delete an existing terms of service.

##### Request

| HTTP            | Value                                           |
| --------------- | ----------------------------------------------- | 
| Method          | DELETE                                          | 
| Path            | /terms_of_service/{id}                          |
| Path Parameters | - `id`: Integer; The system ID for the resource |

##### Response Codes
 
| Code | Description  | Notes                                                   |
| ---- | ------------ | ------------------------------------------------------- |
| 204  | No Content   | Delete successful.                                      |
| 404  | Not Found    | No terms of service matching the supplied ID was found. |
| 500  | Server error | Generic application error. Check application logs.      |

##### Example

###### Request

```ssh
curl -X DELETE https://api.admin.domain.com/v/1.0/terms_of_service/7?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

<br><br>

## Countries

### List Countries

Use the following to read a list of countries.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                   |
| Paths           | /countries<br>/countries/{page}<br>/countries/{page}/{limit}                                                                                                                                                                                                          |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                             |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'name.asc', 'name.desc', 'code_2.asc', 'code_2.desc', 'code_3.asc', 'code_3.desc']; Default: 'id.asc' |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no countries on this page.               |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                               | Value                                                  |
| --------------------------------- | ------------------------------------------------------ | 
| `countries`                       | The top-level country list resource.                   | 
| `countries`[].`code_2`            | The country's two character country code.              |
| `countries`[].`code_3`            | The country's three character country code.            |
| `countries`[].`created_at`        | The datetime the country was created.                  |
| `countries`[].`id`                | The country's system id.                               |
| `countries`[].`name`              | The country's full name.                               |
| `countries`[].`status`            | The status of the country.                             |
| `countries`[].`status_changed_at` | The datetime of the last time the status was changed.  |
| `countries`[].`updated_at`        | The datetime of the last time country was updated.     |
| `limit`                           | The limit of items to show on a single page.           |
| `next_uri`                        | The URI of the next page of results, if available.     |
| `page`                            | The current list page number.                          |
| `previous_uri`                    | The URI of the previous page of results, if available. |
| `total`                           | The total count of items found.                        |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/countries/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "countries": [
    {
      "code_2": "US", 
      "code_3": "USA", 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "name": "United States", 
      "status": 1, 
      "status_changed_at": "2018-01-01T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000"
    }, 
    {
      "code_2": "MX", 
      "code_3": "MEX", 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "name": "Mexico", 
      "status": 1, 
      "status_changed_at": "2018-01-01T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000"
    }
  ], 
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/countries/2/2", 
  "page": 1, 
  "total": 5
}
```

<br><br>

## Regions

### List Regions

Use the following to read a list of regions.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                                                                       |
| Paths           | /regions<br>/regions/{page}<br>/regions/{page}/{limit}                                                                                                                                                                                                                                                                    |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                                                                                 |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'name.asc', 'name.desc', 'code_2.asc', 'code_2.desc']; Default: 'id.asc'<br>- `country_id`: Integer; Optional; The ID of the country to filter results by |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no regions on this page.                 |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                             | Value                                                  |
| ------------------------------- | ------------------------------------------------------ | 
| `regions`                       | The top-level region list resource.                    | 
| `regions`[].`code_2`            | The region's two character code.                       |
| `regions`[].`country`           | The region's country object.                           |
| `regions`[].`country`.`code_2`  | The country's two character country code.              |
| `regions`[].`country`.`code_3`  | The country's three character country code.            |
| `regions`[].`country`.`id`      | The country's system id.                               |
| `regions`[].`country`.`name`    | The country's full name.                               |
| `regions`[].`created_at`        | The datetime the region was created.                   |
| `regions`[].`id`                | The region's system id.                                |
| `regions`[].`name`              | The region's full name.                                |
| `regions`[].`status`            | The status of the region.                              |
| `regions`[].`status_changed_at` | The datetime of the last time the status was changed.  |
| `regions`[].`updated_at`        | The datetime of the last time region was updated.      |
| `limit`                         | The limit of items to show on a single page.           |
| `next_uri`                      | The URI of the next page of results, if available.     |
| `page`                          | The current list page number.                          |
| `previous_uri`                  | The URI of the previous page of results, if available. |
| `total`                         | The total count of items found.                        |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/regions/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/regions/2/2", 
  "page": 1, 
  "regions": [
    {
      "code_2": "CA", 
      "country": {
        "code_2": "US", 
        "code_3": "USA", 
        "id": 1, 
        "name": "United States"
      }, 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "name": "California", 
      "status": 1, 
      "status_changed_at": "2018-01-01T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000"
    }, 
    {
      "code_2": "OR", 
      "country": {
        "code_2": "US", 
        "code_3": "USA", 
        "id": 1, 
        "name": "United States"
      }, 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "name": "Oregon", 
      "status": 1, 
      "status_changed_at": "2018-01-01T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000"
    }
  ], 
  "total": 6
}
```

<br><br>

## Logins

### List Logins

Use the following to read a list of logins.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Paths           | /logins<br>/logins/{page}<br>/logins/{page}/{limit}                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 25                                                                                                                                                                                                                                                                                                                                                         |
| URL Parameters  | - `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'attempt_date.asc', 'attempt_date.desc']; Default: 'id.asc'<br>- `user_id`: Integer; Optional; The ID of the user to filter results by<br>- `username`: String; Optional; The username to filter results by<br>- `ip_address`: String; Optional; The IP address to filter results by<br>- `ip_address`: Integer; Optional; The API code to filter results by; Values: [1 (admin), 2 (public)] |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no logins on this page.                  |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                       | Value                                                  |
| ------------------------- | ------------------------------------------------------ | 
| `limit`                   | The limit of items to show on a single page.           |
| `logins`                  | The top-level login list resource.                     | 
| `logins`[].`attempt_date` | The datetime the login attempt was made.               |
| `logins`[].`created_at`   | The datetime the login was created.                    |
| `logins`[].`id`           | The login's system id.                                 |
| `logins`[].`ip_address`   | The IP address for the login attempt.                  |
| `logins`[].`api`          | The API code for which API access was attempted for.   |
| `logins`[].`success`      | 'true' if the login was successful, 'false' otherwise. |
| `logins`[].`updated_at`   | The datetime of the last time login was updated.       |
| `logins`[].`user_id`      | The user ID for the attempted username, if available.  |
| `logins`[].`username`     | The username the login attempt used.                   |
| `next_uri`                | The URI of the next page of results, if available.     |
| `page`                    | The current list page number.                          |
| `previous_uri`            | The URI of the previous page of results, if available. |
| `total`                   | The total count of items found.                        |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/logins/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "logins": [
    {
      "api": 1,
      "attempt_date": "2018-12-01T08:32:55+0000",
      "created_at": "2019-11-07T02:49:26+0000",
      "id": 1,
      "ip_address": "1.1.1.1",
      "success": true,
      "updated_at": "2019-11-07T02:49:26+0000",
      "user_id": 1,
      "username": "admin1"
    },
    {
      "api": 1,
      "attempt_date": "2018-12-02T12:02:21+0000",
      "created_at": "2019-11-07T02:49:26+0000",
      "id": 2,
      "ip_address": "1.1.1.1",
      "success": false,
      "updated_at": "2019-11-07T02:49:26+0000",
      "user_id": 1,
      "username": "admin1"
    }
  ], 
  "next_uri": "https://api.admin.domain.com/v/1.0/logins/2/2", 
  "page": 1, 
  "total": 13
}
```

<br><br>

## Password Reset Requests

### List Password Reset Requests

Use the following to read a list of password reset requests.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Method          | GET                                                                                                                                                                                                                                                                                                    |
| Paths           | /password_resets<br>/password_resets/{page}<br>/password_resets/{page}/{limit}                                                                                                                                                                                                                         |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                                                              |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'requested_at.asc', 'requested_at.desc']; Default: 'id.asc'<br>- `user_id`: Integer; Optional; The ID of the user to filter results by |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no password reset requests on this page. |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                   | Value                                                          |
| ------------------------------------- | -------------------------------------------------------------- | 
| `limit`                               | The limit of items to show on a single page.                   |
| `next_uri`                            | The URI of the next page of results, if available.             |
| `page`                                | The current list page number.                                  |
| `password_resets`                     | The top-level password reset list resource.                    | 
| `password_resets`[].`code`            | The one-time code for the password reset.                      |
| `password_resets`[].`created_at`      | The datetime the password reset was created.                   |
| `password_resets`[].`id`              | The password reset's system id.                                |
| `password_resets`[].`ip_address`      | The IP address the password reset was made from.               |
| `password_resets`[].`is_used`         | 'true' if the password reset has been used, 'false' otherwise. |
| `password_resets`[].`requested_at`    | The datetime the password reset was requested.                 |
| `password_resets`[].`updated_at`      | The datetime of the last time login was updated.               |
| `password_resets`[].`user`            | The user object for the user who made the request.             |
| `password_resets`[].`user`.`id`       | The user's system ID.                                          |
| `password_resets`[].`user`.`uri`      | The user's resource URI.                                       |
| `password_resets`[].`user`.`username` | The user's username.                                           |
| `previous_uri`                        | The URI of the previous page of results, if available.         |
| `total`                               | The total count of items found.                                |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/password_resets/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "https://api.admin.domain.com/v/1.0/password_resets/2/2", 
  "page": 1, 
  "password_resets": [
    {
      "code": "HD7SF2", 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "ip_address": "1.1.1.1", 
      "is_used": true, 
      "requested_at": "2019-01-10T07:13:49+0000", 
      "status": 1, 
      "status_changed_at": "2019-01-10T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user": {
        "id": 1, 
        "uri": "https://api.admin.domain.com/v/1.0/user/1", 
        "username": "user1"
      }
    }, 
    {
      "code": "M5AF8G", 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "ip_address": "1.1.1.2", 
      "is_used": true, 
      "requested_at": "2019-01-12T14:02:51+0000", 
      "status": 1, 
      "status_changed_at": "2019-01-12T00:00:00+0000", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user": {
        "id": 2, 
        "uri": "https://api.admin.domain.com/v/1.0/user/2", 
        "username": "user2"
      }
    }
  ], 
  "total": 7
}
```

<br><br>

## Notifications

### List Notifications

Use the following to read a list of notifications.

##### Request

| HTTP            | Value                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Method          | GET                                                                                                                                                                                                                                                                                                                                                                                                 |
| Paths           | /notifications<br>/notifications/{page}<br>/notifications/{page}/{limit}                                                                                                                                                                                                                                                                                                                            |
| Path Parameters | - `page`: Integer; Results page number; Default: 1<br>- `limit`: Integer; Number of results per page to show; Default: 10                                                                                                                                                                                                                                                                           |
| URL Parameters  | - `status`: Integer; Resource status code to filter results by; Optional<br>- `order_by`: String; How to order results; Optional; Values: ['id.asc', 'id.desc', 'sent_at.asc', 'sent_at.desc']; Default: 'id.asc'<br>- `user_id`: Integer; Optional; The ID of the user to filter results by<br>- `channel`: Integer; Optional; The communication channel to filter results by; Values: [1 (email)] |

##### Response Codes
 
| Code | Description  | Notes                                              |
| ---- | ------------ | -------------------------------------------------- |
| 200  | OK           | Request successful.                                |
| 204  | No Content   | There are no notifications on this page.           |
| 500  | Server error | Generic application error. Check application logs. |

##### Response Payload

| Key                                   | Value                                                           |
| ------------------------------------- | --------------------------------------------------------------- | 
| `limit`                               | The limit of items to show on a single page.                    |
| `next_uri`                            | The URI of the next page of results, if available.              |
| `notifications`                       | The top-level notification list resource.                       | 
| `notifications`[].`accepted`          | 'true' if the notification was received by the sending service. |
| `notifications`[].`channel`           | The channel code (1 for email, etc.)                            |
| `notifications`[].`created_at`        | The datetime the notification was created.                      |
| `notifications`[].`id`                | The notification's system id.                                   |
| `notifications`[].`notification_id`   | The ID received from the sending service.                       |
| `notifications`[].`rejected`          | 'true' if the sending service rejected the notification.        |
| `notifications`[].`sent_at`           | The datetime the notification was sent.                         |
| `notifications`[].`status`            | The status of the notification.                                 |
| `notifications`[].`status_changed_at` | The datetime of the last time the status was changed.           |
| `notifications`[].`template`          | The template code used on the sending service.                  |
| `notifications`[].`updated_at`        | The datetime of the last time notification was updated.         |
| `notifications`[].`user`              | The user object for the user who was notified.                  |
| `notifications`[].`user`.`id`         | The user's system ID.                                           |
| `notifications`[].`user`.`uri`        | The user's resource URI.                                        |
| `notifications`[].`user`.`username`   | The user's username.                                            |
| `page`                                | The current list page number.                                   |
| `previous_uri`                        | The URI of the previous page of results, if available.          |
| `total`                               | The total count of items found.                                 |

##### Example

###### Request

```ssh
curl https://api.admin.domain.com/v/1.0/notifications/1/2?app_key=y84pSJ7PA4E9Lnj936ptdqj9jmGCmtTx \
    -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3MjQ3NDcyNywiZXhwIjoxNTcyNDg5MTI3fQ.eyJpZCI6MSwidHlwZSI6ImFkbWluaXN0cmF0b3IifQ.5dkEEbWNMxtHxS_nuk-m0zIY37jlmBHBREB9gKHwLWXIN-ic6EdXxhhIvEFZJYnR3rnNsIlZjTBLOMb21dMwtg:
```

###### Response

```json
{
  "limit": 2, 
  "next_uri": "http://base.api.admin.python.vm/v/dev/notifications/2/2", 
  "notifications": [
    {
      "accepted": 1, 
      "channel": 1, 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 1, 
      "notification_id": "123456", 
      "rejected": 0, 
      "sent_at": "2019-02-01T10:45:00+0000", 
      "service": "Service 1", 
      "status": 1, 
      "status_changed_at": "2019-02-01T00:00:00+0000", 
      "template": "template-1", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user": {
        "id": 1, 
        "uri": "http://base.api.admin.python.vm/v/dev/user/1", 
        "username": "user1"
      }
    }, 
    {
      "accepted": 1, 
      "channel": 1, 
      "created_at": "2019-11-05T02:16:56+0000", 
      "id": 2, 
      "notification_id": "123457", 
      "rejected": 0, 
      "sent_at": "2019-02-03T12:10:07+0000", 
      "service": "Service 1", 
      "status": 1, 
      "status_changed_at": "2019-02-03T00:00:00+0000", 
      "template": "template-1", 
      "updated_at": "2019-11-05T02:16:56+0000", 
      "user": {
        "id": 2, 
        "uri": "http://base.api.admin.python.vm/v/dev/user/2", 
        "username": "user2"
      }
    }
  ], 
  "page": 1, 
  "total": 5
}
```
