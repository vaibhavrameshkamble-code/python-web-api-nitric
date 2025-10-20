from nitric.resources import api, kv
from nitric.application import Nitric
from nitric.context import HttpContext
from uuid import uuid4
import json

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
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
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


# Start the Nitric application
Nitric.run()
