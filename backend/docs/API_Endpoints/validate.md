# /api/validate

Endpoint for validating an image.
Accepts a form with a single file included.

## Request
Method: POST

### Form parameters
- file: _uploaded file_

## Response

=== "200"
    OK
    ``` json linenums="1" title="JSON"
    {
        isValid: BOOLEAN;
    }
    ```

=== "400"
    Bad Request
    ``` json linenums="1" title="JSON"
    {
        error: STRING;
    }
    ```
