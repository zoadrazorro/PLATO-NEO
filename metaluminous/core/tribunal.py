"""
Metaluminous Engine - Philosophical Tribunal (Multi-Model Debate)
"""
import asyncio
from typing import List
from loguru import logger

from ..models import PhilosophicalPosition, Critique, ModelRole
from ..prompts import (
    LOGIC_CHECK_PROMPT,
    CONTRADICTION_FINDER_PROMPT,
    NOVELTY_ASSESSMENT_PROMPT,
    EDGE_CASE_GENERATOR_PROMPT,
)
from ..api.llm_clients import OllamaClient
from ..config import settings


class PhilosophicalTribunal:
    """Multi-model debate system for critiquing philosophical positions"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
    
    async def run_tribunal(
        self,
        position: PhilosophicalPosition
    ) -> List[Critique]:
        """
        Run a position through multiple models for critique.
        
        Args:
            position: The philosophical position to critique
            
        Returns:
            List of critiques from different models/perspectives
        """
        logger.info(f"Running tribunal for position: {position.id or 'new'}")
        
        # Run all critiques in parallel
        critiques = await asyncio.gather(
            self._check_logic(position),
            self._find_contradictions(position),
            self._assess_novelty(position),
            self._generate_edge_cases(position),
        )
        
        logger.info(f"Tribunal complete: {len(critiques)} critiques generated")
        return critiques
    
    async def _check_logic(self, position: PhilosophicalPosition) -> Critique:
        """Check logical consistency of the position"""
        logger.debug("Checking logical consistency")
        
        prompt = LOGIC_CHECK_PROMPT.format(position=position.position)
        
        response = await self.ollama_client.generate(
            model=settings.ollama_primary_model,
            prompt=prompt,
            temperature=0.3,  # Lower temperature for logical analysis
        )
        
        # Parse response to extract score and findings
        logic_score = self._extract_score(response)
        flaws = self._extract_list_items(response, ["flaw", "issue", "problem"])
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.ollama_primary_model,
            role=ModelRole.CRITIC,
            logical_consistency=logic_score,
            identified_flaws=flaws,
            metadata={"raw_response": response}
        )
    
    async def _find_contradictions(self, position: PhilosophicalPosition) -> Critique:
        """Find contradictions in the position"""
        logger.debug("Finding contradictions")
        
        prompt = CONTRADICTION_FINDER_PROMPT.format(position=position.position)
        
        response = await self.ollama_client.generate(
            model=settings.ollama_critic_model,
            prompt=prompt,
            temperature=0.4,
        )
        
        contradictions = self._extract_list_items(response, ["contradiction", "paradox", "tension"])
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.ollama_critic_model,
            role=ModelRole.CRITIC,
            logical_consistency=1.0 if not contradictions else 0.5,
            contradictions_found=contradictions,
            metadata={"raw_response": response}
        )
    
    async def _assess_novelty(self, position: PhilosophicalPosition) -> Critique:
        """Assess novelty compared to existing literature"""
        logger.debug("Assessing novelty")
        
        prompt = NOVELTY_ASSESSMENT_PROMPT.format(position=position.position)
        
        response = await self.ollama_client.generate(
            model=settings.ollama_primary_model,
            prompt=prompt,
            temperature=0.5,
        )
        
        novelty_score = self._extract_score(response)
        suggestions = self._extract_list_items(response, ["suggest", "recommend", "improve"])
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.ollama_primary_model,
            role=ModelRole.VALIDATOR,
            logical_consistency=0.8,  # Neutral for novelty check
            novelty_assessment=novelty_score,
            suggestions=suggestions,
            metadata={"raw_response": response}
        )
    
    async def _generate_edge_cases(self, position: PhilosophicalPosition) -> Critique:
        """Generate edge cases to test the position"""
        logger.debug("Generating edge cases")
        
        prompt = EDGE_CASE_GENERATOR_PROMPT.format(position=position.position)
        
        response = await self.ollama_client.generate(
            model=settings.ollama_creative_model,
            prompt=prompt,
            temperature=0.8,  # Higher temperature for creative test generation
        )
        
        test_cases = self._extract_list_items(response, ["case", "scenario", "test", "example"])
        
        return Critique(
            position_id=position.id or "unknown",
            model=settings.ollama_creative_model,
            role=ModelRole.CREATIVE,
            logical_consistency=0.8,  # Neutral
            identified_flaws=test_cases[:5],  # Use flaws field for test cases
            metadata={"raw_response": response, "test_cases": test_cases}
        )
    
    def _extract_score(self, text: str) -> float:
        """Extract numerical score from text (0.0 to 1.0)"""
        # Simple extraction - look for patterns like "0.7" or "7/10" or "70%"
        import re
        
        # Look for decimal between 0 and 1
        decimal_match = re.search(r'\b0?\.\d+\b', text)
        if decimal_match:
            return float(decimal_match.group())
        
        # Look for fraction like 7/10
        fraction_match = re.search(r'(\d+)/(\d+)', text)
        if fraction_match:
            num, denom = fraction_match.groups()
            return float(num) / float(denom)
        
        # Look for percentage
        percent_match = re.search(r'(\d+)%', text)
        if percent_match:
            return float(percent_match.group(1)) / 100.0
        
        # Default to 0.5 if no score found
        return 0.5
    
    def _extract_list_items(self, text: str, keywords: List[str]) -> List[str]:
        """Extract list items from text based on keywords"""
        items = []
        lines = text.split('\n')
        
        in_section = False
        for line in lines:
            line_lower = line.lower()
            
            # Check if we're entering a relevant section
            if any(keyword in line_lower for keyword in keywords):
                in_section = True
                continue
            
            # Extract list items
            if in_section and (line.strip().startswith(('-', '•', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9'))):
                item = line.strip().lstrip('-•*123456789. ').strip()
                if item and len(item) > 10:  # Filter very short items
                    items.append(item)
            
            # Stop at empty line after section
            if in_section and not line.strip():
                in_section = False
        
        return items[:10]  # Limit to 10 items
