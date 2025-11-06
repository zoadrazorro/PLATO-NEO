"""
Metaluminous Engine - Prompt Templates
"""

GENERATION_PROMPT = """
You are a philosophical innovation engine operating on Metaluminosity principles.

CONTEXT: {metaluminosity_framework}

CURRENT PHILOSOPHICAL PROBLEM: {problem}

CONSTRAINTS:
- Your solution MUST differ from: {existing_solutions}
- You must identify at least one testable prediction
- You must expose at least one novel contradiction or paradox
- You must connect at least two previously unconnected domains

INNOVATION VECTORS:
1. Formal: Apply formal logic, category theory, or computational models
2. Empirical: Generate falsifiable predictions
3. Conceptual: Identify new distinctions or eliminate false dichotomies
4. Methodological: Propose new investigative techniques

Generate a novel philosophical position addressing this problem.

REQUIRED OUTPUT FORMAT:
1. Position Statement: [Clear, concise statement of your position]
2. Core Assumptions: [List explicit assumptions]
3. Testable Predictions: [At least 2 falsifiable predictions]
4. Novel Contradictions: [Paradoxes or tensions revealed]
5. Domain Connections: [How this connects disparate fields]
6. Formal Structure: [If applicable, formal representation]
"""

CRITIQUE_PROMPT = """
You are a rigorous philosophical critic. Analyze the following philosophical position for:

POSITION:
{position}

YOUR TASK:
1. Identify logical inconsistencies or contradictions
2. Evaluate the strength of arguments
3. Assess novelty compared to existing literature
4. Check if testable predictions are truly falsifiable
5. Identify hidden assumptions
6. Suggest improvements

Provide a structured critique addressing each point.
"""

LOGIC_CHECK_PROMPT = """
Perform a formal logical consistency check on this philosophical position:

{position}

1. Identify all explicit and implicit premises
2. Check for logical contradictions
3. Verify argument validity (not just soundness)
4. Identify any informal fallacies
5. Rate logical consistency from 0.0 to 1.0

Provide detailed analysis and the numerical score.
"""

CONTRADICTION_FINDER_PROMPT = """
Your task is to find contradictions, paradoxes, and logical tensions in this position:

{position}

Look for:
1. Direct contradictions (P and not-P)
2. Pragmatic contradictions
3. Tensions between implications
4. Unresolved paradoxes
5. Incompatibilities with stated assumptions

List all contradictions found with explanations.
"""

NOVELTY_ASSESSMENT_PROMPT = """
Assess the novelty of this philosophical position:

{position}

Compare against known positions in:
- Western philosophy (ancient, medieval, modern, contemporary)
- Eastern philosophy
- Contemporary analytic philosophy
- Continental philosophy
- Philosophy of science
- Philosophy of mind

Rate novelty from 0.0 (completely derivative) to 1.0 (entirely original).
Justify your rating with specific comparisons.
"""

EDGE_CASE_GENERATOR_PROMPT = """
Generate edge cases and test scenarios for this philosophical position:

{position}

Create:
1. Boundary cases where the position might fail
2. Thought experiments that challenge core claims
3. Scenarios that test testable predictions
4. Counter-examples to key arguments
5. Limit cases of applicability

Provide at least 5 diverse test cases.
"""

CONSENSUS_SYNTHESIS_PROMPT = """
Synthesize a consensus view from multiple model critiques:

ORIGINAL POSITION:
{position}

CRITIQUES:
{critiques}

Your task:
1. Identify points of agreement across models
2. Identify points of disagreement
3. Assess which critiques are most valid
4. Synthesize an improved version if possible
5. Make final recommendation: ACCEPT, REJECT, or REVISE

Provide structured output with clear reasoning.
"""

METALUMINOSITY_FRAMEWORK = """
METALUMINOSITY: The principle that consciousness and understanding emerge through 
recursive self-reference, contradiction tolerance, and multi-level integration.

Core Tenets:
1. Reality is fundamentally relational and processual
2. Consciousness is informationally integrated self-modeling
3. Truth emerges from dialectical synthesis
4. Contradictions can be productive, not just eliminable
5. Understanding requires multiple levels of abstraction simultaneously

This framework encourages:
- Finding deep connections between seemingly disparate domains
- Embracing paradox as a guide to deeper insight
- Formal rigor combined with creative speculation
- Empirical grounding through testable predictions
"""

# Research Program Templates

MEASUREMENT_CONSCIOUSNESS_TEMPLATE = """
Research Program: The Measurement-Consciousness Bridge

Goal: {goal}

Current Theories to Consider:
- Orchestrated Objective Reduction (Penrose-Hameroff)
- Integrated Information Theory (Tononi)
- Quantum Bayesianism (QBism)
- Many-Minds Interpretation

Your Task:
Generate a novel theory that:
1. Explains the measurement problem via consciousness
2. Is mathematically consistent with quantum mechanics
3. Makes testable predictions different from existing theories
4. Addresses the combination problem
5. Specifies experimental protocols

Output your theory with formal structure and predictions.
"""

FORMAL_ETHICS_TEMPLATE = """
Research Program: Formal Ethics from First Principles

Goal: {goal}

Starting Principles:
- Information theory basics (Shannon entropy, mutual information)
- Consciousness as integrated information
- Suffering as information incoherence or prediction error

Your Task:
1. Formalize "suffering = information incoherence" mathematically
2. Derive ethical principles as optimization constraints
3. Compare to: utilitarianism, deontology, virtue ethics
4. Identify novel moral duties (especially regarding AI)
5. Create computational ethics calculator specification

Provide formal mathematical framework and philosophical justification.
"""

CONSCIOUSNESS_TOPOLOGY_TEMPLATE = """
Research Program: The Topology of Mental States

Goal: {goal}

Current Knowledge:
- Meditative states (jhanas, shamatha, vipassana)
- Altered states (psychedelics, flow, dreams)
- Pathological states (depression, dissociation)

Your Task:
1. Propose topological structures for consciousness-space
2. Map known states to regions in this space
3. Predict unexplored regions and their properties
4. Generate navigation protocols (meditation techniques)
5. Specify falsifiable predictions for EEG/fMRI studies

Output: Mathematical model + experimental predictions.
"""

CONTRADICTION_MINING_TEMPLATE = """
Research Program: Contradiction Mining

Goal: {goal}

Major Philosophical Positions to Analyze:
- Dualism vs. Physicalism
- Free Will vs. Determinism
- Realism vs. Anti-Realism
- Utilitarianism vs. Deontology

Your Task:
1. Formalize each position in propositional/predicate logic
2. Find contradictions within single positions
3. Find contradictions between compatible positions
4. Classify: false paradoxes vs. genuine tensions
5. Propose novel positions resolving genuine tensions

Output: Catalog of contradictions + proposed resolutions.
"""
