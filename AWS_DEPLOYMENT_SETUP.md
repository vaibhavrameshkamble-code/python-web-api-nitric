# AWS Deployment Setup Guide

This guide explains how to set up and use the AWS deployment pipeline for the Python Web API using GitHub Actions and Nitric.

## 📋 Overview

The deployment pipeline consists of two main files:
1. **`nitric.aws.yaml`** - Nitric stack configuration for AWS
2. **`.github/workflows/deploy-aws.yml`** - GitHub Actions workflow for automated deployment

## 🚀 Quick Start

### Prerequisites

Before setting up the deployment pipeline, ensure you have:

1. **AWS Account** with appropriate permissions
2. **GitHub Repository** with this code
3. **AWS Credentials** (Access Key ID and Secret Access Key)

### Step 1: Configure AWS Credentials in GitHub

You need to add your AWS credentials as GitHub Secrets:

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key ID
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

#### Getting AWS Credentials

If you don't have AWS credentials yet:

1. Log in to [AWS Console](https://console.aws.amazon.com/)
2. Go to **IAM** → **Users**
3. Select your user or create a new one
4. Go to **Security credentials** tab
5. Click **Create access key**
6. Choose **Command Line Interface (CLI)** as the use case
7. Download and save your credentials securely

#### Required AWS Permissions

The IAM user/role needs permissions for:
- Lambda (create, update, delete functions)
- API Gateway (create, configure, delete APIs)
- DynamoDB (create, configure, delete tables)
- CloudFormation (create, update, delete stacks)
- IAM (create, manage roles for Lambda)
- S3 (upload deployment artifacts)
- CloudWatch (create log groups)

You can use the following managed policies:
- `AWSLambda_FullAccess`
- `AmazonAPIGatewayAdministrator`
- `AmazonDynamoDBFullAccess`
- `CloudWatchLogsFullAccess`
- `AWSCloudFormationFullAccess`
- `IAMFullAccess` (or a more restrictive custom policy)

### Step 2: Configure Deployment Settings

#### Option A: Use Default Settings

The workflow is pre-configured with sensible defaults:
- **Region**: `us-east-1`
- **Stack Name**: `python-web-api-prod`
- **Nitric Version**: `latest`

#### Option B: Customize Settings

Edit `.github/workflows/deploy-aws.yml`:

```yaml
env:
  AWS_REGION: us-west-2           # Change to your preferred region
  STACK_NAME: my-custom-stack     # Change to your desired stack name
  NITRIC_VERSION: latest          # Or specify a version like "1.2.0"
```

Edit `nitric.aws.yaml` to customize AWS resources:

```yaml
# Change the deployment region
region: us-west-2

# Uncomment and configure Lambda settings
config:
  default-timeout: 30       # Lambda timeout in seconds
  default-memory: 512       # Lambda memory in MB

# Uncomment to add resource tags
tags:
  Environment: production
  Project: python-web-api
```

### Step 3: Deploy to AWS

#### Automatic Deployment

The workflow automatically deploys when you push to the `main` branch:

```bash
git checkout main
git merge your-feature-branch
git push origin main
```

This will trigger the deployment workflow automatically.

#### Manual Deployment

You can also trigger deployment manually:

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select **Deploy to AWS** workflow
4. Click **Run workflow**
5. (Optional) Enter a custom stack name
6. Click **Run workflow**

## 🔧 Configuration Files Explained

### nitric.aws.yaml

This file defines how your application is deployed to AWS:

```yaml
# Provider and version
provider: nitric/aws@1.1.0

# AWS region
region: us-east-1

# All other settings are commented out with examples
# Uncomment and modify as needed
```

**Common Customizations:**

1. **Change Region:**
   ```yaml
   region: us-west-2
   ```

2. **Adjust Lambda Settings:**
   ```yaml
   config:
     default-timeout: 30
     default-memory: 512
   ```

3. **Enable CloudWatch Logging:**
   ```yaml
   config:
     log-retention-days: 7
   ```

4. **Add Resource Tags:**
   ```yaml
   tags:
     Environment: production
     CostCenter: engineering
   ```

### .github/workflows/deploy-aws.yml

This GitHub Actions workflow automates the deployment process:

**Workflow Triggers:**
- Push to `main` branch
- Manual trigger via workflow_dispatch

**Workflow Steps:**
1. Checkout code
2. Set up Python 3.11
3. Install uv package manager
4. Install Python dependencies
5. Install Nitric CLI
6. Configure AWS credentials
7. Verify AWS access
8. Build the application
9. Deploy to AWS
10. Run smoke tests
11. Send notifications

**Customizing the Workflow:**

1. **Change Python Version:**
   ```yaml
   - name: Set up Python
     uses: actions/setup-python@v5
     with:
       python-version: '3.12'  # Change version
   ```

2. **Deploy to Different Branches:**
   ```yaml
   on:
     push:
       branches:
         - main
         - staging  # Add more branches
   ```

3. **Add Environment-Specific Deployments:**
   ```yaml
   strategy:
     matrix:
       environment: [dev, staging, prod]
   env:
     STACK_NAME: python-web-api-${{ matrix.environment }}
   ```

## 🔐 Security Best Practices

### Option 1: AWS Access Keys (Current Setup)

✅ **Pros:**
- Simple to set up
- Works immediately

⚠️ **Cons:**
- Less secure
- Credentials can expire
- Manual rotation required

### Option 2: OIDC (Recommended for Production)

OIDC (OpenID Connect) allows GitHub Actions to authenticate with AWS without storing long-lived credentials.

**Setup Steps:**

1. **Create an OIDC Provider in AWS:**
   - Go to IAM → Identity providers
   - Click "Add provider"
   - Provider type: OpenID Connect
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

2. **Create an IAM Role:**
   - Create a role for Web Identity
   - Choose the OIDC provider you created
   - Attach necessary permissions
   - Add trust policy:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
         },
         "Action": "sts:AssumeRoleWithWebIdentity",
         "Condition": {
           "StringEquals": {
             "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
             "token.actions.githubusercontent.com:sub": "repo:YOUR_GITHUB_ORG/YOUR_REPO:ref:refs/heads/main"
           }
         }
       }
     ]
   }
   ```

3. **Update GitHub Workflow:**
   - Add the role ARN as a secret: `AWS_ROLE_ARN`
   - In `.github/workflows/deploy-aws.yml`, replace the AWS credentials step:
   ```yaml
   - name: Configure AWS credentials via OIDC
     uses: aws-actions/configure-aws-credentials@v4
     with:
       role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
       aws-region: ${{ env.AWS_REGION }}
   ```

## 🧪 Testing the Deployment

### Local Testing (Before Pushing)

Test your configuration locally:

```bash
# Install dependencies
uv sync

# Build the application
nitric build

# Deploy to AWS (will prompt for confirmation)
nitric up -s my-test-stack -f nitric.aws.yaml
```

### Verify Deployment in GitHub Actions

1. Go to **Actions** tab in your repository
2. Find the "Deploy to AWS" workflow run
3. Click on it to see detailed logs
4. Check each step for success/failure

### Test the Deployed API

Once deployed, test your API:

```bash
# Get the API URL from the deployment output
export API_URL="https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com"

# Test health endpoint
curl $API_URL/health

# Test create task
curl -X POST $API_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Testing deployment"}'

# Test get all tasks
curl $API_URL/tasks
```

## 📊 Monitoring and Logs

### View Logs in AWS Console

1. Go to [CloudWatch Console](https://console.aws.amazon.com/cloudwatch/)
2. Navigate to **Logs** → **Log groups**
3. Find your Lambda function logs (e.g., `/aws/lambda/python-web-api-prod-main`)
4. Click to view real-time logs

### View Logs via AWS CLI

```bash
# List log groups
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/python-web-api"

# Tail logs in real-time
aws logs tail /aws/lambda/python-web-api-prod-main --follow

# Get recent logs
aws logs tail /aws/lambda/python-web-api-prod-main --since 1h
```

### View Deployment Status

```bash
# Using Nitric CLI
nitric status -s python-web-api-prod

# Using AWS CLI
aws cloudformation describe-stacks \
  --stack-name python-web-api-prod \
  --region us-east-1
```

## 💰 Cost Management

### Estimated Costs

For a low-traffic application:
- **Lambda**: ~$0.20 per 1M requests
- **API Gateway**: ~$1.00 per 1M requests  
- **DynamoDB**: ~$0.25 per GB/month
- **CloudWatch Logs**: ~$0.50 per GB ingested

**Total**: ~$2-10/month for typical development/staging environments

### AWS Free Tier (First 12 Months)

- Lambda: 1M free requests/month
- API Gateway: 1M free API calls/month
- DynamoDB: 25GB storage + 25 RCU/WCU
- CloudWatch: 5GB log ingestion

### Cost Optimization Tips

1. **Set CloudWatch log retention:**
   ```yaml
   config:
     log-retention-days: 7  # Instead of indefinite
   ```

2. **Use DynamoDB on-demand pricing:**
   ```yaml
   kvs:
     tasks:
       billing-mode: PAY_PER_REQUEST
   ```

3. **Remove unused stacks:**
   ```bash
   nitric down -s old-stack-name
   ```

4. **Set up billing alerts in AWS**

## 🔄 Multiple Environments

Deploy to different environments (dev, staging, prod):

### Method 1: Different Stack Names

```yaml
# In workflow file, use matrix strategy
strategy:
  matrix:
    environment: [dev, staging, prod]
env:
  STACK_NAME: python-web-api-${{ matrix.environment }}
```

### Method 2: Different Branches

```yaml
# Deploy dev on push to develop branch
on:
  push:
    branches:
      - develop  # → deploys to dev stack
      - main     # → deploys to prod stack
```

### Method 3: Manual Selection

Use workflow_dispatch with input parameter (already configured):

```yaml
workflow_dispatch:
  inputs:
    stack_name:
      description: 'Stack name for deployment'
      required: false
      default: 'python-web-api-prod'
```

## 🛠️ Troubleshooting

### Issue: Workflow Fails at AWS Credentials Step

**Solution:**
- Verify AWS credentials are correctly set in GitHub Secrets
- Check credential names match exactly: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- Test credentials locally: `aws sts get-caller-identity`

### Issue: Insufficient IAM Permissions

**Solution:**
- Review the IAM policy attached to your user/role
- Ensure all required services are permitted
- Check CloudFormation events in AWS Console for specific permission errors

### Issue: Nitric CLI Installation Fails

**Solution:**
- Check Nitric version availability
- Try pinning to a specific version instead of `latest`
- Review Nitric installation logs in GitHub Actions

### Issue: Deployment Timeout

**Solution:**
- Increase workflow timeout (default is 360 minutes)
- Check CloudFormation events for stuck resources
- Verify network connectivity to AWS

### Issue: API Returns 502 Bad Gateway

**Solution:**
- Check Lambda function logs in CloudWatch
- Verify Python dependencies are correctly installed
- Check Lambda timeout settings in `nitric.aws.yaml`
- Test the function locally first

### Issue: High AWS Costs

**Solution:**
- Check CloudWatch metrics for unexpected traffic
- Review DynamoDB read/write capacity
- Set up AWS Budgets and billing alerts
- Consider implementing API throttling

## 📚 Additional Resources

- [Nitric Documentation](https://nitric.io/docs)
- [Nitric AWS Provider](https://nitric.io/docs/reference/providers/aws)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)

## 🆘 Getting Help

- **Nitric Discord**: https://nitric.io/chat
- **GitHub Issues**: Create an issue in this repository
- **AWS Support**: https://aws.amazon.com/support/

## 📝 Next Steps

After setting up the deployment pipeline:

1. ✅ Configure AWS credentials in GitHub Secrets
2. ✅ Test manual deployment via GitHub Actions
3. ✅ Verify the deployed API works correctly
4. ✅ Set up monitoring and alerts
5. ✅ Configure custom domain (optional)
6. ✅ Implement CI tests before deployment (optional)
7. ✅ Set up multiple environments (optional)
8. ✅ Enable OIDC authentication (recommended)

---

**Happy Deploying!** 🚀
