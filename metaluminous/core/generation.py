"""
Metaluminous Engine - Generation Engine
"""
import asyncio
from typing import List, Optional, Dict, Any
from loguru import logger

from ..models import PhilosophicalPosition, GenerationRequest, PhilosophicalDomain
from ..prompts import GENERATION_PROMPT, METALUMINOSITY_FRAMEWORK
from ..api.llm_clients import OllamaClient
from ..config import settings


class GenerationEngine:
    """Core engine for generating philosophical positions"""
    
    def __init__(self):
        self.ollama_client = OllamaClient()
        
    async def generate_position(
        self,
        request: GenerationRequest
    ) -> PhilosophicalPosition:
        """
        Generate a novel philosophical position based on the request.
        
        Args:
            request: GenerationRequest with problem, constraints, etc.
            
        Returns:
            PhilosophicalPosition with generated content
        """
        logger.info(f"Generating position for problem: {request.problem[:100]}...")
        
        # Format the generation prompt
        prompt = GENERATION_PROMPT.format(
            metaluminosity_framework=METALUMINOSITY_FRAMEWORK,
            problem=request.problem,
            existing_solutions="\n- ".join(request.existing_solutions) if request.existing_solutions else "None specified",
        )
        
        # Generate using Ollama
        response = await self.ollama_client.generate(
            model=settings.ollama_primary_model,
            prompt=prompt,
            temperature=request.temperature,
        )
        
        # Parse response into structured position
        position = self._parse_generation_response(response, request)
        
        logger.info(f"Generated position with {len(position.testable_predictions)} predictions")
        return position
    
    def _parse_generation_response(
        self,
        response: str,
        request: GenerationRequest
    ) -> PhilosophicalPosition:
        """
        Parse LLM response into PhilosophicalPosition structure.
        
        This is a simplified parser. In production, you might want to use
        more sophisticated parsing or enforce JSON output from the LLM.
        """
        # Extract sections (simplified parsing)
        sections = self._extract_sections(response)
        
        return PhilosophicalPosition(
            problem=request.problem,
            position=sections.get("position_statement", response[:500]),
            domains=request.domains or [PhilosophicalDomain.METAPHYSICS],
            assumptions=sections.get("assumptions", []),
            testable_predictions=sections.get("predictions", []),
            contradictions=sections.get("contradictions", []),
            metadata={
                "raw_response": response,
                "temperature": request.temperature,
                "constraints": request.constraints,
            }
        )
    
    def _extract_sections(self, response: str) -> Dict[str, Any]:
        """Extract structured sections from generation response"""
        sections = {}
        
        # Simple section extraction (can be improved)
        lines = response.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'position statement' in line_lower:
                if current_section:
                    sections[current_section] = current_content
                current_section = 'position_statement'
                current_content = []
            elif 'assumptions' in line_lower or 'premise' in line_lower:
                if current_section:
                    sections[current_section] = current_content
                current_section = 'assumptions'
                current_content = []
            elif 'prediction' in line_lower:
                if current_section:
                    sections[current_section] = current_content
                current_section = 'predictions'
                current_content = []
            elif 'contradiction' in line_lower or 'paradox' in line_lower:
                if current_section:
                    sections[current_section] = current_content
                current_section = 'contradictions'
                current_content = []
            else:
                if current_section:
                    current_content.append(line.strip())
        
        if current_section:
            sections[current_section] = current_content
        
        # Clean up sections
        for key in sections:
            if isinstance(sections[key], list):
                # Join for single-value sections, keep as list for multi-value
                if key == 'position_statement':
                    sections[key] = ' '.join(sections[key])
                else:
                    # Filter out empty lines and list markers
                    sections[key] = [
                        item.lstrip('-•*123456789. ').strip()
                        for item in sections[key]
                        if item.strip() and item.strip() not in ['-', '•', '*']
                    ]
        
        return sections
    
    async def generate_variations(
        self,
        base_request: GenerationRequest,
        num_variations: int = 10
    ) -> List[PhilosophicalPosition]:
        """
        Generate multiple variations of philosophical positions.
        
        This implements combinatorial exploration by varying temperature
        and adding random constraints.
        """
        logger.info(f"Generating {num_variations} variations")
        
        tasks = []
        for i in range(num_variations):
            # Vary temperature for diversity
            varied_request = base_request.model_copy()
            varied_request.temperature = 0.5 + (i / num_variations) * 1.0
            
            tasks.append(self.generate_position(varied_request))
        
        positions = await asyncio.gather(*tasks)
        return positions
