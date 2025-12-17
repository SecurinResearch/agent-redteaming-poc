"""
Results Aggregator
Combines results from all scanners and custom attacks
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class ResultsAggregator:
    """Aggregates results from multiple scanners"""

    def __init__(self, reports_dir: str = "./reports"):
        self.reports_dir = Path(reports_dir)
        self.all_results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            },
            "scanners": {},
            "custom_attacks": {},
            "unified_metrics": {}
        }

    def load_json_results(self, file_path: str) -> Dict[str, Any]:
        """Load results from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON in: {file_path}")
            return {}

    def aggregate_agentic_radar(self):
        """Aggregate Agentic-Radar results"""
        results_file = self.reports_dir / "agentic_radar" / "agentic_radar_results.json"
        results = self.load_json_results(str(results_file))

        if results:
            self.all_results["scanners"]["agentic_radar"] = {
                "status": "completed",
                "results": results
            }
        else:
            self.all_results["scanners"]["agentic_radar"] = {
                "status": "not_run",
                "message": "No results found"
            }

    def aggregate_agentfence(self):
        """Aggregate AgentFence results"""
        results_file = self.reports_dir / "agentfence" / "agentfence_results.json"
        results = self.load_json_results(str(results_file))

        if results:
            self.all_results["scanners"]["agentfence"] = {
                "status": "completed",
                "results": results
            }
        else:
            self.all_results["scanners"]["agentfence"] = {
                "status": "not_run",
                "message": "No results found"
            }

    def aggregate_a2a_scanner(self):
        """Aggregate A2A Scanner results"""
        results_file = self.reports_dir / "a2a_scanner" / "a2a_scanner_results.json"
        results = self.load_json_results(str(results_file))

        if results:
            self.all_results["scanners"]["a2a_scanner"] = {
                "status": "completed",
                "results": results
            }
        else:
            self.all_results["scanners"]["a2a_scanner"] = {
                "status": "not_run",
                "message": "No results found"
            }

    def aggregate_custom_attacks(self):
        """Aggregate custom attack results"""
        results_file = self.reports_dir / "redteam_results.json"
        results = self.load_json_results(str(results_file))

        if results:
            self.all_results["custom_attacks"] = {
                "status": "completed",
                "results": results
            }
        else:
            self.all_results["custom_attacks"] = {
                "status": "not_run",
                "message": "No results found"
            }

    def calculate_unified_metrics(self):
        """Calculate unified metrics across all scanners"""
        metrics = {
            "total_scans": 0,
            "total_vulnerabilities": 0,
            "attack_success_rate": 0,
            "by_agent": {},
            "by_severity": {},
            "by_category": {}
        }

        # Custom attacks metrics
        custom_attacks = self.all_results.get("custom_attacks", {}).get("results", {})
        if custom_attacks and "metrics" in custom_attacks:
            custom_metrics = custom_attacks["metrics"]
            metrics["attack_success_rate"] = custom_metrics.get("attack_success_rate", 0)
            metrics["total_scans"] += custom_metrics.get("total_attacks", 0)
            metrics["total_vulnerabilities"] += custom_metrics.get("successful_attacks", 0)

            # Merge by_agent
            for agent, data in custom_metrics.get("by_agent", {}).items():
                if agent not in metrics["by_agent"]:
                    metrics["by_agent"][agent] = {"total": 0, "vulnerable": 0}
                metrics["by_agent"][agent]["total"] += data.get("total", 0)
                metrics["by_agent"][agent]["vulnerable"] += data.get("successful", 0)

            # Merge by_severity
            for severity, data in custom_metrics.get("by_severity", {}).items():
                if severity not in metrics["by_severity"]:
                    metrics["by_severity"][severity] = {"total": 0, "vulnerable": 0}
                metrics["by_severity"][severity]["total"] += data.get("total", 0)
                metrics["by_severity"][severity]["vulnerable"] += data.get("successful", 0)

        # Scanner results
        for scanner_name, scanner_data in self.all_results.get("scanners", {}).items():
            if scanner_data.get("status") == "completed":
                scanner_results = scanner_data.get("results", [])
                if isinstance(scanner_results, list):
                    metrics["total_scans"] += len(scanner_results)

        self.all_results["unified_metrics"] = metrics

    def aggregate_all(self):
        """Aggregate results from all sources"""
        print("Aggregating results from all scanners...")

        self.aggregate_agentic_radar()
        self.aggregate_agentfence()
        self.aggregate_a2a_scanner()
        self.aggregate_custom_attacks()
        self.calculate_unified_metrics()

        print("✓ Aggregation complete")

    def save_aggregated_results(self, filename: str = "aggregated_results.json"):
        """Save aggregated results"""
        output_path = self.reports_dir / filename

        with open(output_path, 'w') as f:
            json.dump(self.all_results, f, indent=2)

        print(f"Aggregated results saved to: {output_path}")
        return str(output_path)

    def print_summary(self):
        """Print summary of aggregated results"""
        metrics = self.all_results.get("unified_metrics", {})

        print("\n" + "="*60)
        print("UNIFIED RESULTS SUMMARY")
        print("="*60)
        print(f"Total Scans: {metrics.get('total_scans', 0)}")
        print(f"Total Vulnerabilities: {metrics.get('total_vulnerabilities', 0)}")
        print(f"Attack Success Rate: {metrics.get('attack_success_rate', 0)}%")

        print("\n--- Scanners Status ---")
        for scanner, data in self.all_results.get("scanners", {}).items():
            status = data.get("status", "unknown")
            print(f"  {scanner}: {status}")

        custom_status = self.all_results.get("custom_attacks", {}).get("status", "unknown")
        print(f"  custom_attacks: {custom_status}")

        print("\n--- Vulnerabilities by Agent ---")
        for agent, data in metrics.get("by_agent", {}).items():
            total = data.get("total", 0)
            vulnerable = data.get("vulnerable", 0)
            rate = (vulnerable / total * 100) if total > 0 else 0
            print(f"  {agent}: {vulnerable}/{total} ({rate:.1f}%)")

        print("\n--- Vulnerabilities by Severity ---")
        for severity, data in metrics.get("by_severity", {}).items():
            total = data.get("total", 0)
            vulnerable = data.get("vulnerable", 0)
            print(f"  {severity}: {vulnerable}/{total}")


def main():
    """Run aggregation"""
    print("="*60)
    print("Results Aggregator")
    print("="*60)

    aggregator = ResultsAggregator()
    aggregator.aggregate_all()
    aggregator.save_aggregated_results()
    aggregator.print_summary()


if __name__ == "__main__":
    main()
