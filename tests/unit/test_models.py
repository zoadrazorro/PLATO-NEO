"""
Unit tests for data models
"""
import pytest
from datetime import datetime

from metaluminous.models import (
    PhilosophicalDomain,
    ModelRole,
    PhilosophicalPosition,
    Critique,
    ConsensusResult,
    GenerationRequest,
    DebateSession,
)


def test_philosophical_domain_enum():
    """Test PhilosophicalDomain enum"""
    assert PhilosophicalDomain.CONSCIOUSNESS == "consciousness"
    assert PhilosophicalDomain.ETHICS == "ethics"
    assert PhilosophicalDomain.QUANTUM == "quantum_mechanics"


def test_model_role_enum():
    """Test ModelRole enum"""
    assert ModelRole.GENERATOR == "generator"
    assert ModelRole.CRITIC == "critic"
    assert ModelRole.VALIDATOR == "validator"


def test_philosophical_position_creation():
    """Test creating a PhilosophicalPosition"""
    position = PhilosophicalPosition(
        problem="Test problem",
        position="Test position statement",
        domains=[PhilosophicalDomain.METAPHYSICS],
        assumptions=["Assumption 1", "Assumption 2"],
        testable_predictions=["Prediction 1", "Prediction 2"],
    )
    
    assert position.problem == "Test problem"
    assert position.position == "Test position statement"
    assert len(position.domains) == 1
    assert len(position.assumptions) == 2
    assert len(position.testable_predictions) == 2
    assert position.id is None
    assert isinstance(position.created_at, datetime)


def test_critique_creation():
    """Test creating a Critique"""
    critique = Critique(
        position_id="test-pos-1",
        model="test-model",
        role=ModelRole.CRITIC,
        logical_consistency=0.8,
        identified_flaws=["Flaw 1", "Flaw 2"],
        novelty_assessment=0.7,
    )
    
    assert critique.position_id == "test-pos-1"
    assert critique.model == "test-model"
    assert critique.role == ModelRole.CRITIC
    assert critique.logical_consistency == 0.8
    assert critique.novelty_assessment == 0.7
    assert len(critique.identified_flaws) == 2


def test_critique_score_validation():
    """Test that critique scores are validated"""
    # Valid scores
    critique = Critique(
        position_id="test",
        model="test",
        role=ModelRole.CRITIC,
        logical_consistency=0.5,
        novelty_assessment=1.0,
    )
    assert critique.logical_consistency == 0.5
    
    # Invalid scores should raise error
    with pytest.raises(ValueError):
        Critique(
            position_id="test",
            model="test",
            role=ModelRole.CRITIC,
            logical_consistency=1.5,  # > 1.0
        )


def test_consensus_result_creation():
    """Test creating a ConsensusResult"""
    consensus = ConsensusResult(
        position_id="test-pos-1",
        unanimous_validity=True,
        average_novelty=0.75,
        testable_predictions_count=3,
        coherence_agreement=4,
        decision="ACCEPT",
        reasons=["Good logic", "High novelty"],
        participating_models=["model1", "model2"],
    )
    
    assert consensus.position_id == "test-pos-1"
    assert consensus.unanimous_validity is True
    assert consensus.average_novelty == 0.75
    assert consensus.decision == "ACCEPT"
    assert len(consensus.reasons) == 2


def test_generation_request_defaults():
    """Test GenerationRequest default values"""
    request = GenerationRequest(
        problem="Test problem",
    )
    
    assert request.problem == "Test problem"
    assert request.domains == []
    assert request.constraints == []
    assert request.existing_solutions == []
    assert request.temperature == 0.7


def test_generation_request_with_values():
    """Test GenerationRequest with all values"""
    request = GenerationRequest(
        problem="Test problem",
        domains=[PhilosophicalDomain.ETHICS],
        constraints=["Constraint 1"],
        existing_solutions=["Solution 1"],
        temperature=0.8,
    )
    
    assert len(request.domains) == 1
    assert len(request.constraints) == 1
    assert request.temperature == 0.8


def test_debate_session_creation():
    """Test creating a DebateSession"""
    position = PhilosophicalPosition(
        problem="Test",
        position="Test position",
        domains=[PhilosophicalDomain.LOGIC],
    )
    
    session = DebateSession(
        id="test-session-1",
        position=position,
        max_iterations=5,
    )
    
    assert session.id == "test-session-1"
    assert session.position == position
    assert session.iterations == 0
    assert session.max_iterations == 5
    assert session.converged is False
    assert len(session.critiques) == 0
    assert session.final_consensus is None
