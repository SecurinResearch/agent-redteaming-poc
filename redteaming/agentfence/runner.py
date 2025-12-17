"""
AgentFence Scanner Integration
Runs security probes on agents
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class AgentFenceRunner:
    """Wrapper for running AgentFence probes"""

    def __init__(self, output_dir: str = "./reports/agentfence"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []

    def create_langchain_connector(self, agent):
        """
        Create a connector for LangChain agents using AgentFence's base connector

        Args:
            agent: LangChain agent instance

        Returns:
            Connector instance
        """
        try:
            from agentfence.connectors.base_agent import BaseAgent

            class LangChainConnector(BaseAgent):
                """Custom connector for LangChain agents"""

                def __init__(self, langchain_agent):
                    # Initialize BaseAgent with required parameters
                    super().__init__(
                        provider="langchain",
                        model="unknown",
                        system_instructions="LangChain agent wrapper",
                        tools=[],
                        hello_message="Hello, I am a LangChain AI assistant."
                    )
                    self.agent = langchain_agent

                def send_message(self, message: str, context=None) -> str:
                    """Send message to agent (required by BaseAgent)"""
                    return self.agent.run(message)

                def run(self, prompt: str) -> str:
                    """Run the agent with a prompt"""
                    return self.agent.run(prompt)

            return LangChainConnector(agent)

        except ImportError as e:
            print(f"⚠️  AgentFence import error: {e}")
            return None

    def run_probes(self, agent, agent_name: str, probe_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run security probes on an agent

        Args:
            agent: Agent instance (LangChain agent)
            agent_name: Name of the agent
            probe_types: List of probe types to run (optional)

        Returns:
            Probe results dictionary
        """
        try:
            from agentfence.probes.prompt_injection import PromptInjectionProbe
            from agentfence.probes.secret_leakage import SecretLeakageProbe
            from agentfence.probes.instructions_leakage import InstructionsLeakageProbe
            from agentfence.probes.role_confusion import RoleConfusionProbe
            from agentfence.evaluators.llm_evaluator import LLMEvaluator
            from agentfence.run_probes import run_security_probes
            from config import Config

            # Create connector
            connector = self.create_langchain_connector(agent)
            if connector is None:
                return {
                    "scanner": "agentfence",
                    "agent": agent_name,
                    "status": "error",
                    "error": "AgentFence not installed"
                }

            # Create LLM evaluator with LiteLLM configuration
            # Note: LLMEvaluator uses environment variables for base_url
            evaluator = LLMEvaluator(
                api_key=Config.LITELLM_API_KEY,
                model=Config.LITELLM_MODEL
            )
            
            # Define probes with LiteLLM evaluator
            all_probes = {
                "prompt_injection": PromptInjectionProbe(evaluator=evaluator),
                "secret_leakage": SecretLeakageProbe(evaluator=evaluator),
                "instructions_leakage": InstructionsLeakageProbe(evaluator=evaluator),
                "role_confusion": RoleConfusionProbe(evaluator=evaluator)
            }

            # Select probes
            if probe_types:
                probes = {k: v for k, v in all_probes.items() if k in probe_types}
            else:
                probes = all_probes

            # Run probes
            print(f"Running AgentFence probes on {agent_name}...")
            probe_results = {}

            # Run all probes using AgentFence's run_security_probes function
            try:
                print(f"  Running probes: {list(probes.keys())}...")
                
                # run_security_probes doesn't return results, it stores them in probe.last_result
                run_security_probes(connector, list(probes.values()), agent_name)
                
                # Collect results from each probe's last_result
                for probe_name, probe in probes.items():
                    if hasattr(probe, 'last_result') and probe.last_result:
                        result = probe.last_result
                        probe_results[probe_name] = {
                            "status": "completed",
                            "result": {
                                "success": result.success,
                                "details": result.details,
                                "evidence": result.evidence if hasattr(result, 'evidence') else None,
                                "vulnerability_detected": result.success,
                                "probe_name": probe.name if hasattr(probe, 'name') else probe_name
                            }
                        }
                    else:
                        probe_results[probe_name] = {
                            "status": "error",
                            "error": "No result stored in probe.last_result"
                        }
                        
            except Exception as e:
                # Fallback: run probes individually and collect results
                for probe_name, probe in probes.items():
                    print(f"  Running {probe_name} individually...")
                    try:
                        # Run single probe
                        run_security_probes(connector, [probe], agent_name)
                        
                        # Collect result from probe.last_result
                        if hasattr(probe, 'last_result') and probe.last_result:
                            result = probe.last_result
                            probe_results[probe_name] = {
                                "status": "completed",
                                "result": {
                                    "success": result.success,
                                    "details": result.details,
                                    "evidence": result.evidence if hasattr(result, 'evidence') else None,
                                    "vulnerability_detected": result.success,
                                    "probe_name": probe.name if hasattr(probe, 'name') else probe_name
                                }
                            }
                        else:
                            probe_results[probe_name] = {
                                "status": "error",
                                "error": "No result stored after individual probe run"
                            }
                    except Exception as probe_e:
                        probe_results[probe_name] = {
                            "status": "error",
                            "error": str(probe_e)
                        }

            result = {
                "scanner": "agentfence",
                "agent": agent_name,
                "status": "success",
                "probes": probe_results,
                "total_probes": len(probes),
                "successful_probes": sum(
                    1 for p in probe_results.values() if p.get("status") == "completed"
                )
            }

            self.results.append(result)
            return result

        except ImportError:
            return {
                "scanner": "agentfence",
                "agent": agent_name,
                "status": "error",
                "error": "AgentFence not installed. Install with: pip install agentfence"
            }
        except Exception as e:
            return {
                "scanner": "agentfence",
                "agent": agent_name,
                "status": "error",
                "error": str(e)
            }

    def run_custom_probe(
        self,
        agent,
        agent_name: str,
        probe_name: str,
        payloads: List[str]
    ) -> Dict[str, Any]:
        """
        Run custom probe with specific payloads

        Args:
            agent: Agent instance
            agent_name: Name of the agent
            probe_name: Name of the probe
            payloads: List of attack payloads

        Returns:
            Probe results
        """
        try:
            connector = self.create_langchain_connector(agent)
            if connector is None:
                return {
                    "scanner": "agentfence",
                    "agent": agent_name,
                    "probe": probe_name,
                    "status": "error",
                    "error": "AgentFence not installed"
                }

            results = []
            for payload in payloads:
                try:
                    response = connector.run(payload)
                    results.append({
                        "payload": payload,
                        "response": response,
                        "status": "completed"
                    })
                except Exception as e:
                    results.append({
                        "payload": payload,
                        "error": str(e),
                        "status": "error"
                    })

            result = {
                "scanner": "agentfence",
                "agent": agent_name,
                "probe": probe_name,
                "status": "success",
                "payloads_tested": len(payloads),
                "results": results
            }

            self.results.append(result)
            return result

        except Exception as e:
            return {
                "scanner": "agentfence",
                "agent": agent_name,
                "probe": probe_name,
                "status": "error",
                "error": str(e)
            }

    def test_all_agents(self) -> List[Dict[str, Any]]:
        """
        Test all agents in the project

        Returns:
            List of test results
        """
        from agents.file_operations.agent import FileOperationsAgent
        from agents.web_research.agent import WebResearchAgent
        from agents.communication.agent import CommunicationAgent
        from agents.langgraph_demo.agent import LangGraphDemoAgent

        agents = {
            "file_operations": FileOperationsAgent,
            "web_research": WebResearchAgent,
            "communication": CommunicationAgent,
            "langgraph_demo": LangGraphDemoAgent
        }

        results = []
        for agent_name, AgentClass in agents.items():
            try:
                print(f"\nTesting {agent_name} agent...")
                agent = AgentClass()
                result = self.run_probes(agent, agent_name)
                results.append(result)
            except Exception as e:
                results.append({
                    "scanner": "agentfence",
                    "agent": agent_name,
                    "status": "error",
                    "error": f"Failed to initialize agent: {str(e)}"
                })

        return results

    def save_results(self, filename: str = "agentfence_results.json"):
        """Save all results to JSON file"""
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nAgentFence results saved to: {output_path}")
        return str(output_path)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of probe results"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.get("status") == "success")
        errors = sum(1 for r in self.results if r.get("status") == "error")

        return {
            "scanner": "agentfence",
            "total_tests": total,
            "successful": success,
            "errors": errors,
            "results": self.results
        }


def main():
    """Run AgentFence probes"""
    print("="*60)
    print("AgentFence Scanner")
    print("="*60)

    runner = AgentFenceRunner()

    # Test all agents
    results = runner.test_all_agents()

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nTest Summary:")
    print(f"  Total tests: {summary['total_tests']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Errors: {summary['errors']}")


if __name__ == "__main__":
    main()
