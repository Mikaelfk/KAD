# /api/analyze/object

Endpoint for performing analysis on all images uploaded.

## Request

Method: POST

## Query Parameters

`?iqes={:iqes_name}`

`?target={:target_name}`


### Supported Parameter Values
Supported iqes values:

* OQT

Supported target values for OQT:

* GTObject
* TE263

## Request
=== "POST"
    Multipart form

    Fields:
    ```
    files: [FILE, ...]
    ```


## Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        "session_id": STRING
    }
    ```

=== "400"
    Bad request
    ``` json linenums="1" title="JSON"
    {
        "error": STRING
    }
    ```


## Sample Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
	    "session_id": "f811367b-6646-4df0-9303-ad850bb36c54"
    }
    ```

=== "400"
    Bad request
    ``` json linenums="1" title="JSON"
    {
        "error": "missing file(s). Check request"
    }
    ```