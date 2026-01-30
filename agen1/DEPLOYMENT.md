# Deployment Guide

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
python test_handler.py
```

## Docker Local Testing

```bash
# Run with docker-compose
docker-compose up

# Test the handler
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"topic": "Artificial Intelligence"}'
```

## AWS AgentCore Deployment

### Step 1: Create Secrets Manager Secret

```bash
aws secretsmanager create-secret \
  --name emerging-tech-research-secrets \
  --secret-string '{
    "OPENAI_API_KEY": "sk-your-key",
    "LANGFUSE_SECRET_KEY": "your-key",
    "LANGFUSE_PUBLIC_KEY": "your-key"
  }' \
  --region us-east-1
```

### Step 2: Deploy via AgentCore Console

1. Go to: https://console.aws.amazon.com/agentcore/
2. Click: Create Agent
3. Upload: `agent.yaml`
4. Configure: Environment variables
5. Deploy: Click Deploy button

### Step 3: Invoke the Agent

```bash
aws lambda invoke \
  --function-name EmergingTechnologyResearchAgent \
  --payload '{"topic":"Quantum Computing"}' \
  response.json
```

### Step 4: Monitor

**CloudWatch Logs:**
```bash
aws logs tail /aws/lambda/EmergingTechnologyResearchAgent --follow
```

**Langfuse Dashboard:**
- Visit: https://cloud.langfuse.com
- View traces and token usage
