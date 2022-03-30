# /api/analyze/iqx

Endpoint for performing an anlysis on two targets.
Targets are referred to as _before_ and _after_ target,
as that is the usecase the endpoint is modeled after.


## Request

Method: POST


## Query Parameters

?target={:target_name}


## Request
=== "POST"
    Multipart form
    
    Fields:
    ```
    before_target: FILE
    ```
    ```
    after_target : FILE
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
        "error":  "before_target not specified"
    }
    ```
