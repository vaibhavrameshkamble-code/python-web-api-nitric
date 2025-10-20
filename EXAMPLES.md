# Example API Usage with Python

This document shows how to interact with the API using Python's `requests` library.

## Installation

```bash
pip install requests
```

## Example Code

```python
import requests
import json

# Base URL (change this to your deployed URL when on AWS)
BASE_URL = "http://localhost:4001"

def main():
    print("=" * 50)
    print("Python Web API - Nitric Example")
    print("=" * 50)
    
    # 1. Check API health
    print("\n1. Health Check:")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # 2. Get API info
    print("\n2. API Information:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Create a new task
    print("\n3. Creating a new task:")
    new_task = {
        "title": "Learn Nitric Framework",
        "description": "Complete the Nitric tutorial and deploy to AWS",
        "completed": False
    }
    response = requests.post(
        f"{BASE_URL}/tasks",
        json=new_task,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    task_data = response.json()
    print(f"Response: {json.dumps(task_data, indent=2)}")
    
    # Get the created task ID
    if task_data.get("success"):
        task_id = task_data["task"]["id"]
        
        # 4. Get the specific task
        print(f"\n4. Getting task by ID ({task_id}):")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 5. Update the task
        print(f"\n5. Updating task ({task_id}):")
        update_data = {
            "title": "Learn Nitric Framework - In Progress",
            "completed": True
        }
        response = requests.put(
            f"{BASE_URL}/tasks/{task_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 6. Get all tasks
        print("\n6. Getting all tasks:")
        response = requests.get(f"{BASE_URL}/tasks")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 7. Delete the task
        print(f"\n7. Deleting task ({task_id}):")
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # 8. Verify deletion
        print("\n8. Verifying deletion:")
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 50)
    print("Example completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

## Running the Example

1. Make sure the API is running:
   ```bash
   nitric start
   ```

2. In another terminal, run the example:
   ```bash
   python examples/api_usage_example.py
   ```

## Expected Output

```
==================================================
Python Web API - Nitric Example
==================================================

1. Health Check:
Status: 200
Response: {'status': 'healthy', 'message': 'API is running successfully'}

2. API Information:
Response: {
  "message": "Welcome to Nitric Python Web API",
  "version": "1.0.0",
  ...
}

3. Creating a new task:
Status: 201
Response: {
  "success": true,
  "message": "Task created successfully",
  "task": {
    "id": "abc-123-def",
    "title": "Learn Nitric Framework",
    ...
  }
}

...
==================================================
Example completed!
==================================================
```
