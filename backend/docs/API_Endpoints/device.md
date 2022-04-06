# /api/analyze/device

Endpoint for performing an anlysis on two targets.
Targets are referred to as _before target_ and _after target_,
as that is the usecase the endpoint is modeled after.


## Request

Method: POST


## Query Parameters

`?iqes={:iqes_name}`

`?target={:target_name}`


### Supported Parameter Values
Supported iqes values:

* OQT
* IQX

Supported target values for OQT:

* GTDevice
* UTT

Supported target values for IQX:

* UTT


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
