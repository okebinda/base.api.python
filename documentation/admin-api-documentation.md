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
| `status`      | The status of the app key.                           | Required; Must be an integer        |

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
| `status`      | The status of the app key.                           | Required; Must be an integer        |

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
| `login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              | Required; Must be an integer         |
| `login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              | Required; Boolean                    |
| `login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 | Required; Must be an integer         |
| `login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   | Required; Must be an integer         |
| `name`                   | The name of the role.                                                                                             | Required; Unique; Length: 2-32 chars |
| `password_policy`        | 'true' if the password policy is enabled.                                                                         | Required; Boolean                    |
| `password_reset_days`    | Number of days a password is valid until user must change it.                                                     | Required; Must be an integer         |
| `password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            | Required; Must be an integer         |
| `priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. | Required; Must be an integer         |

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
| `login_ban_time`         | Number of seconds the lockout policy will ban further login attempts once triggered.                              | Required; Must be an integer         |
| `login_lockout_policy`   | 'true' if lockout policy is enabled.                                                                              | Required; Boolean                    |
| `login_max_attempts`     | Number of failed login attempts to allow within timeframe before locking account.                                 | Required; Must be an integer         |
| `login_timeframe`        | Window of time (in seconds) to allow max login attempts before locking account.                                   | Required; Must be an integer         |
| `name`                   | The name of the role.                                                                                             | Required; Unique; Length: 2-32 chars |
| `password_policy`        | 'true' if the password policy is enabled.                                                                         | Required; Boolean                    |
| `password_reset_days`    | Number of days a password is valid until user must change it.                                                     | Required; Must be an integer         |
| `password_reuse_history` | Number of previous passwords to disallow when a user updates password.                                            | Required; Must be an integer         |
| `priority`               | The priority (an integer, lower is higher priority) of the role, used to apply policies if more than one applies. | Required; Must be an integer         |

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
| `roles`      | List of the administrator's role IDs.    | Optional; List literal of Role IDs (integers)                                                              |
| `status`     | The status of the administrator.         | Required; Must be an integer                                                                               |
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
| `roles`      | List of the administrator's role IDs.    | Optional; List literal of Role IDs (integers)                                                              |
| `status`     | The status of the administrator.         | Required; Must be an integer                                                                               |
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
