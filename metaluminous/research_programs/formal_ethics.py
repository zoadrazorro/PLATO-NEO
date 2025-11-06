"""
Research Program 2: Formal Ethics from First Principles

Goal: Derive ethical framework directly from information theory + consciousness
"""
from loguru import logger

from ..models import GenerationRequest, PhilosophicalDomain
from ..core import MetaluminousEngine
from ..prompts import FORMAL_ETHICS_TEMPLATE


class FormalEthicsProgram:
    """
    Research program to derive ethics from information theory and consciousness.
    """
    
    def __init__(self):
        self.engine = MetaluminousEngine()
        self.goal = "Derive ethical framework directly from information theory + consciousness"
    
    async def run(self) -> dict:
        """
        Execute the research program.
        
        Returns:
            Dictionary with formal ethics framework
        """
        logger.info("Starting Formal Ethics from First Principles program")
        
        request = GenerationRequest(
            problem=FORMAL_ETHICS_TEMPLATE.format(goal=self.goal),
            domains=[PhilosophicalDomain.ETHICS, PhilosophicalDomain.CONSCIOUSNESS],
            constraints=[
                "Must formalize 'suffering = information incoherence' mathematically",
                "Must derive principles as optimization constraints",
                "Must compare to utilitarianism, deontology, virtue ethics",
                "Must identify novel moral duties regarding AI",
            ],
            innovation_vectors=[
                "Apply information theory formally",
                "Use computational models",
                "Ground in consciousness science",
            ],
            temperature=0.7,
        )
        
        # Process with cloud APIs for deeper analysis
        session = await self.engine.process_problem(request, use_cloud_apis=True)
        
        results = {
            "program": "Formal Ethics from First Principles",
            "position": session.position.position,
            "formal_structure": self._extract_formal_structure(session.position.position),
            "ethical_principles": self._extract_principles(session.position.position),
            "ai_moral_duties": self._extract_ai_duties(session.position.position),
            "consensus": {
                "decision": session.final_consensus.decision,
                "novelty": session.final_consensus.average_novelty,
                "reasoning": session.final_consensus.reasons,
            }
        }
        
        return results
    
    def _extract_formal_structure(self, text: str) -> list:
        """Extract formal mathematical structures from text"""
        # Simple extraction - look for equations or formulas
        import re
        structures = []
        
        # Look for lines with mathematical notation
        for line in text.split('\n'):
            if any(symbol in line for symbol in ['=', '∈', '∀', '∃', '→', '≤', '≥']):
                structures.append(line.strip())
        
        return structures[:10]
    
    def _extract_principles(self, text: str) -> list:
        """Extract ethical principles from text"""
        principles = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if 'principle' in line.lower():
                # Get next few lines as the principle
                principle_text = line.strip()
                if i + 1 < len(lines):
                    principle_text += " " + lines[i + 1].strip()
                principles.append(principle_text)
        
        return principles[:5]
    
    def _extract_ai_duties(self, text: str) -> list:
        """Extract AI-specific moral duties"""
        duties = []
        lines = text.split('\n')
        
        in_ai_section = False
        for line in lines:
            if 'ai' in line.lower() and 'dut' in line.lower():
                in_ai_section = True
            
            if in_ai_section and line.strip().startswith(('-', '•', '*', '1', '2', '3')):
                duty = line.strip().lstrip('-•*123456789. ')
                if duty:
                    duties.append(duty)
        
        return duties[:5]
