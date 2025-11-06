# Getting Started with PLATO-NEO

This guide will walk you through setting up and using the Metaluminous Engine for the first time.

## Prerequisites

### Required
- **Python 3.10+** - Check with `python3 --version`
- **Docker & Docker Compose** - For PostgreSQL and Qdrant
- **Git** - For cloning the repository
- **8GB+ RAM** - Minimum for basic operation

### Recommended (for local inference)
- **GPU with 24GB+ VRAM** - For running local LLMs
- **Ollama** - For easy local model management
- **64GB+ System RAM** - For running larger models

## Installation

### Step 1: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/zoadrazorro/PLATO-NEO.git
cd PLATO-NEO

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This will:
- Create a Python virtual environment
- Install all dependencies
- Start Docker services (PostgreSQL, Qdrant)
- Create a `.env` file

### Step 2: Install Ollama (Optional but Recommended)

For local inference without API costs:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models (requires significant disk space and time)
ollama pull qwen2.5:72b-instruct-q4_K_M    # ~40GB
ollama pull deepseek-r1:70b                # ~40GB
ollama pull mixtral:8x22b                  # ~80GB

# For testing with smaller models:
ollama pull qwen2.5:7b-instruct            # ~4.7GB
```

### Step 3: Configure Environment

Edit `.env` file:

```bash
# Required for local inference (if using Ollama)
OLLAMA_HOST=http://localhost:11434

# Optional: Cloud API keys for Four Sage Council
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Adjust model names if using smaller models
OLLAMA_PRIMARY_MODEL=qwen2.5:7b-instruct   # For testing
```

### Step 4: Verify Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
pytest tests/unit/ -v

# Check imports
python3 -c "from metaluminous import MetaluminousEngine; print('Success!')"
```

## Basic Usage

### 1. Start the API Server

```bash
source venv/bin/activate
python -m metaluminous.web.app
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

### 2. Use the Python API

Create a file `my_first_position.py`:

```python
import asyncio
from metaluminous.core import MetaluminousEngine
from metaluminous.models import GenerationRequest, PhilosophicalDomain

async def main():
    # Initialize engine
    engine = MetaluminousEngine()
    
    # Create request
    request = GenerationRequest(
        problem="What is the relationship between mind and body?",
        domains=[PhilosophicalDomain.CONSCIOUSNESS, PhilosophicalDomain.METAPHYSICS],
        constraints=["Must avoid simple dualism"],
        temperature=0.7
    )
    
    # Generate and critique position
    session = await engine.process_problem(request, use_cloud_apis=False)
    
    # Display results
    print(f"Decision: {session.final_consensus.decision}")
    print(f"Novelty: {session.final_consensus.average_novelty:.2f}")
    print(f"\nPosition:\n{session.position.position}")

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python my_first_position.py
```

### 3. Use the REST API

```bash
# Generate a position
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Can artificial intelligence be conscious?",
    "domains": ["consciousness"],
    "temperature": 0.7
  }'

# Explore multiple variations
curl -X POST "http://localhost:8000/explore?num_variations=5" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "What is the nature of time?",
    "domains": ["metaphysics"]
  }'
```

### 4. Run a Research Program

```python
import asyncio
from metaluminous.research_programs import MeasurementConsciousnessProgram

async def main():
    program = MeasurementConsciousnessProgram()
    results = await program.run(num_variations=10)
    
    print(f"Generated {results['total_generated']} theories")
    print(f"Acceptable: {results['acceptable_count']}")
    
    if results['top_theories']:
        print(f"\nTop theory (novelty: {results['top_theories'][0]['novelty']:.2f}):")
        print(results['top_theories'][0]['position'])

if __name__ == "__main__":
    asyncio.run(main())
```

## Using Cloud APIs (Four Sage Council)

For deeper philosophical analysis, you can use cloud APIs:

1. **Get API Keys**:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://ai.google.dev/

2. **Add to `.env`**:
   ```bash
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...
   ```

3. **Use in code**:
   ```python
   session = await engine.process_problem(request, use_cloud_apis=True)
   ```

This will run your position through Claude, GPT-4, and Gemini for comprehensive critique.

## Common Issues

### "No module named 'metaluminous'"
```bash
# Make sure you're in the virtual environment
source venv/bin/activate
```

### "Connection refused" errors
```bash
# Make sure Docker services are running
docker-compose ps

# If not running:
docker-compose up -d
```

### "Model not found" errors
```bash
# Check if Ollama is running
ollama list

# If model is missing, pull it:
ollama pull qwen2.5:7b-instruct
```

### Out of memory errors
- Use smaller models for testing: `qwen2.5:7b-instruct`
- Reduce batch size in exploration: `num_variations=3`
- Close other applications to free RAM

## Next Steps

1. **Read the Documentation**: Check out `README.md` for comprehensive docs
2. **Explore Examples**: Look at `examples/basic_generation.py`
3. **Run Research Programs**: Try the pre-configured philosophical programs
4. **Customize Prompts**: Edit `metaluminous/prompts/templates.py`
5. **Build Your Own Programs**: Create custom research programs in `metaluminous/research_programs/`

## Development

### Running Tests
```bash
pytest tests/ -v
pytest tests/ --cov=metaluminous  # With coverage
```

### Code Quality
```bash
black metaluminous/           # Format code
ruff check metaluminous/      # Lint code
mypy metaluminous/            # Type checking
```

### Project Structure
```
metaluminous/
├── core/           # Core engine and orchestration
├── api/            # LLM client abstractions
├── models/         # Data models
├── prompts/        # Prompt templates
├── research_programs/  # Pre-configured programs
└── web/            # FastAPI application
```

## Support

- **Issues**: https://github.com/zoadrazorro/PLATO-NEO/issues
- **Documentation**: See README.md
- **Examples**: See examples/ directory

## Tips for Best Results

1. **Start Small**: Use smaller models and fewer iterations for testing
2. **Be Specific**: Provide clear constraints and existing solutions to avoid
3. **Iterate**: Use the revision system to refine positions
4. **Validate**: Check testable predictions in generated positions
5. **Explore**: Use the exploration endpoint to find novel angles

Happy philosophizing! 🧠✨
