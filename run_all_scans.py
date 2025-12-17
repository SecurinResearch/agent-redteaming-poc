"""
Main runner script to execute all red-teaming scans
"""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup LiteLLM environment for scanners
from setup_scanner_env import setup_litellm_environment
setup_litellm_environment()

from redteaming.agentic_radar.runner import AgenticRadarRunner
from redteaming.agentfence.runner import AgentFenceRunner
from redteaming.a2a_scanner.runner import A2AScannerRunner
from evaluation.orchestrator import RedTeamOrchestrator
from evaluation.aggregator import ResultsAggregator


def print_header(text: str):
    """Print section header"""
    print("\n" + "="*60)
    print(text)
    print("="*60 + "\n")


def run_custom_attacks():
    """Run custom attack scenarios"""
    print_header("1. RUNNING CUSTOM ATTACK SCENARIOS")

    orchestrator = RedTeamOrchestrator()

    payload_files = [
        "attacks/tool_misuse.json",
        "attacks/harmful_content.json"
    ]

    orchestrator.run_attack_suite(payload_files, evaluate=True)
    orchestrator.print_summary()
    orchestrator.save_results()


def run_agentic_radar():
    """Run Agentic-Radar scans"""
    print_header("2. RUNNING AGENTIC-RADAR SCANNER")

    runner = AgenticRadarRunner()

    # Scan all agents
    runner.scan_all_agents()

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nAgentic-Radar Summary:")
    print(f"  Total scans: {summary['total_scans']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Errors: {summary['errors']}")


def run_agentfence():
    """Run AgentFence probes"""
    print_header("3. RUNNING AGENTFENCE SCANNER")

    runner = AgentFenceRunner()

    # Test all agents
    runner.test_all_agents()

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nAgentFence Summary:")
    print(f"  Total tests: {summary['total_tests']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Errors: {summary['errors']}")


def run_a2a_scanner():
    """Run A2A Scanner"""
    print_header("4. RUNNING A2A SCANNER")

    runner = A2AScannerRunner()

    # Scan all agent cards
    runner.scan_all_agent_cards()

    # Note: Endpoint scanning requires API server running
    print("\n⚠️  Note: Endpoint scanning requires the API server to be running")
    print("To scan endpoints, start the server first: python api_server.py")

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nA2A Scanner Summary:")
    print(f"  Total scans: {summary['total_scans']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Errors: {summary['errors']}")


def aggregate_results():
    """Aggregate all results"""
    print_header("5. AGGREGATING RESULTS")

    aggregator = ResultsAggregator()
    aggregator.aggregate_all()
    aggregator.save_aggregated_results()
    aggregator.print_summary()


def main():
    """Run all scans"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           AI Agent Red-Teaming PoC - Full Suite             ║
╚══════════════════════════════════════════════════════════════╝

This script will run:
  1. Agentic-Radar scanner (static + dynamic analysis)
  2. AgentFence scanner (security probes)
  3. A2A Scanner (protocol compliance)
  4. Results aggregation

Press Ctrl+C to cancel at any time.
""")

    try:
        # Run all scans
        run_custom_attacks()
        run_agentic_radar()
        run_agentfence()
        run_a2a_scanner()
        aggregate_results()

        print_header("✓ ALL SCANS COMPLETED")
        print("""
Results saved to:
  - reports/agentic_radar/agentic_radar_results.json
  - reports/agentfence/agentfence_results.json
  - reports/a2a_scanner/a2a_scanner_results.json
  - reports/aggregated_results.json (unified results)

Next steps:
  1. Review the aggregated results
  2. Generate HTML dashboard (coming soon)
  3. Analyze vulnerabilities and plan mitigations
""")

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during scan: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
