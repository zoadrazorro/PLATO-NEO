# PLATO-NEO: Metaluminous Engine

**A Full-Stack Computational Philosophy Engine**

PLATO-NEO is a sophisticated system for generating and refining novel philosophical insights through computational exploration. Built on the principles of Metaluminosity, it combines local AI inference with multi-model debate and cloud-based refinement to produce genuinely original philosophical positions.

---

## 🎯 Overview

The Metaluminous Engine implements a multi-phase pipeline:

```
GENERATION → LOCAL CRITIQUE → MULTI-MODEL REFINEMENT → VALIDATION → SYNTHESIS
```

### Key Features

- **Local Generation**: Uses powerful local models (Qwen2.5 72B, DeepSeek-R1 70B) for initial philosophical position generation
- **Philosophical Tribunal**: Multi-model debate system for rigorous critique and validation
- **Four Sage Council**: Optional cloud API integration (Claude, GPT-4, Gemini) for deep refinement
- **Consensus Building**: Automated decision-making based on logical validity, novelty, and testability
- **Research Programs**: Pre-configured programs for specific philosophical domains
- **REST API**: FastAPI-based web service for programmatic access

---

## 🏗️ Architecture

### Hardware Requirements

**Recommended Local Setup:**
- **GPU**: Dual AMD Radeon 7900XT (48GB VRAM) or equivalent NVIDIA GPUs
- **RAM**: 128GB system memory
- **Storage**: NVMe SSD for model weights and databases

**Minimum Setup:**
- **GPU**: 24GB VRAM (single GPU)
- **RAM**: 64GB system memory
- **Storage**: 500GB SSD

### Software Stack

- **Inference**: Ollama or llama.cpp
- **Orchestration**: Python + AsyncIO
- **Database**: PostgreSQL
- **Vector Store**: Qdrant
- **API**: FastAPI + Uvicorn
- **LLM APIs**: OpenAI, Anthropic, Google (optional)

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/zoadrazorro/PLATO-NEO.git
cd PLATO-NEO

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install all dependencies
- Start Docker services (PostgreSQL, Qdrant)
- Create a `.env` file from the template

### 2. Install Ollama and Models

```bash
# Install Ollama (see https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required models
ollama pull qwen2.5:72b-instruct-q4_K_M
ollama pull deepseek-r1:70b
ollama pull mixtral:8x22b
```

### 3. Configure Environment

Edit `.env` with your settings:

```bash
# Required: Ollama configuration
OLLAMA_HOST=http://localhost:11434

# Optional: Cloud API keys for Four Sage Council
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
```

### 4. Start the Server

```bash
# Activate virtual environment
source venv/bin/activate

# Run the API server
python -m metaluminous.web.app
```

The API will be available at `http://localhost:8000`

---

## 📖 Usage

### Python API

```python
from metaluminous import MetaluminousEngine
from metaluminous.models import GenerationRequest, PhilosophicalDomain

# Initialize engine
engine = MetaluminousEngine()

# Create a generation request
request = GenerationRequest(
    problem="How can we resolve the hard problem of consciousness?",
    domains=[PhilosophicalDomain.CONSCIOUSNESS, PhilosophicalDomain.METAPHYSICS],
    constraints=[
        "Must not invoke panpsychism",
        "Must be empirically testable"
    ],
    existing_solutions=[
        "Integrated Information Theory",
        "Global Workspace Theory"
    ],
    temperature=0.7
)

# Process the problem
session = await engine.process_problem(request, use_cloud_apis=True)

# Access results
print(f"Position: {session.position.position}")
print(f"Decision: {session.final_consensus.decision}")
print(f"Novelty: {session.final_consensus.average_novelty}")
print(f"Testable Predictions: {session.position.testable_predictions}")
```

### REST API

```bash
# Generate a philosophical position
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "What is the nature of free will?",
    "domains": ["metaphysics", "consciousness"],
    "temperature": 0.7
  }'

# Explore problem space with variations
curl -X POST "http://localhost:8000/explore?num_variations=10" \
  -H "Content-Type: application/json" \
  -d '{
    "problem": "Can ethics be derived from first principles?",
    "domains": ["ethics"]
  }'

# List available domains
curl "http://localhost:8000/domains"

# Check system configuration
curl "http://localhost:8000/config"
```

### Research Programs

```python
from metaluminous.research_programs import (
    MeasurementConsciousnessProgram,
    FormalEthicsProgram
)

# Run the Measurement-Consciousness Bridge program
program = MeasurementConsciousnessProgram()
results = await program.run(num_variations=100)

print(f"Generated {results['total_generated']} theories")
print(f"Acceptable: {results['acceptable_count']}")
print(f"Top theory: {results['top_theories'][0]}")

# Run the Formal Ethics program
ethics_program = FormalEthicsProgram()
ethics_results = await ethics_program.run()

print(f"Ethical framework: {ethics_results['ethical_principles']}")
print(f"AI duties: {ethics_results['ai_moral_duties']}")
```

---

## 🔬 Research Programs

### 1. Measurement-Consciousness Bridge
Explores consciousness-based solutions to the quantum measurement problem.

**Goal**: Generate novel interpretations connecting consciousness and quantum mechanics  
**Output**: Formal theories with testable predictions and experimental protocols

### 2. Formal Ethics from First Principles
Derives ethical frameworks from information theory and consciousness.

**Goal**: Create computational ethics based on mathematical foundations  
**Output**: Formal ethical framework with AI-specific moral duties

### 3. Topology of Mental States
Maps consciousness-space using topological structures.

**Goal**: Create mathematical models of meditative and altered states  
**Output**: "Map of Consciousness" with navigation protocols

### 4. Contradiction Mining
Systematically finds and resolves philosophical paradoxes.

**Goal**: Catalog genuine contradictions in philosophy  
**Output**: Contradiction catalog with proposed resolutions

---

## 🏛️ Core Concepts

### Metaluminosity Framework

The engine operates on principles of **Metaluminosity**:

1. **Recursive Self-Reference**: Understanding emerges through systems examining themselves
2. **Contradiction Tolerance**: Paradoxes guide insight rather than being eliminated
3. **Multi-Level Integration**: Truth requires simultaneous multiple abstractions
4. **Relational Ontology**: Reality is fundamentally processual and relational
5. **Empirical Grounding**: Philosophical positions must generate testable predictions

### The Philosophical Tribunal

A multi-model debate system where different AI models critique positions:

- **Logic Checker**: Verifies formal consistency
- **Contradiction Finder**: Identifies paradoxes and tensions
- **Novelty Assessor**: Compares to existing philosophical literature
- **Edge Case Generator**: Creates test scenarios and counterexamples

### The Four Sage Council

Cloud-based refinement using specialized models:

1. **Claude (Anthropic)**: Deep philosophical analysis and implicit assumptions
2. **GPT-4 (OpenAI)**: Formal logical verification and mathematical modeling
3. **Gemini (Google)**: Interdisciplinary connections and scientific grounding
4. **GPT-4o (OpenAI)**: Accessibility assessment and synthesis

### Consensus Algorithm

Positions are accepted based on:
- ✅ Unanimous logical validity across all models
- ✅ Novelty score above threshold (default: 0.7)
- ✅ Minimum testable predictions (default: 2)
- ✅ Coherence agreement (3/4 models minimum)

---

## 📚 API Documentation

### Models

#### `GenerationRequest`
```python
{
    "problem": str,                          # The philosophical problem
    "domains": List[PhilosophicalDomain],    # Relevant domains
    "constraints": List[str],                # Constraints on solutions
    "existing_solutions": List[str],         # Known solutions to differ from
    "innovation_vectors": List[str],         # Suggested approaches
    "temperature": float                     # Generation randomness (0.0-2.0)
}
```

#### `PhilosophicalPosition`
```python
{
    "id": str,
    "problem": str,
    "position": str,                         # The generated position
    "domains": List[PhilosophicalDomain],
    "assumptions": List[str],
    "testable_predictions": List[str],
    "contradictions": List[str],
    "novelty_score": float,
    "coherence_score": float
}
```

#### `DebateSession`
```python
{
    "id": str,
    "position": PhilosophicalPosition,
    "critiques": List[Critique],
    "iterations": int,
    "converged": bool,
    "final_consensus": ConsensusResult
}
```

### Endpoints

- `GET /` - Root endpoint with system info
- `GET /health` - Health check
- `POST /generate` - Generate and critique a position
- `POST /explore` - Explore problem space with variations
- `GET /domains` - List available philosophical domains
- `GET /config` - Get current configuration

---

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=metaluminous

# Run specific test file
pytest tests/unit/test_generation.py
```

### Code Quality

```bash
# Format code
black metaluminous/

# Lint code
ruff check metaluminous/

# Type checking
mypy metaluminous/
```

### Project Structure

```
PLATO-NEO/
├── metaluminous/           # Main package
│   ├── core/              # Core engine components
│   │   ├── engine.py      # Main orchestration
│   │   ├── generation.py  # Position generation
│   │   ├── tribunal.py    # Multi-model debate
│   │   └── consensus.py   # Consensus building
│   ├── api/               # API clients
│   │   ├── llm_clients.py # LLM client abstractions
│   │   └── four_sages.py  # Cloud API integration
│   ├── models/            # Data models
│   │   └── schema.py      # Pydantic models
│   ├── prompts/           # Prompt templates
│   │   └── templates.py   # All prompts
│   ├── research_programs/ # Research programs
│   ├── web/               # FastAPI application
│   │   └── app.py         # Web server
│   └── config.py          # Configuration
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── docker-compose.yml     # Docker services
├── requirements.txt       # Python dependencies
└── .env.example          # Environment template
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

- Inspired by computational philosophy and AI safety research
- Built on the shoulders of giants: Ollama, FastAPI, LangChain
- Special thanks to the open-source AI community

---

## 📞 Contact

For questions, issues, or philosophical discussions:
- GitHub Issues: https://github.com/zoadrazorro/PLATO-NEO/issues
- Project Website: Coming soon

---

**Note**: This is experimental philosophical research software. Results should be critically evaluated and not taken as authoritative philosophical claims.
