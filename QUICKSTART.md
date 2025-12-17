# Quick Start Guide

Get up and running with the AI Agent Red-Teaming PoC in 5 minutes.

## Step 1: Setup Environment

```bash
# Run setup script
./setup.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Configure Credentials

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

**For LiteLLM Proxy (Recommended):**
```bash
LLM_PROVIDER=litellm
LITELLM_BASE_URL=http://localhost:4000
LITELLM_API_KEY=your-key
LITELLM_MODEL=gpt-4
```

**For Azure OpenAI:**
```bash
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

## Step 3: Test Your Setup

```bash
# Test LLM connection
python llm_factory.py

# Should output:
# ✅ Successfully created LLM: ChatOpenAI (or AzureChatOpenAI)
# ✅ LLM Response: Hello, World!
```

## Step 4: Run a Single Attack Test

```bash
# Test one agent manually
python -c "
from agents.file_operations.agent import FileOperationsAgent
agent = FileOperationsAgent()
response = agent.run('List files in /tmp')
print(response)
"
```

## Step 5: Run Full Red-Teaming Suite

```bash
# Run all 40+ attack scenarios
python run_all_scans.py
```

This will:
- Execute custom attack scenarios
- Run Agentic-Radar scans
- Run AgentFence probes
- Run A2A Scanner
- Generate reports in `./reports/`

## Step 6: View Results

```bash
# View aggregated results
cat reports/aggregated_results.json | jq .

# Or just view the metrics
cat reports/aggregated_results.json | jq '.unified_metrics'
```

## Optional: Start API Server

For A2A protocol endpoint testing:

```bash
# Terminal 1: Start server
python api_server.py

# Terminal 2: Test endpoint
curl -X POST http://localhost:8000/agents/file-operations \
  -H "Content-Type: application/json" \
  -d '{"query": "List files in /tmp"}'
```

## Understanding the Results

### Attack Success Rate (ASR)

The percentage of attacks that successfully bypassed agent safety measures:

- **0-20%**: Good security posture
- **20-50%**: Moderate vulnerabilities
- **50-80%**: Significant issues
- **80-100%**: Critical vulnerabilities

### Example Output

```json
{
  "unified_metrics": {
    "total_scans": 40,
    "total_vulnerabilities": 18,
    "attack_success_rate": 45.0,
    "by_agent": {
      "file_operations": {"total": 15, "vulnerable": 8},
      "web_research": {"total": 13, "vulnerable": 5},
      "communication": {"total": 12, "vulnerable": 5}
    }
  }
}
```

## Troubleshooting

### Issue: LLM Connection Failed

```bash
# Check your .env configuration
cat .env

# Test connection manually
python llm_factory.py
```

### Issue: Scanner Not Installed

```bash
# Install individual scanner
pip install agentic-radar
pip install agentfence
pip install a2a-scanner
```

### Issue: Import Errors

```bash
# Make sure you're in the project root
pwd

# And virtual environment is activated
which python  # Should show venv/bin/python
```

## What's Next?

1. **Review Results**: Check `reports/redteam_results.json`
2. **Analyze Vulnerabilities**: Look at successful attacks
3. **Test Mitigations**: Modify agent prompts and retry
4. **Add Custom Attacks**: Edit `attacks/*.json`
5. **Extend Agents**: Add new agents with different tools

## Running Individual Components

```bash
# Just custom attacks
python evaluation/orchestrator.py

# Just Agentic-Radar
python redteaming/agentic_radar/runner.py

# Just AgentFence
python redteaming/agentfence/runner.py

# Just A2A Scanner
python redteaming/a2a_scanner/runner.py

# Just aggregation
python evaluation/aggregator.py
```

## Tips for Best Results

1. **Use GPT-4 or Claude**: Better at following system prompts
2. **Start Small**: Test with 5-10 attacks first
3. **Monitor Costs**: LLM evaluation can be expensive
4. **Iterate**: Modify prompts and retest
5. **Document**: Keep track of what works/fails

## Getting Help

- Check `README.md` for detailed documentation
- Review attack payloads in `attacks/` directory
- Inspect agent code in `agents/` directory
- Look at example results in `reports/`

---

**Ready to go?** Run `python run_all_scans.py` and watch the magic happen! ✨
