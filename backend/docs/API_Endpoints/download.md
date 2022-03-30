# /api/download/{:session_id}

Endpoint for downloading a single image or a ZIP with all images in a session.


## Request

Method: GET


## Optional Query Parameters

?file_name={:file_name}


## Response

=== "200"

    FILE

=== "404"
    Not found
    ``` json linenums="1" title="JSON"
    {
	    "error": STRING
    }
    ```


## Sample Response

=== "200"

    FILE

=== "404"
    Not found
    ``` json linenums="1" title="JSON"
    {
	    "error": "session does not exist"
    }
    ```