# /api/upload/device

Endpoint to upload device level targets and the corresponding images

## Request
Method: POST

### Form parameters
- before_target: _uploaded target file_
- after_target: _uploaded target file_
- images: _uploaded images_

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
