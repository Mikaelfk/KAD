# /api/upload/object

Endpoint to upload object level target and the corresponding images

## Request
Method: POST

### Form parameters
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
