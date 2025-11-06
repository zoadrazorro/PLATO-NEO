"""
Metaluminous Engine - Consensus Building
"""
from typing import List
from loguru import logger

from ..models import ConsensusResult, Critique, PhilosophicalPosition
from ..config import settings


class ConsensusBuilder:
    """Build consensus from multiple model critiques"""
    
    async def build_consensus(
        self,
        position: PhilosophicalPosition,
        critiques: List[Critique]
    ) -> ConsensusResult:
        """
        Build consensus from multiple critiques.
        
        Args:
            position: The philosophical position being evaluated
            critiques: List of critiques from different models
            
        Returns:
            ConsensusResult with final decision
        """
        logger.info(f"Building consensus from {len(critiques)} critiques")
        
        # Check unanimous logical validity
        unanimous_validity = self._check_unanimous_validity(critiques)
        
        # Calculate average novelty
        average_novelty = self._calculate_average_novelty(critiques)
        
        # Count testable predictions
        testable_count = len(position.testable_predictions)
        
        # Count coherence agreement
        coherence_agreement = self._count_coherence_agreement(critiques)
        
        # Make decision
        decision, reasons = self._make_decision(
            unanimous_validity,
            average_novelty,
            testable_count,
            coherence_agreement,
            critiques
        )
        
        participating_models = list(set(c.model for c in critiques))
        
        return ConsensusResult(
            position_id=position.id or "unknown",
            unanimous_validity=unanimous_validity,
            average_novelty=average_novelty,
            testable_predictions_count=testable_count,
            coherence_agreement=coherence_agreement,
            decision=decision,
            reasons=reasons,
            participating_models=participating_models,
        )
    
    def _check_unanimous_validity(self, critiques: List[Critique]) -> bool:
        """Check if all models agree on logical validity"""
        if not critiques:
            return False
        
        # Consider valid if all critiques have logical_consistency > 0.7
        return all(c.logical_consistency >= 0.7 for c in critiques)
    
    def _calculate_average_novelty(self, critiques: List[Critique]) -> float:
        """Calculate average novelty score across critiques"""
        novelty_scores = [
            c.novelty_assessment
            for c in critiques
            if c.novelty_assessment is not None
        ]
        
        if not novelty_scores:
            return 0.5  # Default to neutral
        
        return sum(novelty_scores) / len(novelty_scores)
    
    def _count_coherence_agreement(self, critiques: List[Critique]) -> int:
        """Count how many models agree on coherence"""
        # Models agree on coherence if logical_consistency > 0.7
        return sum(1 for c in critiques if c.logical_consistency >= 0.7)
    
    def _make_decision(
        self,
        unanimous_validity: bool,
        average_novelty: float,
        testable_count: int,
        coherence_agreement: int,
        critiques: List[Critique]
    ) -> tuple[str, List[str]]:
        """
        Make final decision based on consensus metrics.
        
        Returns:
            Tuple of (decision, reasons)
        """
        reasons = []
        
        # Check logical validity (must be unanimous)
        if not unanimous_validity:
            return "REJECT", ["Logical flaw detected by one or more models"]
        
        reasons.append("All models agree on logical validity")
        
        # Check novelty threshold
        if average_novelty < settings.novelty_threshold:
            return "REJECT", reasons + [
                f"Insufficient novelty: {average_novelty:.2f} < {settings.novelty_threshold}"
            ]
        
        reasons.append(f"Novelty score: {average_novelty:.2f}")
        
        # Check testable predictions
        if testable_count < settings.min_testable_predictions:
            return "REJECT", reasons + [
                f"Insufficient testable predictions: {testable_count} < {settings.min_testable_predictions}"
            ]
        
        reasons.append(f"{testable_count} testable predictions provided")
        
        # Check coherence agreement (at least 3/4 of models)
        required_agreement = max(3, len(critiques) * 3 // 4)
        if coherence_agreement < required_agreement:
            return "REVISE", reasons + [
                f"Insufficient coherence agreement: {coherence_agreement}/{len(critiques)} models"
            ]
        
        reasons.append(f"Coherence agreement: {coherence_agreement}/{len(critiques)} models")
        
        # Check for critical flaws
        critical_flaws = []
        for critique in critiques:
            if critique.contradictions_found:
                critical_flaws.extend(critique.contradictions_found)
        
        if critical_flaws:
            return "REVISE", reasons + [
                f"Critical contradictions found: {len(critical_flaws)}"
            ]
        
        # All checks passed
        return "ACCEPT", reasons + ["All criteria met for acceptance"]
