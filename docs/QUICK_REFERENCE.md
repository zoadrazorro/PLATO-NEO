# PLATO-NEO Quick Reference

## Command Cheatsheet

### Setup
```bash
./scripts/setup.sh                    # Initial setup
source venv/bin/activate              # Activate environment
docker-compose up -d                  # Start databases
docker-compose down                   # Stop databases
```

### Ollama Models
```bash
ollama list                           # List installed models
ollama pull qwen2.5:7b-instruct      # Pull model
ollama run qwen2.5:7b-instruct       # Test model
ollama rm qwen2.5:7b-instruct        # Remove model
```

### Running
```bash
python -m metaluminous.web.app       # Start API server
python examples/basic_generation.py  # Run example
pytest tests/unit/ -v                # Run tests
```

### Development
```bash
black metaluminous/                   # Format code
ruff check metaluminous/              # Lint code
mypy metaluminous/                    # Type check
pytest --cov=metaluminous             # Test with coverage
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System information |
| GET | `/health` | Health check |
| POST | `/generate` | Generate philosophical position |
| POST | `/explore` | Explore problem space with variations |
| GET | `/domains` | List available philosophical domains |
| GET | `/config` | Get current configuration |

## Python API Quick Reference

### Basic Generation
```python
from metaluminous.core import MetaluminousEngine
from metaluminous.models import GenerationRequest, PhilosophicalDomain

engine = MetaluminousEngine()
request = GenerationRequest(
    problem="Your philosophical question",
    domains=[PhilosophicalDomain.CONSCIOUSNESS],
    constraints=["Avoid X", "Must include Y"],
    temperature=0.7
)
session = await engine.process_problem(request)
```

### Exploration
```python
sessions = await engine.explore_problem_space(
    request,
    num_variations=10
)
best_session = sessions[0]  # Sorted by quality
```

### Research Programs
```python
from metaluminous.research_programs import MeasurementConsciousnessProgram

program = MeasurementConsciousnessProgram()
results = await program.run(num_variations=100)
```

## Configuration Variables

### Ollama
- `OLLAMA_HOST` - Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_PRIMARY_MODEL` - Main generation model
- `OLLAMA_CRITIC_MODEL` - Critique model
- `OLLAMA_CREATIVE_MODEL` - Creative exploration model

### Cloud APIs
- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `GOOGLE_API_KEY` - Google API key

### Database
- `POSTGRES_HOST` - PostgreSQL host
- `POSTGRES_PORT` - PostgreSQL port
- `POSTGRES_DB` - Database name
- `QDRANT_HOST` - Qdrant host
- `QDRANT_PORT` - Qdrant port

### Generation
- `MAX_ITERATIONS` - Max refinement iterations (default: 10)
- `TEMPERATURE` - Generation randomness (default: 0.7)
- `NOVELTY_THRESHOLD` - Min novelty score (default: 0.7)
- `MIN_TESTABLE_PREDICTIONS` - Required predictions (default: 2)

## Philosophical Domains

- `consciousness` - Philosophy of mind
- `metaphysics` - Nature of reality
- `epistemology` - Theory of knowledge
- `ethics` - Moral philosophy
- `logic` - Formal logic
- `aesthetics` - Philosophy of art
- `political` - Political philosophy
- `phenomenology` - Lived experience
- `quantum_mechanics` - Quantum philosophy

## Model Roles

- `generator` - Generates new positions
- `critic` - Critiques positions
- `creative` - Creative exploration
- `refiner` - Refines and improves
- `validator` - Validates logic

## Consensus Decisions

- `ACCEPT` - Position meets all criteria
- `REJECT` - Critical flaw found
- `REVISE` - Needs improvement

## Common Patterns

### With Cloud APIs
```python
session = await engine.process_problem(
    request,
    use_cloud_apis=True  # Uses Four Sage Council
)
```

### Local Only (Free)
```python
session = await engine.process_problem(
    request,
    use_cloud_apis=False  # Uses only Ollama
)
```

### Accessing Results
```python
# Position
position = session.position
print(position.position)          # Main text
print(position.assumptions)       # Assumptions
print(position.testable_predictions)  # Predictions

# Consensus
consensus = session.final_consensus
print(consensus.decision)         # ACCEPT/REJECT/REVISE
print(consensus.average_novelty)  # Novelty score
print(consensus.reasons)          # Decision reasons

# Critiques
for critique in session.critiques:
    print(critique.model)         # Model name
    print(critique.role)          # Role
    print(critique.logical_consistency)  # Score
```

## Prompt Templates

Located in `metaluminous/prompts/templates.py`:

- `GENERATION_PROMPT` - Main generation
- `CRITIQUE_PROMPT` - General critique
- `LOGIC_CHECK_PROMPT` - Logic validation
- `CONTRADICTION_FINDER_PROMPT` - Find paradoxes
- `NOVELTY_ASSESSMENT_PROMPT` - Assess novelty
- `EDGE_CASE_GENERATOR_PROMPT` - Generate tests
- `CONSENSUS_SYNTHESIS_PROMPT` - Build consensus

## Research Program Templates

- `MEASUREMENT_CONSCIOUSNESS_TEMPLATE`
- `FORMAL_ETHICS_TEMPLATE`
- `CONSCIOUSNESS_TOPOLOGY_TEMPLATE`
- `CONTRADICTION_MINING_TEMPLATE`

## Error Messages

| Error | Solution |
|-------|----------|
| "No module named 'metaluminous'" | Run `source venv/bin/activate` |
| "Connection refused" | Start Docker: `docker-compose up -d` |
| "Model not found" | Pull model: `ollama pull <model>` |
| "Out of memory" | Use smaller model or reduce batch size |
| "API key not found" | Set in `.env` file |

## Performance Tips

1. **Use smaller models for testing**: `qwen2.5:7b-instruct`
2. **Limit variations**: Start with 3-5, increase as needed
3. **Cache results**: Save sessions to avoid regenerating
4. **Use local only**: Faster and free (no API costs)
5. **Parallel processing**: Engine uses async/await

## File Locations

- **Configuration**: `.env`
- **Models**: `metaluminous/models/`
- **Prompts**: `metaluminous/prompts/templates.py`
- **Examples**: `examples/`
- **Tests**: `tests/unit/`, `tests/integration/`
- **Logs**: Console output (configure with `LOG_LEVEL`)

## Quick Debugging

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check configuration
from metaluminous import settings
print(settings.ollama_host)
print(settings.database_url)

# Test database connection
import asyncio
from sqlalchemy import create_engine
engine = create_engine(settings.database_url)
conn = engine.connect()
print("Database connected!")
```

## Resources

- **Full Documentation**: `README.md`
- **Getting Started Guide**: `docs/GETTING_STARTED.md`
- **Examples**: `examples/basic_generation.py`
- **API Docs**: http://localhost:8000/docs (when running)
- **GitHub**: https://github.com/zoadrazorro/PLATO-NEO
