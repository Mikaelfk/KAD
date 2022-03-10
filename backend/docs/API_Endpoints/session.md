# /api/session/{:session_id}

Endpoint that gives some information about the images from a session.

- Image ID
- Image Name
- ISO Score

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
    Bad Reqest
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
