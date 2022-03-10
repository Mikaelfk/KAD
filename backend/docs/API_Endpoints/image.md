# /api/image/{:image_id}

Endpoint that gives extensive information about an image

- Image ID
- Image Name
- ISO Score
- Analysis

## Request
Method: GET

## Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        session_id: STRING;
    }
    ```

=== "400"
    Bad Request
    ``` json linenums="1" title="JSON"
    {
        error: STRING;
    }
    ```

=== "415"
    Unsupported Media Type
    ``` json linenums="1" title="JSON"
    {
        error: STRING;
    }
    ```
