# AI Market Intelligence Platform

An enterprise-grade agentic application for researching emerging technologies, powered by CrewAI and deployed on AWS AgentCore.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- AWS Account (for cloud deployment)
- API Keys: OpenAI, Langfuse

### Local Setup

```bash
# Clone the repository
git clone https://github.com/Ayushant/ai-market-intelligence-platform.git
cd ai-market-intelligence-platform

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Test locally
python test_handler.py

# Run CLI mode
python -m researcheragen1.run
```

### Docker Setup (Local Testing)

```bash
# Build and run
docker-compose up

# Test the agent
curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
  -d '{"topic": "Quantum Computing"}'
```

## 📁 Project Structure

```
.
├── agentcore_handler.py          # AWS Lambda handler
├── requirements.txt              # Python dependencies
├── agent.yaml                    # AgentCore configuration
├── .env.example                  # Environment template
├── .gitignore                    # Git protection rules
├── test_handler.py              # Local testing script
├── pyproject.toml               # Project metadata
├── docker/
│   ├── Dockerfile               # Container image
│   └── docker-compose.yml       # Local test setup
└── researcheragen1/             # Agent implementation
    ├── run.py                   # CLI entry point
    ├── crews/
    │   └── researchCrew.py      # CrewAI agent definition
    ├── config/
    │   ├── researchAgents.yaml  # Agent configurations
    │   └── researchTasks.yaml   # Task definitions
    └── utils/
        ├── env.py               # AWS Secrets integration
        └── llmUtils.py          # LLM configuration
```

## 🧠 How It Works

The platform orchestrates multiple AI agents to research emerging technologies:

1. **Researcher Agent** - Gathers cutting-edge information from the latest developments
2. **Reporting Agent** - Synthesizes findings into comprehensive, structured reports

### Architecture

```
User Request (Topic)
        ↓
AWS Lambda (agentcore_handler.py)
        ↓
CrewAI Crew (Sequential Execution)
├─ Researcher Agent → GPT-4
└─ Reporting Agent → GPT-4
        ↓
AWS Secrets Manager (Secure Credentials)
AWS CloudWatch (Logging)
Langfuse (LLM Observability)
        ↓
JSON Research Report
```

## 🚀 Deployment

### Local Testing
```bash
python test_handler.py
```

### AWS AgentCore Deployment

1. **Create AWS Secrets Manager Secret**
```bash
aws secretsmanager create-secret \
  --name emerging-tech-research-secrets \
  --secret-string '{"OPENAI_API_KEY":"sk-...", "LANGFUSE_SECRET_KEY":"..."}'
```

2. **Deploy via AgentCore Console**
   - Go to: https://console.aws.amazon.com/agentcore/
   - Upload `agent.yaml`
   - Configure environment variables
   - Deploy

3. **Invoke in Cloud**
```bash
aws lambda invoke \
  --function-name EmergingTechnologyResearchAgent \
  --payload '{"topic":"AI in Healthcare"}' \
  response.json
```

## 📊 Monitoring

### CloudWatch Logs
```bash
aws logs tail /aws/lambda/EmergingTechnologyResearchAgent --follow
```

### Langfuse Dashboard
- URL: https://cloud.langfuse.com
- View: LLM traces, token usage, costs

## 📚 Technology Stack

- **Framework**: CrewAI (Agent Orchestration)
- **LLM**: OpenAI GPT-4
- **Cloud**: AWS Lambda, Secrets Manager, CloudWatch
- **Observability**: Langfuse
- **Container**: Docker
- **Language**: Python 3.11+

## 🔒 Security

- ✅ No hardcoded API keys
- ✅ AWS Secrets Manager integration
- ✅ Environment-based configuration
- ✅ IAM role-based access
- ✅ Encrypted credentials

## 💰 Cost Optimization

- **Lambda**: Free tier covers 1M invocations/month
- **Secrets Manager**: Free tier included
- **CloudWatch**: 5GB free logs/month
- **OpenAI**: ~$0.01 per research request (varies)


