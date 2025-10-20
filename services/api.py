from nitric.resources import api, kv
from nitric.application import Nitric
from nitric.context import HttpContext
from uuid import uuid4
import json

# OpenAPI 3.0 Specification
OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Nitric Python Web API",
        "version": "1.0.0",
        "description": "A REST API example with CRUD operations for task management built with Nitric framework",
        "contact": {
            "name": "API Support"
        }
    },
    "servers": [
        {
            "url": "http://localhost:4001",
            "description": "Local development server"
        }
    ],
    "paths": {
        "/": {
            "get": {
                "summary": "API information",
                "description": "Welcome endpoint with API information and available endpoints",
                "tags": ["General"],
                "responses": {
                    "200": {
                        "description": "API information",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"},
                                        "version": {"type": "string"},
                                        "description": {"type": "string"},
                                        "endpoints": {"type": "object"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/health": {
            "get": {
                "summary": "Health check",
                "description": "Health check endpoint to verify the API is running",
                "tags": ["General"],
                "responses": {
                    "200": {
                        "description": "API is healthy",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "healthy"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "/tasks": {
            "get": {
                "summary": "Get all tasks",
                "description": "Retrieve all tasks from the key-value store",
                "tags": ["Tasks"],
                "responses": {
                    "200": {
                        "description": "List of all tasks",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "count": {"type": "integer"},
                                        "tasks": {
                                            "type": "array",
                                            "items": {"$ref": "#/components/schemas/Task"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            },
            "post": {
                "summary": "Create a new task",
                "description": "Create a new task with title, description, and completion status",
                "tags": ["Tasks"],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TaskInput"},
                            "example": {
                                "title": "Learn Nitric",
                                "description": "Complete the Nitric tutorial",
                                "completed": False
                            }
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": "Task created successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "message": {"type": "string"},
                                        "task": {"$ref": "#/components/schemas/Task"}
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request - missing required fields",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    },
                    "500": {
                        "description": "Server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        },
        "/tasks/{id}": {
            "get": {
                "summary": "Get a specific task",
                "description": "Retrieve a specific task by its ID",
                "tags": ["Tasks"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "Task ID",
                        "schema": {"type": "string", "format": "uuid"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task details",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "task": {"$ref": "#/components/schemas/Task"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Task not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    },
                    "500": {
                        "description": "Server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            },
            "put": {
                "summary": "Update a task",
                "description": "Update an existing task by ID",
                "tags": ["Tasks"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "Task ID",
                        "schema": {"type": "string", "format": "uuid"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/TaskUpdate"},
                            "example": {
                                "title": "Learn Nitric - Updated",
                                "completed": True
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Task updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "message": {"type": "string"},
                                        "task": {"$ref": "#/components/schemas/Task"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Task not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    },
                    "500": {
                        "description": "Server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            },
            "delete": {
                "summary": "Delete a task",
                "description": "Delete a task by ID",
                "tags": ["Tasks"],
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": "Task ID",
                        "schema": {"type": "string", "format": "uuid"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task deleted successfully",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "success": {"type": "boolean"},
                                        "message": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Task not found",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    },
                    "500": {
                        "description": "Server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "Task": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid", "description": "Unique task identifier"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "completed": {"type": "boolean", "description": "Task completion status"},
                    "created_at": {"type": "string", "description": "Creation timestamp"},
                    "updated_at": {"type": "string", "description": "Last update timestamp"}
                },
                "required": ["id", "title"]
            },
            "TaskInput": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "completed": {"type": "boolean", "description": "Task completion status", "default": False},
                    "created_at": {"type": "string", "description": "Creation timestamp"}
                },
                "required": ["title"]
            },
            "TaskUpdate": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "completed": {"type": "boolean", "description": "Task completion status"},
                    "updated_at": {"type": "string", "description": "Last update timestamp"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": False},
                    "error": {"type": "string", "description": "Error message"}
                }
            }
        }
    },
    "tags": [
        {
            "name": "General",
            "description": "General API endpoints"
        },
        {
            "name": "Tasks",
            "description": "Task management operations"
        }
    ]
}

# Create an API named "main"
main_api = api("main")

# Create a key-value store for tasks
tasks_store = kv("tasks").allow("get", "set", "delete")

# Health check endpoint
@main_api.get("/health")
async def health_check(ctx: HttpContext):
    """Health check endpoint to verify the API is running"""
    ctx.res.body = {
        "status": "healthy",
        "message": "API is running successfully"
    }


# Welcome endpoint
@main_api.get("/")
async def welcome(ctx: HttpContext):
    """Welcome endpoint with API information"""
    ctx.res.body = {
        "message": "Welcome to Nitric Python Web API",
        "version": "1.0.0",
        "description": "A REST API example with CRUD operations for task management",
        "documentation": {
            "swagger_ui": "/docs",
            "openapi_spec": "/swagger.json"
        },
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /docs": "Swagger UI documentation",
            "GET /swagger.json": "OpenAPI specification",
            "GET /tasks": "Get all tasks",
            "GET /tasks/:id": "Get a specific task by ID",
            "POST /tasks": "Create a new task",
            "PUT /tasks/:id": "Update a task by ID",
            "DELETE /tasks/:id": "Delete a task by ID"
        }
    }


# Get all tasks
@main_api.get("/tasks")
async def get_all_tasks(ctx: HttpContext):
    """Retrieve all tasks from the key-value store"""
    try:
        # Get all keys from the store
        keys = await tasks_store.keys()
        tasks = []
        
        # Retrieve each task
        for key in keys:
            task = await tasks_store.get(key)
            if task:
                tasks.append({
                    "id": key,
                    **task
                })
        
        ctx.res.body = {
            "success": True,
            "count": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        ctx.res.status = 500
        ctx.res.body = {
            "success": False,
            "error": f"Failed to retrieve tasks: {str(e)}"
        }


# Get a specific task by ID
@main_api.get("/tasks/:id")
async def get_task(ctx: HttpContext):
    """Retrieve a specific task by its ID"""
    task_id = ctx.req.params.get("id")
    
    if not task_id:
        ctx.res.status = 400
        ctx.res.body = {
            "success": False,
            "error": "Task ID is required"
        }
        return
    
    try:
        task = await tasks_store.get(task_id)
        
        if not task:
            ctx.res.status = 404
            ctx.res.body = {
                "success": False,
                "error": f"Task with ID '{task_id}' not found"
            }
            return
        
        ctx.res.body = {
            "success": True,
            "task": {
                "id": task_id,
                **task
            }
        }
    except Exception as e:
        ctx.res.status = 500
        ctx.res.body = {
            "success": False,
            "error": f"Failed to retrieve task: {str(e)}"
        }


# Create a new task
@main_api.post("/tasks")
async def create_task(ctx: HttpContext):
    """Create a new task"""
    try:
        # Parse request body
        data = ctx.req.json
        
        # Validate required fields
        if not data or "title" not in data:
            ctx.res.status = 400
            ctx.res.body = {
                "success": False,
                "error": "Task title is required"
            }
            return
        
        # Generate a unique ID
        task_id = str(uuid4())
        
        # Create task object
        task = {
            "title": data["title"],
            "description": data.get("description", ""),
            "completed": data.get("completed", False),
            "created_at": data.get("created_at", "")
        }
        
        # Save to store
        await tasks_store.set(task_id, task)
        
        ctx.res.status = 201
        ctx.res.body = {
            "success": True,
            "message": f"Task created successfully",
            "task": {
                "id": task_id,
                **task
            }
        }
    except Exception as e:
        ctx.res.status = 500
        ctx.res.body = {
            "success": False,
            "error": f"Failed to create task: {str(e)}"
        }


# Update a task
@main_api.put("/tasks/:id")
async def update_task(ctx: HttpContext):
    """Update an existing task by ID"""
    task_id = ctx.req.params.get("id")
    
    if not task_id:
        ctx.res.status = 400
        ctx.res.body = {
            "success": False,
            "error": "Task ID is required"
        }
        return
    
    try:
        # Check if task exists
        existing_task = await tasks_store.get(task_id)
        
        if not existing_task:
            ctx.res.status = 404
            ctx.res.body = {
                "success": False,
                "error": f"Task with ID '{task_id}' not found"
            }
            return
        
        # Parse request body
        data = ctx.req.json
        
        if not data:
            ctx.res.status = 400
            ctx.res.body = {
                "success": False,
                "error": "Request body is required"
            }
            return
        
        # Update task fields
        updated_task = {
            "title": data.get("title", existing_task.get("title")),
            "description": data.get("description", existing_task.get("description")),
            "completed": data.get("completed", existing_task.get("completed")),
            "created_at": existing_task.get("created_at", ""),
            "updated_at": data.get("updated_at", "")
        }
        
        # Save updated task
        await tasks_store.set(task_id, updated_task)
        
        ctx.res.body = {
            "success": True,
            "message": "Task updated successfully",
            "task": {
                "id": task_id,
                **updated_task
            }
        }
    except Exception as e:
        ctx.res.status = 500
        ctx.res.body = {
            "success": False,
            "error": f"Failed to update task: {str(e)}"
        }


# Delete a task
@main_api.delete("/tasks/:id")
async def delete_task(ctx: HttpContext):
    """Delete a task by ID"""
    task_id = ctx.req.params.get("id")
    
    if not task_id:
        ctx.res.status = 400
        ctx.res.body = {
            "success": False,
            "error": "Task ID is required"
        }
        return
    
    try:
        # Check if task exists
        existing_task = await tasks_store.get(task_id)
        
        if not existing_task:
            ctx.res.status = 404
            ctx.res.body = {
                "success": False,
                "error": f"Task with ID '{task_id}' not found"
            }
            return
        
        # Delete the task
        await tasks_store.delete(task_id)
        
        ctx.res.body = {
            "success": True,
            "message": f"Task with ID '{task_id}' deleted successfully"
        }
    except Exception as e:
        ctx.res.status = 500
        ctx.res.body = {
            "success": False,
            "error": f"Failed to delete task: {str(e)}"
        }


# Swagger/OpenAPI endpoints
@main_api.get("/swagger.json")
async def swagger_spec(ctx: HttpContext):
    """Serve the OpenAPI specification as JSON"""
    ctx.res.headers["Content-Type"] = "application/json"
    ctx.res.body = OPENAPI_SPEC


@main_api.get("/docs")
async def swagger_ui(ctx: HttpContext):
    """Serve Swagger UI for interactive API documentation"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Nitric Python Web API - Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui.css">
        <link rel="icon" type="image/png" href="https://nitric.io/favicon.ico">
        <style>
            html {
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }
            *, *:before, *:after {
                box-sizing: inherit;
            }
            body {
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                const ui = SwaggerUIBundle({
                    url: "/swagger.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout"
                });
                window.ui = ui;
            };
        </script>
    </body>
    </html>
    """
    ctx.res.headers["Content-Type"] = "text/html"
    ctx.res.body = html_content


@main_api.get("/swagger")
async def swagger_redirect(ctx: HttpContext):
    """Redirect /swagger to /docs for convenience"""
    ctx.res.status = 301
    ctx.res.headers["Location"] = "/docs"
    ctx.res.body = ""


# Start the Nitric application
Nitric.run()
