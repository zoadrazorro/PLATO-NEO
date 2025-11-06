"""
Metaluminous Engine - Cloud API Integration (Four Sage Council)
"""
import asyncio
from typing import List, Dict, Any
from loguru import logger

from ..models import PhilosophicalPosition, Critique, ModelRole
from ..prompts import CONSENSUS_SYNTHESIS_PROMPT
from .llm_clients import OpenAIClient, AnthropicClient, GoogleClient
from ..config import settings


class FourSageCouncil:
    """
    Multi-model refinement using cloud APIs.
    
    The Four Sages:
    1. Claude (Anthropic) - Deep philosophical analysis
    2. GPT-4 (OpenAI) - Formal logical verification
    3. Gemini (Google) - Interdisciplinary connections
    4. GPT-4o (OpenAI) - Accessibility & synthesis
    """
    
    def __init__(self):
        self.anthropic_client = AnthropicClient()
        self.openai_client = OpenAIClient()
        self.google_client = GoogleClient()
    
    async def refine_position(
        self,
        position: PhilosophicalPosition,
        local_critiques: List[Critique]
    ) -> List[Critique]:
        """
        Run position through the Four Sage Council for refinement.
        
        Args:
            position: The philosophical position to refine
            local_critiques: Critiques from local models
            
        Returns:
            List of critiques from cloud models
        """
        logger.info("Convening the Four Sage Council")
        
        # Run all sages in parallel
        sage_critiques = await asyncio.gather(
            self._claude_analysis(position, local_critiques),
            self._gpt4_verification(position, local_critiques),
            self._gemini_connections(position, local_critiques),
            self._gpt4o_synthesis(position, local_critiques),
            return_exceptions=True
        )
        
        # Filter out any exceptions and log them
        valid_critiques = []
        for i, critique in enumerate(sage_critiques):
            if isinstance(critique, Exception):
                logger.error(f"Sage {i} failed: {critique}")
            else:
                valid_critiques.append(critique)
        
        logger.info(f"Four Sage Council complete: {len(valid_critiques)} critiques")
        return valid_critiques
    
    async def _claude_analysis(
        self,
        position: PhilosophicalPosition,
        local_critiques: List[Critique]
    ) -> Critique:
        """Claude Sonnet: Deep philosophical analysis"""
        logger.debug("Claude: Deep philosophical analysis")
        
        prompt = f"""
        You are Claude, providing deep philosophical analysis.
        
        POSITION:
        {position.position}
        
        LOCAL CRITIQUES SUMMARY:
        {self._summarize_critiques(local_critiques)}
        
        YOUR TASK:
        1. Identify implicit assumptions not yet surfaced
        2. Check coherence with Metaluminosity framework
        3. Rate: Originality (0-1), Rigor (0-1), Relevance (0-1)
        4. Provide philosophical depth analysis
        
        Provide structured analysis.
        """
        
        response = await self.anthropic_client.generate(
            prompt=prompt,
            model=settings.anthropic_model,
            temperature=0.5,
        )
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.anthropic_model,
            role=ModelRole.REFINER,
            logical_consistency=self._extract_score_from_text(response, "rigor"),
            novelty_assessment=self._extract_score_from_text(response, "originality"),
            suggestions=self._extract_suggestions(response),
            metadata={"raw_response": response, "sage": "claude"}
        )
    
    async def _gpt4_verification(
        self,
        position: PhilosophicalPosition,
        local_critiques: List[Critique]
    ) -> Critique:
        """GPT-4: Formal logical verification"""
        logger.debug("GPT-4: Formal logical verification")
        
        prompt = f"""
        You are GPT-4, providing formal logical verification.
        
        POSITION:
        {position.position}
        
        YOUR TASK:
        1. Perform formal logical verification
        2. Create mathematical models where applicable
        3. Cross-reference with academic literature
        4. Generate potential counterexamples
        5. Rate logical consistency (0-1)
        
        Provide structured verification.
        """
        
        response = await self.openai_client.generate(
            prompt=prompt,
            model=settings.openai_model,
            temperature=0.3,
        )
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.openai_model,
            role=ModelRole.VALIDATOR,
            logical_consistency=self._extract_score_from_text(response, "consistency"),
            identified_flaws=self._extract_counterexamples(response),
            metadata={"raw_response": response, "sage": "gpt4"}
        )
    
    async def _gemini_connections(
        self,
        position: PhilosophicalPosition,
        local_critiques: List[Critique]
    ) -> Critique:
        """Gemini: Interdisciplinary connections"""
        logger.debug("Gemini: Interdisciplinary connections")
        
        prompt = f"""
        You are Gemini, identifying interdisciplinary connections.
        
        POSITION:
        {position.position}
        
        YOUR TASK:
        1. Find connections to other scientific domains
        2. Ground in empirical research where possible
        3. Identify practical implications
        4. Suggest alternative framings
        5. Rate interdisciplinary potential (0-1)
        
        Provide structured analysis.
        """
        
        response = await self.google_client.generate(
            prompt=prompt,
            model=settings.google_model,
            temperature=0.6,
        )
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.google_model,
            role=ModelRole.CREATIVE,
            logical_consistency=0.8,  # Neutral
            suggestions=self._extract_suggestions(response),
            metadata={"raw_response": response, "sage": "gemini"}
        )
    
    async def _gpt4o_synthesis(
        self,
        position: PhilosophicalPosition,
        local_critiques: List[Critique]
    ) -> Critique:
        """GPT-4o: Accessibility and synthesis"""
        logger.debug("GPT-4o: Accessibility and synthesis")
        
        prompt = f"""
        You are GPT-4o, assessing accessibility and practical integration.
        
        POSITION:
        {position.position}
        
        YOUR TASK:
        1. Assess public comprehensibility
        2. Identify practical applications
        3. Check integration with existing knowledge
        4. Suggest improvements for clarity
        5. Rate accessibility (0-1)
        
        Provide structured assessment.
        """
        
        response = await self.openai_client.generate(
            prompt=prompt,
            model="gpt-4o",
            temperature=0.5,
        )
        
        return Critique(
            position_id=position.id or "unknown",
            model="gpt-4o",
            role=ModelRole.REFINER,
            logical_consistency=0.8,  # Neutral
            suggestions=self._extract_suggestions(response),
            metadata={"raw_response": response, "sage": "gpt4o"}
        )
    
    def _summarize_critiques(self, critiques: List[Critique]) -> str:
        """Summarize local critiques for context"""
        if not critiques:
            return "No local critiques available."
        
        summary = []
        for c in critiques:
            summary.append(f"- {c.model} ({c.role}): Logic={c.logical_consistency:.2f}")
            if c.identified_flaws:
                summary.append(f"  Flaws: {len(c.identified_flaws)}")
        
        return "\n".join(summary)
    
    def _extract_score_from_text(self, text: str, score_name: str) -> float:
        """Extract a named score from text"""
        import re
        
        # Look for patterns like "Rigor: 0.8" or "Originality: 8/10"
        pattern = rf'{score_name}[:\s]+(\d*\.?\d+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            value = float(match.group(1))
            # Normalize to 0-1 if needed
            if value > 1:
                value = value / 10.0
            return value
        
        return 0.5  # Default
    
    def _extract_suggestions(self, text: str) -> List[str]:
        """Extract suggestions from text"""
        suggestions = []
        lines = text.split('\n')
        
        in_suggestions = False
        for line in lines:
            if 'suggest' in line.lower() or 'improv' in line.lower():
                in_suggestions = True
                continue
            
            if in_suggestions and line.strip().startswith(('-', '•', '*', '1', '2', '3')):
                suggestion = line.strip().lstrip('-•*123456789. ')
                if suggestion:
                    suggestions.append(suggestion)
        
        return suggestions[:5]
    
    def _extract_counterexamples(self, text: str) -> List[str]:
        """Extract counterexamples from text"""
        examples = []
        lines = text.split('\n')
        
        for line in lines:
            if 'counter' in line.lower() or 'example' in line.lower():
                if line.strip().startswith(('-', '•', '*', '1', '2', '3')):
                    example = line.strip().lstrip('-•*123456789. ')
                    if example:
                        examples.append(example)
        
        return examples[:5]
