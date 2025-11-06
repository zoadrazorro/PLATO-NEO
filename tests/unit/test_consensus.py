"""
Unit tests for consensus building
"""
import pytest

from metaluminous.models import (
    PhilosophicalPosition,
    Critique,
    ModelRole,
    PhilosophicalDomain,
)
from metaluminous.core.consensus import ConsensusBuilder


@pytest.fixture
def sample_position():
    """Create a sample philosophical position"""
    return PhilosophicalPosition(
        id="test-pos-1",
        problem="Test problem",
        position="Test position statement",
        domains=[PhilosophicalDomain.METAPHYSICS],
        testable_predictions=["Prediction 1", "Prediction 2", "Prediction 3"],
    )


@pytest.fixture
def valid_critiques():
    """Create valid critiques (all passing)"""
    return [
        Critique(
            position_id="test-pos-1",
            model="model1",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.8,
        ),
        Critique(
            position_id="test-pos-1",
            model="model2",
            role=ModelRole.VALIDATOR,
            logical_consistency=0.85,
            novelty_assessment=0.75,
        ),
        Critique(
            position_id="test-pos-1",
            model="model3",
            role=ModelRole.REFINER,
            logical_consistency=0.8,
            novelty_assessment=0.8,
        ),
    ]


@pytest.mark.asyncio
async def test_consensus_accept(sample_position, valid_critiques):
    """Test consensus with acceptable position"""
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(sample_position, valid_critiques)
    
    assert consensus.decision == "ACCEPT"
    assert consensus.unanimous_validity is True
    assert consensus.average_novelty > 0.7
    assert consensus.testable_predictions_count == 3


@pytest.mark.asyncio
async def test_consensus_reject_logic():
    """Test consensus rejection due to logical flaw"""
    position = PhilosophicalPosition(
        id="test-pos-1",
        problem="Test",
        position="Test",
        domains=[PhilosophicalDomain.LOGIC],
        testable_predictions=["Pred 1", "Pred 2"],
    )
    
    critiques = [
        Critique(
            position_id="test-pos-1",
            model="model1",
            role=ModelRole.CRITIC,
            logical_consistency=0.5,  # Below threshold
        ),
    ]
    
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(position, critiques)
    
    assert consensus.decision == "REJECT"
    assert consensus.unanimous_validity is False


@pytest.mark.asyncio
async def test_consensus_reject_novelty():
    """Test consensus rejection due to low novelty"""
    position = PhilosophicalPosition(
        id="test-pos-1",
        problem="Test",
        position="Test",
        domains=[PhilosophicalDomain.ETHICS],
        testable_predictions=["Pred 1", "Pred 2"],
    )
    
    critiques = [
        Critique(
            position_id="test-pos-1",
            model="model1",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.3,  # Low novelty
        ),
    ]
    
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(position, critiques)
    
    assert consensus.decision == "REJECT"
    assert any("novelty" in r.lower() for r in consensus.reasons)


@pytest.mark.asyncio
async def test_consensus_reject_predictions():
    """Test consensus rejection due to insufficient predictions"""
    position = PhilosophicalPosition(
        id="test-pos-1",
        problem="Test",
        position="Test",
        domains=[PhilosophicalDomain.CONSCIOUSNESS],
        testable_predictions=["Only one prediction"],  # Only 1, need 2
    )
    
    critiques = [
        Critique(
            position_id="test-pos-1",
            model="model1",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.8,
        ),
    ]
    
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(position, critiques)
    
    assert consensus.decision == "REJECT"
    assert any("prediction" in r.lower() for r in consensus.reasons)


@pytest.mark.asyncio
async def test_consensus_revise_contradictions():
    """Test consensus revision due to contradictions"""
    position = PhilosophicalPosition(
        id="test-pos-1",
        problem="Test",
        position="Test",
        domains=[PhilosophicalDomain.LOGIC],
        testable_predictions=["Pred 1", "Pred 2"],
    )
    
    critiques = [
        Critique(
            position_id="test-pos-1",
            model="model1",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.8,
            contradictions_found=["Contradiction 1"],
        ),
        Critique(
            position_id="test-pos-1",
            model="model2",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.8,
        ),
        Critique(
            position_id="test-pos-1",
            model="model3",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
            novelty_assessment=0.8,
        ),
    ]
    
    builder = ConsensusBuilder()
    consensus = await builder.build_consensus(position, critiques)
    
    assert consensus.decision == "REVISE"
    assert any("contradiction" in r.lower() for r in consensus.reasons)


def test_check_unanimous_validity():
    """Test unanimous validity check"""
    builder = ConsensusBuilder()
    
    # All valid
    critiques = [
        Critique(
            position_id="test",
            model="m1",
            role=ModelRole.CRITIC,
            logical_consistency=0.8,
        ),
        Critique(
            position_id="test",
            model="m2",
            role=ModelRole.CRITIC,
            logical_consistency=0.9,
        ),
    ]
    assert builder._check_unanimous_validity(critiques) is True
    
    # One invalid
    critiques.append(
        Critique(
            position_id="test",
            model="m3",
            role=ModelRole.CRITIC,
            logical_consistency=0.5,
        )
    )
    assert builder._check_unanimous_validity(critiques) is False


def test_calculate_average_novelty():
    """Test average novelty calculation"""
    builder = ConsensusBuilder()
    
    critiques = [
        Critique(
            position_id="test",
            model="m1",
            role=ModelRole.CRITIC,
            logical_consistency=0.8,
            novelty_assessment=0.8,
        ),
        Critique(
            position_id="test",
            model="m2",
            role=ModelRole.CRITIC,
            logical_consistency=0.8,
            novelty_assessment=0.6,
        ),
        Critique(
            position_id="test",
            model="m3",
            role=ModelRole.CRITIC,
            logical_consistency=0.8,
            novelty_assessment=None,  # No assessment
        ),
    ]
    
    avg = builder._calculate_average_novelty(critiques)
    assert avg == 0.7  # (0.8 + 0.6) / 2
