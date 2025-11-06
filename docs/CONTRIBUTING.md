# Contributing to PLATO-NEO

Thank you for your interest in contributing to the Metaluminous Engine! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/PLATO-NEO.git
   cd PLATO-NEO
   ```
3. Run setup:
   ```bash
   ./scripts/setup.sh
   ```
4. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Standards

### Python Style
- Follow PEP 8
- Use **Black** for formatting (line length: 100)
- Use **Ruff** for linting
- Use **type hints** where appropriate
- Use **docstrings** for all public functions

### Code Quality Tools
```bash
# Format code
black metaluminous/

# Lint
ruff check metaluminous/

# Type check
mypy metaluminous/

# Run all checks
black metaluminous/ && ruff check metaluminous/ && mypy metaluminous/
```

### Testing
- Write tests for new features
- Maintain test coverage
- Tests should be in `tests/unit/` or `tests/integration/`
- Use pytest fixtures for common setup

```bash
# Run tests
pytest tests/unit/ -v

# With coverage
pytest tests/unit/ --cov=metaluminous --cov-report=html

# Run specific test
pytest tests/unit/test_models.py::test_philosophical_position_creation
```

## Project Structure

```
metaluminous/
├── core/              # Core engine logic
│   ├── engine.py      # Main orchestration
│   ├── generation.py  # Position generation
│   ├── tribunal.py    # Multi-model debate
│   └── consensus.py   # Consensus building
├── api/               # API clients
│   ├── llm_clients.py # LLM abstractions
│   └── four_sages.py  # Cloud integration
├── models/            # Data models
│   └── schema.py      # Pydantic models
├── prompts/           # Prompt templates
│   └── templates.py   # All prompts
├── research_programs/ # Research programs
├── web/               # Web API
│   └── app.py         # FastAPI app
├── db/                # Database layer (future)
└── utils/             # Utilities (future)
```

## Adding Features

### Adding a New Research Program

1. Create file in `metaluminous/research_programs/`:
   ```python
   # your_program.py
   from ..models import GenerationRequest, PhilosophicalDomain
   from ..core import MetaluminousEngine
   
   class YourProgram:
       def __init__(self):
           self.engine = MetaluminousEngine()
           
       async def run(self) -> dict:
           # Implementation
           pass
   ```

2. Add to `__init__.py`:
   ```python
   from .your_program import YourProgram
   __all__ = [..., "YourProgram"]
   ```

3. Add tests in `tests/unit/test_your_program.py`

### Adding a New API Endpoint

1. Edit `metaluminous/web/app.py`:
   ```python
   @app.post("/your-endpoint")
   async def your_endpoint(request: YourRequest):
       """Docstring describing endpoint"""
       try:
           result = await engine.your_method(request)
           return result
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

2. Add request/response models to `metaluminous/models/schema.py`

3. Test manually and add integration tests

### Adding a New Prompt Template

1. Edit `metaluminous/prompts/templates.py`:
   ```python
   YOUR_PROMPT = """
   Your prompt template here with {variables}
   """
   ```

2. Add to exports in `__init__.py`

3. Use in your code:
   ```python
   from metaluminous.prompts import YOUR_PROMPT
   prompt = YOUR_PROMPT.format(variables=values)
   ```

## Pull Request Process

1. **Update tests**: Add/update tests for your changes
2. **Run tests**: Ensure all tests pass
3. **Update docs**: Update README.md if needed
4. **Format code**: Run Black and Ruff
5. **Commit**:
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   ```
6. **Push**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create PR**: Open a pull request on GitHub

### Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

Examples:
```
feat: Add consciousness topology research program
fix: Correct consensus threshold calculation
docs: Update API documentation
test: Add tests for generation engine
```

## Code Review Guidelines

When reviewing PRs:
- Check code quality and style
- Verify tests pass and cover new code
- Review documentation updates
- Test functionality manually if needed
- Provide constructive feedback

## Areas for Contribution

### High Priority
- [ ] Integration tests with mock LLM responses
- [ ] Database persistence layer
- [ ] Vector database integration for literature
- [ ] Web UI dashboard
- [ ] Formal logic verification (Z3/Lean integration)

### Medium Priority
- [ ] Additional research programs
- [ ] Performance optimizations
- [ ] Better error handling
- [ ] Logging improvements
- [ ] Configuration validation

### Nice to Have
- [ ] CLI interface
- [ ] Export to various formats (PDF, LaTeX)
- [ ] Visualization tools
- [ ] Batch processing
- [ ] Result caching

## Testing Guidelines

### Unit Tests
- Test individual functions/classes
- Mock external dependencies
- Fast execution
- High coverage

Example:
```python
@pytest.mark.asyncio
async def test_consensus_accept():
    position = PhilosophicalPosition(...)
    critiques = [...]
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(position, critiques)
    assert consensus.decision == "ACCEPT"
```

### Integration Tests
- Test component interaction
- Use real databases (or testcontainers)
- Test API endpoints
- May be slower

Example:
```python
@pytest.mark.integration
async def test_full_pipeline():
    engine = MetaluminousEngine()
    request = GenerationRequest(...)
    session = await engine.process_problem(request)
    assert session.final_consensus is not None
```

## Documentation

### Code Documentation
- Use docstrings for all public APIs
- Include parameter descriptions
- Include return value descriptions
- Include examples where helpful

Example:
```python
async def generate_position(self, request: GenerationRequest) -> PhilosophicalPosition:
    """
    Generate a novel philosophical position.
    
    Args:
        request: GenerationRequest with problem and constraints
        
    Returns:
        PhilosophicalPosition with generated content
        
    Example:
        >>> request = GenerationRequest(problem="What is consciousness?")
        >>> position = await engine.generate_position(request)
    """
```

### User Documentation
- Update README.md for major features
- Add examples to `examples/` directory
- Update GETTING_STARTED.md if setup changes
- Update QUICK_REFERENCE.md for new APIs

## Performance Considerations

- Use `async/await` for I/O operations
- Batch API calls where possible
- Cache expensive computations
- Profile before optimizing
- Document performance characteristics

## Security

- Never commit API keys or secrets
- Use environment variables for sensitive config
- Validate all user input
- Sanitize LLM outputs before storage
- Follow security best practices

## Questions?

- Open an issue for bugs
- Start a discussion for feature ideas
- Ask in pull requests for code questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to PLATO-NEO! 🧠✨
