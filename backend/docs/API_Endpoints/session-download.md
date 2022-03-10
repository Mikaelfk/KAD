# /api/download/{:session_id}{?image_id={:image_id}}

Endpoint to download images from a session.

## Request
Method: GET

## Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        status: STRING;
    }
    ```

=== "400"
    Bad Request
    ``` json linenums="1" title="JSON"
    {
        error: STRING;
    }
    ```

=== "404"
    Not Found
    ``` json linenums="1" title="JSON"
    {
        error: STRING;
    }
    ```
