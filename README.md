# Python Web API with Nitric.io

A production-ready Python REST API example built with the [Nitric](https://nitric.io) framework, designed for easy deployment to AWS.

## 🚀 Features

- **RESTful API**: Complete CRUD operations for task management
- **Cloud-Native**: Built with Nitric framework for seamless cloud deployment
- **AWS Ready**: Configured for easy deployment to Amazon Web Services
- **Key-Value Storage**: Uses Nitric's KV store abstraction for data persistence
- **Modern Python**: Uses Python 3.11+ with async/await patterns
- **Easy Development**: Hot-reload enabled for fast development cycles

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check endpoint |
| GET | `/docs` | **Swagger UI - Interactive API documentation** |
| GET | `/swagger.json` | OpenAPI 3.0 specification (JSON) |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/:id` | Get a specific task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/:id` | Update a task |
| DELETE | `/tasks/:id` | Delete a task |

### 📖 API Documentation

This API includes **Swagger UI** for interactive API documentation:

- **Swagger UI**: Visit `http://localhost:4001/docs` when running locally
- **OpenAPI Spec**: Available at `http://localhost:4001/swagger.json`

The Swagger UI provides:
- Interactive API exploration
- Try-it-out functionality for all endpoints
- Complete request/response schemas
- Example payloads for each endpoint

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.11+**: [Download Python](https://www.python.org/downloads/)
2. **uv**: Fast Python package installer
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Nitric CLI**: [Installation guide](https://nitric.io/docs/get-started/installation)
   ```bash
   # macOS/Linux
   curl -L https://nitric.io/install?version=latest | bash
   
   # Windows (PowerShell)
   iwr https://nitric.io/install?version=latest -useb | iex
   ```

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd python-web-api-nitric
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

## 🏃 Running Locally

Start the Nitric development server:

```bash
nitric start
```

The API will be available at `http://localhost:4001`

You'll see output showing your services connecting. The development server includes hot-reload, so changes to your code will automatically restart the service.

### 📖 Accessing API Documentation

Once the server is running, you can access the interactive Swagger documentation:

```bash
# Open in your browser
http://localhost:4001/docs
```

The Swagger UI allows you to:
- Explore all available endpoints
- View request/response schemas
- Test API endpoints directly from the browser
- Download the OpenAPI specification

## 🧪 Testing the API

### Using curl

**Get API Information**:
```bash
curl http://localhost:4001/
```

**Health Check**:
```bash
curl http://localhost:4001/health
```

**Create a Task**:
```bash
curl -X POST http://localhost:4001/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Nitric",
    "description": "Complete the Nitric tutorial",
    "completed": false
  }'
```

**Get All Tasks**:
```bash
curl http://localhost:4001/tasks
```

**Get a Specific Task**:
```bash
curl http://localhost:4001/tasks/{task-id}
```

**Update a Task**:
```bash
curl -X PUT http://localhost:4001/tasks/{task-id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Nitric - Updated",
    "completed": true
  }'
```

**Delete a Task**:
```bash
curl -X DELETE http://localhost:4001/tasks/{task-id}
```

## ☁️ Deploying to AWS

### Option 1: Automated Deployment with GitHub Actions (Recommended)

This repository includes a pre-configured GitHub Actions workflow for automated AWS deployment.

**Quick Setup:**

1. **Add AWS credentials to GitHub Secrets**:
   - Go to your repository **Settings** → **Secrets and variables** → **Actions**
   - Add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`

2. **Push to main branch**:
   ```bash
   git push origin main
   ```
   
   The deployment will start automatically!

3. **Or trigger manually**:
   - Go to **Actions** tab → **Deploy to AWS** workflow
   - Click **Run workflow**

📚 **[See detailed setup guide →](AWS_DEPLOYMENT_SETUP.md)**

### Option 2: Manual Deployment (CLI)

#### Prerequisites for Manual Deployment

1. **AWS Account**: You need an active AWS account
2. **AWS CLI**: [Install AWS CLI](https://aws.amazon.com/cli/)
3. **AWS Credentials**: Configure your AWS credentials
   ```bash
   aws configure
   ```

#### Manual Deployment Steps

1. **Build your application**:
   ```bash
   nitric build
   ```

2. **Deploy to AWS**:
   ```bash
   nitric up -s python-web-api-dev -f nitric.aws.yaml
   ```

3. **Wait for deployment**: Nitric will provision all necessary AWS resources:
   - API Gateway
   - Lambda functions
   - DynamoDB tables (for KV store)
   - IAM roles and policies
   - CloudWatch logs

4. **Access your deployed API**: Once deployment is complete, Nitric will output the API URL.

#### Update Deployment

To deploy updates to your application:

```bash
nitric up -s python-web-api-dev -f nitric.aws.yaml
```

#### Remove Deployment

To tear down the AWS resources:

```bash
nitric down -s python-web-api-dev
```

## 📁 Project Structure

```
python-web-api-nitric/
├── .github/
│   └── workflows/
│       └── deploy-aws.yml         # GitHub Actions deployment workflow
├── services/
│   └── api.py                     # Main API implementation
├── .gitignore                     # Git ignore rules
├── .python-version                # Python version specification
├── AWS_DEPLOYMENT_SETUP.md        # Detailed AWS deployment guide
├── DEPLOYMENT.md                  # General deployment documentation
├── nitric.yaml                    # Nitric project configuration
├── nitric.aws.yaml                # AWS stack configuration
├── pyproject.toml                 # Python project configuration
├── python.dockerfile              # Docker configuration for deployment
├── python.dockerfile.dockerignore
├── README.md                      # This file
└── requirements.txt               # Python dependencies
```

## 🔑 Key Concepts

### Nitric Resources

- **API**: HTTP API gateway that routes requests to your handlers
- **KV Store**: Key-value store for persistent data (maps to DynamoDB on AWS)

### Code Structure

The main API is defined in `services/api.py`:

```python
from nitric.resources import api, kv
from nitric.application import Nitric

# Define API and storage
main_api = api("main")
tasks_store = kv("tasks").allow("get", "set", "delete")

# Define route handlers
@main_api.get("/tasks")
async def get_tasks(ctx):
    # Handler logic
    pass

# Start the application
Nitric.run()
```

## 🔒 Security Considerations

- Nitric automatically handles IAM permissions for AWS resources
- API Gateway provides built-in DDoS protection
- Consider adding authentication/authorization for production use
- Review AWS security best practices

## 📚 Learn More

- [Nitric Documentation](https://nitric.io/docs)
- [Nitric Python Guide](https://nitric.io/docs/guides?langs=python)
- [Nitric Examples](https://github.com/nitrictech/examples)
- [Join Nitric Discord](https://nitric.io/chat)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

### Issue: "nitric: command not found"
- Make sure the Nitric CLI is installed and in your PATH
- Try restarting your terminal after installation

### Issue: "uv: command not found"
- Install uv using the installation command in Prerequisites
- Restart your terminal

### Issue: AWS deployment fails
- Verify AWS credentials are configured: `aws sts get-caller-identity`
- Check you have sufficient AWS permissions
- Review CloudWatch logs for detailed error messages

## 💡 Tips

- Use `nitric start` during development for hot-reload
- Check Nitric dashboard at `http://localhost:49152` when running locally
- Use `nitric doctor` to diagnose common issues
- Keep your Nitric CLI updated: `nitric update`

---

Built with ❤️ using [Nitric](https://nitric.io)
