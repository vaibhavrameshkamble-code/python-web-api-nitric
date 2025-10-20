# AWS Deployment Guide

This guide provides detailed instructions for deploying the Python Web API to AWS using Nitric.

## Prerequisites Checklist

Before deploying to AWS, ensure you have:

- [ ] AWS Account with appropriate permissions
- [ ] AWS CLI installed and configured
- [ ] Nitric CLI installed
- [ ] Python 3.11+ installed
- [ ] uv or pip installed

## Step-by-Step Deployment

### 1. Configure AWS Credentials

If you haven't already, configure your AWS credentials:

```bash
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

Verify your credentials:
```bash
aws sts get-caller-identity
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Build the Application

Build your application for deployment:

```bash
nitric build
```

This will:
- Compile your application
- Build Docker images
- Prepare deployment artifacts

### 4. Deploy to AWS

Deploy your application:

```bash
nitric up
```

You'll be prompted to:
1. Select a cloud provider: Choose `aws`
2. Select a region: Choose your preferred AWS region (e.g., `us-east-1`)
3. Provide a stack name: Enter a name for your deployment (e.g., `python-web-api-prod`)

Example interaction:
```
? Select a cloud provider: aws
? Select a region: us-east-1
? Enter a stack name: python-web-api-prod
```

### 5. Wait for Deployment

Nitric will now provision the following AWS resources:
- **API Gateway**: HTTP API endpoint
- **Lambda Functions**: Serverless compute for your API
- **DynamoDB Table**: For the key-value store
- **IAM Roles and Policies**: For secure access
- **CloudWatch Logs**: For monitoring and debugging

This typically takes 2-5 minutes.

### 6. Access Your API

Once deployment completes, Nitric will display your API endpoint:

```
Deployed successfully!

API Endpoints:
  main: https://abc123def.execute-api.us-east-1.amazonaws.com
```

Test your deployed API:
```bash
# Replace with your actual endpoint
export API_URL="https://abc123def.execute-api.us-east-1.amazonaws.com"

# Health check
curl $API_URL/health

# Create a task
curl -X POST $API_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Production task", "description": "Running on AWS!"}'
```

## Managing Your Deployment

### View Deployment Status

```bash
nitric status
```

### Update Your Deployment

After making code changes:

```bash
# Build new changes
nitric build

# Deploy updates
nitric up
```

### View Logs

Check CloudWatch logs:

```bash
# Using AWS CLI
aws logs tail /aws/lambda/python-web-api-prod-main --follow
```

Or view in AWS Console:
1. Go to CloudWatch → Log groups
2. Find your Lambda function logs
3. View real-time logs

### Remove Deployment

When you're done and want to remove all AWS resources:

```bash
nitric down
```

Confirm the stack name when prompted. This will:
- Delete the API Gateway
- Remove Lambda functions
- Delete DynamoDB tables
- Clean up IAM roles
- Remove CloudWatch logs (after retention period)

## Cost Estimation

### AWS Free Tier (First 12 months)
- Lambda: 1M free requests per month
- API Gateway: 1M API calls per month
- DynamoDB: 25GB storage, 25 read/write capacity units

### After Free Tier
Estimated monthly costs for low-traffic application:
- Lambda: ~$0.20 per 1M requests
- API Gateway: ~$1.00 per 1M requests
- DynamoDB: ~$0.25 per GB per month

Total: **$1-5/month** for typical development workloads

## Environment-Specific Deployments

Deploy to different environments using different stack names:

```bash
# Development
nitric up --stack dev

# Staging
nitric up --stack staging

# Production
nitric up --stack prod
```

## Custom Domain Setup

To use a custom domain with your API:

1. **Register a domain** in Route 53 or your preferred registrar
2. **Create a certificate** in AWS Certificate Manager
3. **Configure in nitric.yaml**:

```yaml
name: python-web-api-nitric
services:
  - match: services/*.py
    start: uv run watchmedo auto-restart -p *.py --no-restart-on-command-exit -R uv run $SERVICE_PATH
    runtime: python
runtimes:
  python:
    dockerfile: "./python.dockerfile"
```

4. **Redeploy**: `nitric up`

## Monitoring and Observability

### CloudWatch Metrics
- Monitor Lambda invocations
- Track API Gateway requests
- View error rates and latency

### X-Ray Tracing
Enable X-Ray for distributed tracing:
- See request flow through services
- Identify performance bottlenecks
- Debug errors in production

### Alarms
Set up CloudWatch alarms for:
- Error rates
- Response times
- Request counts

## Security Best Practices

1. **Use IAM roles** (automatically handled by Nitric)
2. **Enable API throttling** to prevent abuse
3. **Implement authentication** for production APIs
4. **Use AWS Secrets Manager** for sensitive data
5. **Enable CloudTrail** for audit logging
6. **Regular security updates** for dependencies

## Troubleshooting

### Deployment Fails

**Check AWS permissions:**
```bash
aws iam get-user
```

Ensure your IAM user has permissions for:
- Lambda
- API Gateway
- DynamoDB
- CloudFormation
- IAM
- S3

**Check Nitric version:**
```bash
nitric version
```

Update if needed:
```bash
nitric update
```

### API Returns 502 Bad Gateway

Check Lambda logs:
```bash
nitric logs
```

Common causes:
- Python runtime errors
- Missing dependencies
- Timeout issues

### High Costs

Monitor costs in AWS Cost Explorer:
- Check Lambda invocations
- Review DynamoDB read/write units
- Verify API Gateway usage

## Rollback

If a deployment has issues:

```bash
# Remove the bad deployment
nitric down

# Redeploy the previous version
git checkout <previous-commit>
nitric up
```

## CI/CD Integration

For automated deployments, see GitHub Actions example:

```yaml
name: Deploy to AWS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: nitrictech/setup-nitric@v1
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - name: Deploy
        run: nitric up --ci
```

## Additional Resources

- [Nitric AWS Provider Documentation](https://nitric.io/docs/reference/providers/aws)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

## Support

- Nitric Discord: https://nitric.io/chat
- Nitric GitHub: https://github.com/nitrictech/nitric
- AWS Support: https://aws.amazon.com/support/

---

Happy deploying! 🚀
