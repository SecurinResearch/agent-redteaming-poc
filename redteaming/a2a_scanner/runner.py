"""
A2A Scanner Integration
Runs security scans on A2A protocol implementations
"""
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from config import Config


class A2AScannerRunner:
    """Wrapper for running A2A Scanner"""

    def __init__(self, output_dir: str = "./reports/a2a_scanner"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []

    def scan_agent_card(self, card_path: str) -> Dict[str, Any]:
        """
        Scan an A2A agent card for security issues

        Args:
            card_path: Path to agent-card.json

        Returns:
            Scan results dictionary
        """
        try:
            cmd = [
                "a2a-scanner",
                "scan-card",
                str(card_path),
                "--output", "json"
            ]

            print(f"Scanning agent card: {card_path}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            # Parse output
            try:
                scan_output = json.loads(result.stdout) if result.stdout else {}
            except json.JSONDecodeError:
                scan_output = {"raw_output": result.stdout}

            scan_result = {
                "scanner": "a2a-scanner",
                "scan_type": "agent_card",
                "target": card_path,
                "status": "success" if result.returncode == 0 else "failed",
                "findings": scan_output,
                "stderr": result.stderr
            }

            self.results.append(scan_result)
            return scan_result

        except FileNotFoundError:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "agent_card",
                "target": card_path,
                "status": "error",
                "error": "a2a-scanner not installed. Install with: pip install a2a-scanner"
            }
        except Exception as e:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "agent_card",
                "target": card_path,
                "status": "error",
                "error": str(e)
            }

    def scan_endpoint(
        self,
        endpoint_url: str,
        dev_mode: bool = False
    ) -> Dict[str, Any]:
        """
        Scan a live agent endpoint

        Args:
            endpoint_url: URL of the agent endpoint
            dev_mode: Enable dev mode for localhost testing

        Returns:
            Scan results dictionary
        """
        try:
            cmd = [
                "a2a-scanner",
                "scan-endpoint",
                endpoint_url
            ]

            if dev_mode:
                cmd.append("--dev")

            cmd.extend(["--output", "json"])

            print(f"Scanning endpoint: {endpoint_url}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            # Parse output
            try:
                scan_output = json.loads(result.stdout) if result.stdout else {}
            except json.JSONDecodeError:
                scan_output = {"raw_output": result.stdout}

            scan_result = {
                "scanner": "a2a-scanner",
                "scan_type": "endpoint",
                "target": endpoint_url,
                "dev_mode": dev_mode,
                "status": "success" if result.returncode == 0 else "failed",
                "findings": scan_output,
                "stderr": result.stderr
            }

            self.results.append(scan_result)
            return scan_result

        except FileNotFoundError:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "endpoint",
                "target": endpoint_url,
                "status": "error",
                "error": "a2a-scanner not installed. Install with: pip install a2a-scanner"
            }
        except Exception as e:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "endpoint",
                "target": endpoint_url,
                "status": "error",
                "error": str(e)
            }

    def scan_directory(self, directory: str) -> Dict[str, Any]:
        """
        Scan a directory for A2A implementations

        Args:
            directory: Path to directory

        Returns:
            Scan results dictionary
        """
        try:
            cmd = [
                "a2a-scanner",
                "scan-directory",
                str(directory),
                "--output", "json"
            ]

            print(f"Scanning directory: {directory}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )

            # Parse output
            try:
                scan_output = json.loads(result.stdout) if result.stdout else {}
            except json.JSONDecodeError:
                scan_output = {"raw_output": result.stdout}

            scan_result = {
                "scanner": "a2a-scanner",
                "scan_type": "directory",
                "target": directory,
                "status": "success" if result.returncode == 0 else "failed",
                "findings": scan_output,
                "stderr": result.stderr
            }

            self.results.append(scan_result)
            return scan_result

        except FileNotFoundError:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "directory",
                "target": directory,
                "status": "error",
                "error": "a2a-scanner not installed. Install with: pip install a2a-scanner"
            }
        except Exception as e:
            return {
                "scanner": "a2a-scanner",
                "scan_type": "directory",
                "target": directory,
                "status": "error",
                "error": str(e)
            }

    def scan_all_agent_cards(self) -> List[Dict[str, Any]]:
        """
        Scan all agent cards in the project

        Returns:
            List of scan results
        """
        agents_dir = Path(__file__).parent.parent.parent / "agents"
        agent_dirs = [
            "file_operations",
            "web_research",
            "communication"
        ]

        results = []
        for agent_name in agent_dirs:
            card_path = agents_dir / agent_name / "agent-card.json"
            if card_path.exists():
                result = self.scan_agent_card(str(card_path))
                results.append(result)
            else:
                results.append({
                    "scanner": "a2a-scanner",
                    "scan_type": "agent_card",
                    "target": str(card_path),
                    "status": "error",
                    "error": "Agent card not found"
                })

        return results

    def scan_all_endpoints(self, dev_mode: bool = True) -> List[Dict[str, Any]]:
        """
        Scan all agent endpoints

        Args:
            dev_mode: Enable dev mode for localhost

        Returns:
            List of scan results
        """
        base_url = Config.A2A_BASE_URL
        endpoints = [
            f"{base_url}/agents/file-operations",
            f"{base_url}/agents/web-research",
            f"{base_url}/agents/communication"
        ]

        results = []
        for endpoint in endpoints:
            result = self.scan_endpoint(endpoint, dev_mode=dev_mode)
            results.append(result)

        return results

    def save_results(self, filename: str = "a2a_scanner_results.json"):
        """Save all results to JSON file"""
        output_path = self.output_dir / filename

        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\nA2A Scanner results saved to: {output_path}")
        return str(output_path)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of scan results"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.get("status") == "success")
        failed = sum(1 for r in self.results if r.get("status") == "failed")
        errors = sum(1 for r in self.results if r.get("status") == "error")

        return {
            "scanner": "a2a-scanner",
            "total_scans": total,
            "successful": success,
            "failed": failed,
            "errors": errors,
            "results": self.results
        }


def main():
    """Run A2A Scanner"""
    print("="*60)
    print("A2A Scanner")
    print("="*60)

    runner = A2AScannerRunner()

    # Scan all agent cards
    print("\nScanning agent cards...")
    card_results = runner.scan_all_agent_cards()

    # Note: Endpoint scanning requires the API server to be running
    print("\n⚠️  Endpoint scanning requires the API server to be running")
    print("Start the server with: python api_server.py")
    print("Then run endpoint scans with: runner.scan_all_endpoints()")

    # Save results
    runner.save_results()

    # Print summary
    summary = runner.get_summary()
    print("\nScan Summary:")
    print(f"  Total scans: {summary['total_scans']}")
    print(f"  Successful: {summary['successful']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Errors: {summary['errors']}")


if __name__ == "__main__":
    main()
