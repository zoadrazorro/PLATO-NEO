#!/usr/bin/env python3
"""
Example: Generate a philosophical position on consciousness

This example demonstrates the basic usage of the Metaluminous Engine.
"""
import asyncio
from metaluminous.core import MetaluminousEngine
from metaluminous.models import GenerationRequest, PhilosophicalDomain


async def main():
    """Run example generation"""
    print("=== Metaluminous Engine Example ===\n")
    
    # Initialize engine
    print("Initializing engine...")
    engine = MetaluminousEngine()
    
    # Create a generation request
    request = GenerationRequest(
        problem="How can consciousness arise from physical processes?",
        domains=[
            PhilosophicalDomain.CONSCIOUSNESS,
            PhilosophicalDomain.METAPHYSICS
        ],
        constraints=[
            "Must avoid simple emergence arguments",
            "Must provide testable predictions",
            "Must address the explanatory gap"
        ],
        existing_solutions=[
            "Functionalism",
            "Identity Theory",
            "Integrated Information Theory"
        ],
        temperature=0.7
    )
    
    print(f"\nProblem: {request.problem}")
    print(f"Domains: {', '.join(d.value for d in request.domains)}")
    print(f"Constraints: {len(request.constraints)}")
    print("\nProcessing (this may take a few minutes)...\n")
    
    # Process the problem (using local models only in this example)
    try:
        session = await engine.process_problem(
            request,
            use_cloud_apis=False  # Set to True if you have API keys configured
        )
        
        # Display results
        print("=== RESULTS ===\n")
        print(f"Session ID: {session.id}")
        print(f"Iterations: {session.iterations}")
        print(f"Converged: {session.converged}")
        print()
        
        print("=== POSITION ===")
        print(session.position.position)
        print()
        
        if session.position.testable_predictions:
            print("=== TESTABLE PREDICTIONS ===")
            for i, pred in enumerate(session.position.testable_predictions, 1):
                print(f"{i}. {pred}")
            print()
        
        if session.position.assumptions:
            print("=== KEY ASSUMPTIONS ===")
            for i, assumption in enumerate(session.position.assumptions, 1):
                print(f"{i}. {assumption}")
            print()
        
        print("=== CONSENSUS ===")
        print(f"Decision: {session.final_consensus.decision}")
        print(f"Novelty Score: {session.final_consensus.average_novelty:.2f}")
        print(f"Unanimous Validity: {session.final_consensus.unanimous_validity}")
        print(f"Testable Predictions: {session.final_consensus.testable_predictions_count}")
        print(f"Coherence Agreement: {session.final_consensus.coherence_agreement}/{len(session.critiques)}")
        print()
        
        if session.final_consensus.reasons:
            print("=== REASONING ===")
            for reason in session.final_consensus.reasons:
                print(f"- {reason}")
            print()
        
        print("=== CRITIQUES ===")
        print(f"Total critiques: {len(session.critiques)}")
        for critique in session.critiques:
            print(f"\n{critique.model} ({critique.role.value}):")
            print(f"  Logical Consistency: {critique.logical_consistency:.2f}")
            if critique.novelty_assessment:
                print(f"  Novelty Assessment: {critique.novelty_assessment:.2f}")
            if critique.identified_flaws:
                print(f"  Flaws Identified: {len(critique.identified_flaws)}")
        
        print("\n=== COMPLETE ===")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Docker services are running (docker-compose up -d)")
        print("2. Ollama is installed and running")
        print("3. Models are pulled (see README.md)")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
