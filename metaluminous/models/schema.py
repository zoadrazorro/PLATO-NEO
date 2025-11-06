"""
Metaluminous Engine - Core Data Models
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PhilosophicalDomain(str, Enum):
    """Major philosophical domains"""
    METAPHYSICS = "metaphysics"
    EPISTEMOLOGY = "epistemology"
    ETHICS = "ethics"
    CONSCIOUSNESS = "consciousness"
    LOGIC = "logic"
    AESTHETICS = "aesthetics"
    POLITICAL = "political"
    PHENOMENOLOGY = "phenomenology"
    QUANTUM = "quantum_mechanics"


class ModelRole(str, Enum):
    """Roles for different models in the system"""
    GENERATOR = "generator"
    CRITIC = "critic"
    CREATIVE = "creative"
    REFINER = "refiner"
    VALIDATOR = "validator"


class PhilosophicalPosition(BaseModel):
    """A generated philosophical position"""
    id: Optional[str] = None
    problem: str
    position: str
    domains: List[PhilosophicalDomain]
    assumptions: List[str] = Field(default_factory=list)
    testable_predictions: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    novelty_score: Optional[float] = None
    coherence_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Critique(BaseModel):
    """A critique of a philosophical position"""
    position_id: str
    model: str
    role: ModelRole
    logical_consistency: float = Field(ge=0.0, le=1.0)
    identified_flaws: List[str] = Field(default_factory=list)
    contradictions_found: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    novelty_assessment: Optional[float] = Field(None, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConsensusResult(BaseModel):
    """Result of multi-model consensus building"""
    position_id: str
    unanimous_validity: bool
    average_novelty: float
    testable_predictions_count: int
    coherence_agreement: int  # Number of models agreeing on coherence
    decision: str  # ACCEPT, REJECT, or REVISE
    reasons: List[str] = Field(default_factory=list)
    participating_models: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ResearchProgram(BaseModel):
    """A research program configuration"""
    id: str
    name: str
    goal: str
    method: str
    domain: PhilosophicalDomain
    constraints: List[str] = Field(default_factory=list)
    innovation_vectors: List[str] = Field(default_factory=list)
    expected_output: str
    status: str = "pending"  # pending, running, completed, failed
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


class GenerationRequest(BaseModel):
    """Request for generating a philosophical position"""
    problem: str
    domains: List[PhilosophicalDomain] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    existing_solutions: List[str] = Field(default_factory=list)
    innovation_vectors: List[str] = Field(default_factory=list)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class DebateSession(BaseModel):
    """A multi-model debate session"""
    id: str
    position: PhilosophicalPosition
    critiques: List[Critique] = Field(default_factory=list)
    iterations: int = 0
    max_iterations: int = 10
    converged: bool = False
    final_consensus: Optional[ConsensusResult] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
