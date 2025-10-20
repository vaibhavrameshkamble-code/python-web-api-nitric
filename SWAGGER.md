# Swagger/OpenAPI Documentation

This document describes the Swagger UI and OpenAPI documentation features added to the Nitric Python Web API.

## Overview

The API now includes comprehensive Swagger/OpenAPI 3.0 documentation that provides:
- Interactive API exploration through Swagger UI
- Complete request/response schemas
- Example payloads for all endpoints
- "Try it out" functionality for testing endpoints directly from the browser

## Accessing the Documentation

### Swagger UI (Interactive Documentation)
When running the API locally:
```
http://localhost:4001/docs
```

Alternative URL:
```
http://localhost:4001/swagger
```
(This redirects to `/docs`)

### OpenAPI Specification (JSON)
```
http://localhost:4001/swagger.json
```

## Features

### 1. Complete API Documentation
All endpoints are documented with:
- Detailed descriptions
- Request parameters and body schemas
- Response schemas for success and error cases
- HTTP status codes
- Example payloads

### 2. Interactive Testing
The Swagger UI allows you to:
- Test any endpoint directly from the browser
- Fill in parameters and request bodies using forms
- See actual responses from the API
- Download the OpenAPI specification

### 3. Schema Definitions
The following schemas are documented:

#### Task
Complete task object with all fields
```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "completed": boolean,
  "created_at": "string",
  "updated_at": "string"
}
```

#### TaskInput
Schema for creating new tasks
```json
{
  "title": "string (required)",
  "description": "string",
  "completed": boolean,
  "created_at": "string"
}
```

#### TaskUpdate
Schema for updating existing tasks
```json
{
  "title": "string",
  "description": "string",
  "completed": boolean,
  "updated_at": "string"
}
```

#### Error
Error response schema
```json
{
  "success": false,
  "error": "string"
}
```

## Documented Endpoints

### General Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /swagger.json` - OpenAPI specification

### Task Management Endpoints
- `GET /tasks` - Retrieve all tasks
- `GET /tasks/{id}` - Retrieve a specific task by ID
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update an existing task
- `DELETE /tasks/{id}` - Delete a task

## HTTP Status Codes

The API uses standard HTTP status codes:
- `200 OK` - Successful GET, PUT, DELETE requests
- `201 Created` - Successful POST request
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Example Usage

### Viewing Documentation
1. Start the Nitric development server:
   ```bash
   nitric start
   ```

2. Open your browser to:
   ```
   http://localhost:4001/docs
   ```

### Using the Swagger UI
1. Navigate to an endpoint you want to test
2. Click "Try it out"
3. Fill in required parameters and request body
4. Click "Execute"
5. View the response below

### Downloading the OpenAPI Spec
You can download the OpenAPI specification for use with other tools:
```bash
curl http://localhost:4001/swagger.json > openapi.json
```

## Implementation Details

### Zero Dependencies
The implementation uses CDN-hosted Swagger UI resources, so no additional Python packages are required. The OpenAPI specification is embedded directly in the code.

### Technology Stack
- **OpenAPI Version**: 3.0.0
- **Swagger UI Version**: 5.10.5 (loaded from unpkg CDN)
- **Format**: JSON

### Customization
The OpenAPI specification is defined in the `OPENAPI_SPEC` dictionary in `services/api.py`. You can customize:
- API information (title, version, description)
- Server URLs
- Endpoint descriptions
- Schema definitions
- Example payloads

## Benefits

1. **Developer Experience**: Developers can explore and test the API interactively
2. **Documentation**: Always up-to-date documentation alongside the code
3. **API Client Generation**: The OpenAPI spec can be used to generate client SDKs
4. **Testing**: Built-in testing interface for quick API validation
5. **Standards Compliance**: Uses industry-standard OpenAPI 3.0 format

## Future Enhancements

Potential improvements:
- Add authentication/authorization documentation
- Include more detailed examples
- Add response examples for all endpoints
- Document rate limiting (if implemented)
- Add API versioning information

## Troubleshooting

### Swagger UI Not Loading
If the Swagger UI page is blank:
1. Check browser console for errors
2. Ensure internet connection is available (CDN resources required)
3. Try clearing browser cache
4. Verify the API is running at `http://localhost:4001`

### OpenAPI Spec Not Found
If `/swagger.json` returns 404:
1. Ensure the Nitric server is running
2. Check that `services/api.py` is loaded correctly
3. Look for errors in the Nitric console output

## Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [Nitric Framework Documentation](https://nitric.io/docs)
