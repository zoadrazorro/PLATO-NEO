"""
Metaluminous Engine - Main Orchestration Pipeline
"""
import uuid
from typing import Optional, List
from loguru import logger

from ..models import (
    GenerationRequest,
    PhilosophicalPosition,
    DebateSession,
    ConsensusResult,
)
from .generation import GenerationEngine
from .tribunal import PhilosophicalTribunal
from .consensus import ConsensusBuilder
from ..api.four_sages import FourSageCouncil
from ..config import settings


class MetaluminousEngine:
    """
    Main orchestration engine for the Metaluminous system.
    
    Implements the core loop:
    GENERATION → LOCAL CRITIQUE → MULTI-MODEL REFINEMENT → VALIDATION → SYNTHESIS
    """
    
    def __init__(self):
        self.generator = GenerationEngine()
        self.tribunal = PhilosophicalTribunal()
        self.consensus_builder = ConsensusBuilder()
        self.four_sages = FourSageCouncil()
    
    async def process_problem(
        self,
        request: GenerationRequest,
        use_cloud_apis: bool = True,
    ) -> DebateSession:
        """
        Process a philosophical problem through the full pipeline.
        
        Args:
            request: GenerationRequest with problem and constraints
            use_cloud_apis: Whether to use cloud APIs (Four Sages)
            
        Returns:
            DebateSession with complete debate history and consensus
        """
        logger.info(f"Processing problem: {request.problem[:100]}...")
        
        # Create debate session
        session_id = str(uuid.uuid4())
        
        # Phase 1: Generation
        logger.info("Phase 1: Generation")
        position = await self.generator.generate_position(request)
        position.id = f"{session_id}-pos-0"
        
        # Initialize debate session
        session = DebateSession(
            id=session_id,
            position=position,
            max_iterations=settings.max_iterations,
        )
        
        # Phase 2: Local Critique (Philosophical Tribunal)
        logger.info("Phase 2: Local Critique (Tribunal)")
        local_critiques = await self.tribunal.run_tribunal(position)
        session.critiques.extend(local_critiques)
        
        # Phase 3: Multi-Model Refinement (Optional - Four Sages)
        cloud_critiques = []
        if use_cloud_apis:
            logger.info("Phase 3: Cloud Refinement (Four Sages)")
            try:
                cloud_critiques = await self.four_sages.refine_position(
                    position,
                    local_critiques
                )
                session.critiques.extend(cloud_critiques)
            except Exception as e:
                logger.error(f"Four Sages failed: {e}")
                logger.info("Continuing with local critiques only")
        
        # Phase 4: Validation (Consensus Building)
        logger.info("Phase 4: Validation (Consensus)")
        consensus = await self.consensus_builder.build_consensus(
            position,
            session.critiques
        )
        session.final_consensus = consensus
        
        # Phase 5: Iteration if needed
        if consensus.decision == "REVISE" and session.iterations < session.max_iterations:
            logger.info(f"Phase 5: Iteration {session.iterations + 1}")
            session = await self._iterate_position(session, request, use_cloud_apis)
        else:
            session.converged = True
        
        logger.info(f"Processing complete. Final decision: {consensus.decision}")
        return session
    
    async def _iterate_position(
        self,
        session: DebateSession,
        original_request: GenerationRequest,
        use_cloud_apis: bool,
    ) -> DebateSession:
        """
        Iterate on a position based on critiques.
        
        This creates a revised position incorporating feedback.
        """
        session.iterations += 1
        logger.info(f"Iteration {session.iterations}/{session.max_iterations}")
        
        # Create refinement prompt incorporating critiques
        critique_summary = self._summarize_critiques(session.critiques)
        
        refined_request = GenerationRequest(
            problem=f"{original_request.problem}\n\nPREVIOUS ATTEMPT:\n{session.position.position}\n\nCRITIQUES TO ADDRESS:\n{critique_summary}",
            domains=original_request.domains,
            constraints=original_request.constraints + [
                "Address all critiques from previous iteration",
                "Maintain strengths while fixing weaknesses"
            ],
            existing_solutions=original_request.existing_solutions,
            temperature=original_request.temperature * 0.9,  # Slightly lower temp
        )
        
        # Generate revised position
        revised_position = await self.generator.generate_position(refined_request)
        revised_position.id = f"{session.id}-pos-{session.iterations}"
        
        # Update session
        session.position = revised_position
        
        # Re-run critiques
        new_local_critiques = await self.tribunal.run_tribunal(revised_position)
        session.critiques = new_local_critiques  # Replace old critiques
        
        if use_cloud_apis:
            try:
                new_cloud_critiques = await self.four_sages.refine_position(
                    revised_position,
                    new_local_critiques
                )
                session.critiques.extend(new_cloud_critiques)
            except Exception as e:
                logger.error(f"Four Sages failed on iteration: {e}")
        
        # Re-build consensus
        new_consensus = await self.consensus_builder.build_consensus(
            revised_position,
            session.critiques
        )
        session.final_consensus = new_consensus
        
        # Check if we should iterate again
        if new_consensus.decision == "REVISE" and session.iterations < session.max_iterations:
            return await self._iterate_position(session, original_request, use_cloud_apis)
        else:
            session.converged = True
            return session
    
    def _summarize_critiques(self, critiques) -> str:
        """Summarize critiques for refinement prompt"""
        summary = []
        
        for critique in critiques:
            if critique.identified_flaws:
                summary.append(f"- {critique.model}: {len(critique.identified_flaws)} flaws identified")
                for flaw in critique.identified_flaws[:3]:
                    summary.append(f"  • {flaw}")
            
            if critique.contradictions_found:
                summary.append(f"- {critique.model}: Contradictions found")
                for contradiction in critique.contradictions_found[:2]:
                    summary.append(f"  • {contradiction}")
            
            if critique.suggestions:
                summary.append(f"- {critique.model}: Suggestions")
                for suggestion in critique.suggestions[:2]:
                    summary.append(f"  • {suggestion}")
        
        return "\n".join(summary) if summary else "No critiques available"
    
    async def explore_problem_space(
        self,
        request: GenerationRequest,
        num_variations: int = 10,
        use_cloud_apis: bool = False,
    ) -> List[DebateSession]:
        """
        Explore the problem space by generating multiple variations.
        
        This implements combinatorial exploration.
        """
        logger.info(f"Exploring problem space with {num_variations} variations")
        
        # Generate variations
        positions = await self.generator.generate_variations(request, num_variations)
        
        # Process each position
        sessions = []
        for i, position in enumerate(positions):
            logger.info(f"Processing variation {i+1}/{num_variations}")
            
            # Create mini-request for this position
            mini_request = GenerationRequest(
                problem=request.problem,
                domains=request.domains,
                constraints=request.constraints,
            )
            
            # We'll create a simpler session without full iteration
            session_id = str(uuid.uuid4())
            position.id = f"{session_id}-pos-0"
            
            # Run tribunal only (skip cloud APIs and iteration for exploration)
            local_critiques = await self.tribunal.run_tribunal(position)
            
            consensus = await self.consensus_builder.build_consensus(
                position,
                local_critiques
            )
            
            session = DebateSession(
                id=session_id,
                position=position,
                critiques=local_critiques,
                final_consensus=consensus,
                converged=True,
            )
            
            sessions.append(session)
        
        # Sort by consensus quality
        sessions.sort(
            key=lambda s: (
                s.final_consensus.unanimous_validity,
                s.final_consensus.average_novelty
            ),
            reverse=True
        )
        
        logger.info(f"Exploration complete. Top novelty: {sessions[0].final_consensus.average_novelty:.2f}")
        return sessions
