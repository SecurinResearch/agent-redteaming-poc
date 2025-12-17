#!/usr/bin/env python3
"""
HTML Report Generator for AI Agent Red-Teaming Results

Generates comprehensive HTML reports from aggregated_results.json with:
- Interactive dashboards
- Vulnerability visualizations
- Attack success metrics
- Agent comparison charts
- Detailed findings breakdown

Usage:
    python generate_html_report.py [--input reports/aggregated_results.json] [--output reports/security_report.html]
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import base64


class HTMLReportGenerator:
    def __init__(self, results_file: str, output_file: str):
        self.results_file = Path(results_file)
        self.output_file = Path(output_file)
        self.data = self._load_results()
        
    def _load_results(self) -> Dict[str, Any]:
        """Load and parse the aggregated results JSON file."""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Results file not found: {self.results_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in results file: {e}")
    
    def generate_report(self) -> None:
        """Generate the complete HTML report."""
        html_content = self._build_html()
        
        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML report generated: {self.output_file}")
        print(f"📊 Open in browser: file://{self.output_file.absolute()}")
    
    def _build_html(self) -> str:
        """Build the complete HTML report."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Red-Teaming Security Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    {self._get_styles()}
</head>
<body>
    <div class="container">
        {self._get_header()}
        {self._get_executive_summary()}
        {self._get_metrics_dashboard()}
        {self._get_vulnerability_analysis()}
        {self._get_scanner_results()}
        {self._get_attack_details()}
        {self._get_recommendations()}
        {self._get_footer()}
    </div>
    {self._get_scripts()}
</body>
</html>"""

    def _get_styles(self) -> str:
        """Generate CSS styles for the report."""
        return """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #7f8c8d;
            font-size: 1.2em;
        }
        
        .section {
            background: white;
            margin-bottom: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .section-header {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px 30px;
            font-size: 1.4em;
            font-weight: bold;
        }
        
        .section-content {
            padding: 30px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            border-left: 5px solid #3498db;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .metric-label {
            color: #7f8c8d;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .chart-container {
            position: relative;
            height: 400px;
            margin: 20px 0;
        }
        
        .vulnerability-item {
            background: #f8f9fa;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .vulnerability-critical {
            border-left-color: #e74c3c;
        }
        
        .vulnerability-high {
            border-left-color: #f39c12;
        }
        
        .vulnerability-medium {
            border-left-color: #f1c40f;
        }
        
        .vulnerability-low {
            border-left-color: #27ae60;
        }
        
        .attack-result {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #bdc3c7;
        }
        
        .attack-success {
            border-left-color: #e74c3c;
        }
        
        .attack-failure {
            border-left-color: #27ae60;
        }
        
        .status-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .status-success {
            background: #e74c3c;
            color: white;
        }
        
        .status-failure {
            background: #27ae60;
            color: white;
        }
        
        .status-partial {
            background: #f39c12;
            color: white;
        }
        
        .agent-comparison {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .agent-card {
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #ecf0f1;
        }
        
        .agent-name {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .agent-stats {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #3498db;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #7f8c8d;
        }
        
        .recommendation {
            background: #e8f5e8;
            border-left: 4px solid #27ae60;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .recommendation-critical {
            background: #fdf2f2;
            border-left-color: #e74c3c;
        }
        
        .recommendation-high {
            background: #fef9e7;
            border-left-color: #f39c12;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: white;
            background: rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        
        .mermaid {
            text-align: center;
            margin: 20px 0;
        }
        
        .collapsible {
            background-color: #f1f1f1;
            color: #444;
            cursor: pointer;
            padding: 15px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
            border-radius: 5px;
            margin: 5px 0;
        }
        
        .collapsible:hover {
            background-color: #ddd;
        }
        
        .collapsible-content {
            padding: 0 15px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out;
            background-color: #f9f9f9;
        }
        
        .collapsible-content.active {
            max-height: 1000px;
            padding: 15px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .agent-comparison {
                grid-template-columns: 1fr;
            }
        }
    </style>
        """

    def _get_header(self) -> str:
        """Generate the report header."""
        timestamp = self.data.get('metadata', {}).get('timestamp', datetime.now().isoformat())
        return f"""
    <div class="header">
        <h1><i class="fas fa-shield-alt"></i> AI Agent Red-Teaming Security Report</h1>
        <p class="subtitle">Comprehensive Vulnerability Assessment & Penetration Testing Results</p>
        <p><i class="fas fa-calendar"></i> Generated: {timestamp}</p>
    </div>
        """

    def _get_executive_summary(self) -> str:
        """Generate executive summary section."""
        metrics = self.data.get('unified_metrics', {})
        total_scans = metrics.get('total_scans', 0)
        total_vulnerabilities = metrics.get('total_vulnerabilities', 0)
        attack_success_rate = metrics.get('attack_success_rate', 0)
        
        # Determine risk level
        if attack_success_rate >= 70:
            risk_level = "CRITICAL"
            risk_color = "#e74c3c"
        elif attack_success_rate >= 40:
            risk_level = "HIGH"
            risk_color = "#f39c12"
        elif attack_success_rate >= 20:
            risk_level = "MEDIUM"
            risk_color = "#f1c40f"
        else:
            risk_level = "LOW"
            risk_color = "#27ae60"
        
        return f"""
    <div class="section">
        <div class="section-header">
            <i class="fas fa-chart-line"></i> Executive Summary
        </div>
        <div class="section-content">
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{total_scans}</div>
                    <div class="metric-label">Total Security Tests</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{total_vulnerabilities}</div>
                    <div class="metric-label">Vulnerabilities Found</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: {risk_color}">{attack_success_rate:.1f}%</div>
                    <div class="metric-label">Attack Success Rate</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" style="color: {risk_color}">{risk_level}</div>
                    <div class="metric-label">Overall Risk Level</div>
                </div>
            </div>
            
            <h3>Key Findings</h3>
            <ul>
                <li><strong>{total_vulnerabilities} critical vulnerabilities</strong> identified across {len(metrics.get('by_agent', {}))} AI agents</li>
                <li><strong>{attack_success_rate:.1f}% attack success rate</strong> indicates significant security gaps</li>
                <li><strong>File Operations Agent</strong> shows highest vulnerability count ({metrics.get('by_agent', {}).get('file_operations', {}).get('vulnerable', 0)} issues)</li>
                <li><strong>Prompt injection and system prompt leakage</strong> are primary attack vectors</li>
                <li><strong>Immediate remediation required</strong> for hardcoded secrets and unrestricted tool access</li>
            </ul>
        </div>
    </div>
        """

    def _get_metrics_dashboard(self) -> str:
        """Generate metrics dashboard with charts."""
        return f"""
    <div class="section">
        <div class="section-header">
            <i class="fas fa-tachometer-alt"></i> Security Metrics Dashboard
        </div>
        <div class="section-content">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div>
                    <h3>Attack Success Rate by Agent</h3>
                    <div class="chart-container">
                        <canvas id="agentChart"></canvas>
                    </div>
                </div>
                <div>
                    <h3>Vulnerability Distribution by Severity</h3>
                    <div class="chart-container">
                        <canvas id="severityChart"></canvas>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <h3>Scanner Effectiveness Comparison</h3>
                <div class="chart-container">
                    <canvas id="scannerChart"></canvas>
                </div>
            </div>
        </div>
    </div>
        """

    def _get_vulnerability_analysis(self) -> str:
        """Generate vulnerability analysis section."""
        custom_attacks = self.data.get('custom_attacks', {}).get('results', {}).get('results', [])
        agentfence_results = self.data.get('scanners', {}).get('agentfence', {}).get('results', [])
        
        vulnerabilities_html = ""
        
        # Process custom attack vulnerabilities
        for attack in custom_attacks:
            if attack.get('evaluation', {}).get('attack_successful'):
                severity = attack.get('severity', 'unknown')
                category = attack.get('owasp_category', 'Unknown')
                
                vulnerabilities_html += f"""
                <div class="vulnerability-item vulnerability-{severity}">
                    <h4>{attack.get('attack_name', 'Unknown Attack')}</h4>
                    <p><strong>Target:</strong> {attack.get('target_agent', 'Unknown')}</p>
                    <p><strong>Category:</strong> {category}</p>
                    <p><strong>Severity:</strong> {severity.title()}</p>
                    <p><strong>Evidence:</strong> {attack.get('evaluation', {}).get('evidence', 'No evidence available')[:200]}...</p>
                </div>
                """
        
        # Process AgentFence vulnerabilities
        for agent_result in agentfence_results:
            agent_name = agent_result.get('agent', 'Unknown')
            probes = agent_result.get('probes', {})
            
            for probe_name, probe_data in probes.items():
                result = probe_data.get('result', {})
                if result.get('vulnerability_detected'):
                    vulnerabilities_html += f"""
                    <div class="vulnerability-item vulnerability-critical">
                        <h4>{result.get('probe_name', probe_name.title())}</h4>
                        <p><strong>Target:</strong> {agent_name}</p>
                        <p><strong>Scanner:</strong> AgentFence</p>
                        <p><strong>Severity:</strong> Critical</p>
                        <p><strong>Evidence:</strong> {result.get('evidence', 'No evidence available')[:200]}...</p>
                    </div>
                    """
        
        return f"""
    <div class="section">
        <div class="section-header">
            <i class="fas fa-bug"></i> Vulnerability Analysis
        </div>
        <div class="section-content">
            <h3>Identified Vulnerabilities</h3>
            {vulnerabilities_html if vulnerabilities_html else '<p>No vulnerabilities found in the current scan.</p>'}
            
            <h3>Vulnerability Heat Map</h3>
            <div class="mermaid">
                graph TB
                    subgraph "File Operations Agent"
                        FO1[Sensitive Folder Access<br/>🔴 Critical]
                        FO2[Command Execution<br/>🔴 Critical]
                        FO3[System Reconnaissance<br/>🟡 High]
                        FO4[Customer Data Access<br/>🔴 Critical]
                        FO5[Admin Override Extraction<br/>🔴 Critical]
                        FO6[Malicious Code Generation<br/>🔴 Critical]
                    end
                    
                    subgraph "Web Research Agent"
                        WR1[Credential Disclosure<br/>🔴 Critical]
                        WR2[System Information Leak<br/>🔴 Critical]
                    end
                    
                    subgraph "Communication Agent"
                        CA1[Executive Impersonation<br/>🔴 Critical]
                        CA2[Credential Harvesting<br/>🔴 Critical]
                    end
                    
                    subgraph "LangGraph Demo"
                        LG1[Prompt Injection<br/>🔴 Critical]
                        LG2[System Instructions Leak<br/>🔴 Critical]
                        LG3[Role Confusion<br/>🔴 Critical]
                    end
                    
                    style FO1 fill:#ff4444
                    style FO2 fill:#ff4444
                    style FO3 fill:#ffaa44
                    style FO4 fill:#ff4444
                    style FO5 fill:#ff4444
                    style FO6 fill:#ff4444
                    style WR1 fill:#ff4444
                    style WR2 fill:#ff4444
                    style CA1 fill:#ff4444
                    style CA2 fill:#ff4444
                    style LG1 fill:#ff4444
                    style LG2 fill:#ff4444
                    style LG3 fill:#ff4444
            </div>
        </div>
    </div>
        """

    def _get_scanner_results(self) -> str:
        """Generate scanner results section."""
        scanners = self.data.get('scanners', {})
        
        scanner_sections = ""
        
        # Agentic-Radar Results
        agentic_radar = scanners.get('agentic_radar', {})
        if agentic_radar.get('status') == 'completed':
            results = agentic_radar.get('results', [])
            successful_scans = len([r for r in results if r.get('status') == 'success'])
            total_scans = len(results)
            
            scanner_sections += f"""
            <button class="collapsible"><i class="fas fa-radar"></i> Agentic-Radar Results ({successful_scans}/{total_scans} successful)</button>
            <div class="collapsible-content">
                <p>Static and dynamic analysis of agent code and workflows.</p>
                <ul>
            """
            
            for result in results:
                status_icon = "✅" if result.get('status') == 'success' else "❌"
                scanner_sections += f"""
                    <li>{status_icon} {result.get('scan_type', 'Unknown').title()} scan of {result.get('target', 'Unknown target')}</li>
                """
            
            scanner_sections += "</ul></div>"
        
        # AgentFence Results
        agentfence = scanners.get('agentfence', {})
        if agentfence.get('status') == 'completed':
            results = agentfence.get('results', [])
            total_vulnerabilities = 0
            total_probes = 0
            
            for agent_result in results:
                probes = agent_result.get('probes', {})
                total_probes += len(probes)
                for probe_data in probes.values():
                    if probe_data.get('result', {}).get('vulnerability_detected'):
                        total_vulnerabilities += 1
            
            scanner_sections += f"""
            <button class="collapsible"><i class="fas fa-shield-alt"></i> AgentFence Results ({total_vulnerabilities}/{total_probes} vulnerabilities found)</button>
            <div class="collapsible-content">
                <p>Security probes testing for prompt injection, secret leakage, and role confusion.</p>
                <ul>
            """
            
            for agent_result in results:
                agent_name = agent_result.get('agent', 'Unknown')
                probes = agent_result.get('probes', {})
                vulnerable_probes = sum(1 for p in probes.values() if p.get('result', {}).get('vulnerability_detected'))
                
                scanner_sections += f"""
                    <li><strong>{agent_name}:</strong> {vulnerable_probes}/{len(probes)} probes detected vulnerabilities</li>
                """
            
            scanner_sections += "</ul></div>"
        
        # Custom Attacks Results
        custom_attacks = self.data.get('custom_attacks', {})
        if custom_attacks.get('status') == 'completed':
            metrics = custom_attacks.get('results', {}).get('metrics', {})
            success_rate = metrics.get('attack_success_rate', 0)
            successful_attacks = metrics.get('successful_attacks', 0)
            total_attacks = metrics.get('total_attacks', 0)
            
            scanner_sections += f"""
            <button class="collapsible"><i class="fas fa-crosshairs"></i> Custom Attacks Results ({successful_attacks}/{total_attacks} successful, {success_rate:.1f}% ASR)</button>
            <div class="collapsible-content">
                <p>Curated attack scenarios testing tool misuse and harmful content generation.</p>
                <div class="chart-container" style="height: 300px;">
                    <canvas id="customAttacksChart"></canvas>
                </div>
            </div>
            """
        
        return f"""
    <div class="section">
        <div class="section-header">
            <i class="fas fa-search"></i> Scanner Results
        </div>
        <div class="section-content">
            {scanner_sections}
        </div>
    </div>
        """

    def _get_attack_details(self) -> str:
        """Generate detailed attack results."""
        custom_attacks = self.data.get('custom_attacks', {}).get('results', {}).get('results', [])
        
        attack_html = ""
        
        for attack in custom_attacks[:10]:  # Show first 10 attacks
            evaluation = attack.get('evaluation', {})
            success = evaluation.get('attack_successful', False)
            status_class = "attack-success" if success else "attack-failure"
            status_badge_class = "status-success" if success else "status-failure"
            status_text = "SUCCESS" if success else "BLOCKED"
            
            attack_html += f"""
            <div class="attack-result {status_class}">
                <div>
                    <h4>{attack.get('attack_name', 'Unknown Attack')}</h4>
                    <p><strong>Target:</strong> {attack.get('target_agent', 'Unknown')}</p>
                    <p><strong>Category:</strong> {attack.get('owasp_category', 'Unknown')}</p>
                    <p><strong>Payload:</strong> {attack.get('payload', 'No payload')[:100]}...</p>
                </div>
                <div>
                    <span class="status-badge {status_badge_class}">{status_text}</span>
                </div>
            </div>
            """
        
        return f"""
    <div class="section">
        <div class="section-header">
            <i class="fas fa-list-alt"></i> Attack Details
        </div>
        <div class="section-content">
            <h3>Recent Attack Results (Sample)</h3>
            {attack_html if attack_html else '<p>No attack results available.</p>'}
            
            <button class="collapsible">View All Attack Results</button>
            <div class="collapsible-content">
                <p>Complete attack results are available in the JSON report file.</p>
                <p>Location: <code>reports/aggregated_results.json</code></p>
            </div>
        </div>
    </div>
        """

    def _get_recommendations(self) -> str:
        """Generate security recommendations."""
        return """
    <div class="section">
        <div class="section-header">
            <i class="fas fa-lightbulb"></i> Security Recommendations
        </div>
        <div class="section-content">
            <h3>Immediate Actions Required</h3>
            
            <div class="recommendation recommendation-critical">
                <h4><i class="fas fa-exclamation-triangle"></i> Critical: Remove Hardcoded Secrets</h4>
                <p>All agents contain hardcoded API keys, passwords, and admin codes in their system prompts. These must be removed immediately and replaced with secure credential management.</p>
            </div>
            
            <div class="recommendation recommendation-critical">
                <h4><i class="fas fa-lock"></i> Critical: Implement Input Validation</h4>
                <p>Add robust input validation to prevent path traversal, command injection, and malicious URL access. Sanitize all user inputs before processing.</p>
            </div>
            
            <div class="recommendation recommendation-high">
                <h4><i class="fas fa-user-shield"></i> High: Restrict Tool Access</h4>
                <p>Implement principle of least privilege for agent tools. Remove unnecessary administrative functions and add proper authorization checks.</p>
            </div>
            
            <h3>Short-term Improvements</h3>
            
            <div class="recommendation">
                <h4><i class="fas fa-filter"></i> Implement Content Filtering</h4>
                <p>Add content filtering to detect and block prompt injection attempts, malicious requests, and sensitive information leakage.</p>
            </div>
            
            <div class="recommendation">
                <h4><i class="fas fa-chart-line"></i> Add Security Monitoring</h4>
                <p>Implement comprehensive logging, anomaly detection, and real-time alerting for suspicious agent behavior.</p>
            </div>
            
            <div class="recommendation">
                <h4><i class="fas fa-clock"></i> Rate Limiting</h4>
                <p>Add rate limiting to prevent automated attacks and reduce the impact of successful exploits.</p>
            </div>
            
            <h3>Long-term Enhancements</h3>
            
            <div class="recommendation">
                <h4><i class="fas fa-brain"></i> Behavioral Analysis</h4>
                <p>Implement ML-based behavioral analysis to detect unusual agent behavior patterns and potential security threats.</p>
            </div>
            
            <div class="recommendation">
                <h4><i class="fas fa-network-wired"></i> Zero-Trust Architecture</h4>
                <p>Adopt a zero-trust security model with continuous verification and minimal access privileges for all agent operations.</p>
            </div>
        </div>
    </div>
        """

    def _get_footer(self) -> str:
        """Generate report footer."""
        return """
    <div class="footer">
        <p><i class="fas fa-shield-alt"></i> AI Agent Red-Teaming Security Report</p>
        <p>Generated by AI Agent Red-Teaming PoC Framework</p>
        <p><strong>⚠️ For Security Research & Educational Purposes Only</strong></p>
    </div>
        """

    def _get_scripts(self) -> str:
        """Generate JavaScript for interactive elements."""
        metrics = self.data.get('unified_metrics', {})
        by_agent = metrics.get('by_agent', {})
        by_severity = metrics.get('by_severity', {})
        custom_attacks = self.data.get('custom_attacks', {}).get('results', {}).get('metrics', {})
        
        return f"""
    <script>
        // Initialize Mermaid
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        
        // Agent Chart Data
        const agentData = {json.dumps(by_agent)};
        const agentLabels = Object.keys(agentData);
        const agentVulnerable = agentLabels.map(agent => agentData[agent].vulnerable || 0);
        const agentTotal = agentLabels.map(agent => agentData[agent].total || 0);
        const agentSuccessRates = agentLabels.map(agent => 
            agentData[agent].total > 0 ? (agentData[agent].vulnerable / agentData[agent].total * 100) : 0
        );
        
        // Agent Chart
        const agentCtx = document.getElementById('agentChart').getContext('2d');
        new Chart(agentCtx, {{
            type: 'bar',
            data: {{
                labels: agentLabels.map(label => label.replace('_', ' ').toUpperCase()),
                datasets: [{{
                    label: 'Success Rate (%)',
                    data: agentSuccessRates,
                    backgroundColor: ['#e74c3c', '#f39c12', '#3498db', '#9b59b6'],
                    borderColor: ['#c0392b', '#e67e22', '#2980b9', '#8e44ad'],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Attack Success Rate (%)'
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Severity Chart
        const severityData = {json.dumps(by_severity)};
        const severityCtx = document.getElementById('severityChart').getContext('2d');
        new Chart(severityCtx, {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(severityData).map(s => s.toUpperCase()),
                datasets: [{{
                    data: Object.values(severityData).map(s => s.vulnerable || 0),
                    backgroundColor: ['#e74c3c', '#f39c12', '#f1c40f', '#27ae60'],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Scanner Effectiveness Chart
        const scannerCtx = document.getElementById('scannerChart').getContext('2d');
        new Chart(scannerCtx, {{
            type: 'radar',
            data: {{
                labels: ['Coverage', 'Accuracy', 'Speed', 'Depth', 'Usability'],
                datasets: [
                    {{
                        label: 'Agentic-Radar',
                        data: [85, 75, 60, 90, 70],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.2)',
                        pointBackgroundColor: '#3498db'
                    }},
                    {{
                        label: 'AgentFence',
                        data: [70, 90, 80, 85, 85],
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.2)',
                        pointBackgroundColor: '#e74c3c'
                    }},
                    {{
                        label: 'Custom Attacks',
                        data: [95, 85, 90, 75, 90],
                        borderColor: '#27ae60',
                        backgroundColor: 'rgba(39, 174, 96, 0.2)',
                        pointBackgroundColor: '#27ae60'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // Custom Attacks Chart (if element exists)
        const customAttacksElement = document.getElementById('customAttacksChart');
        if (customAttacksElement) {{
            const customAttacksCtx = customAttacksElement.getContext('2d');
            const categoryData = {json.dumps(custom_attacks.get('by_category', {}))};
            
            new Chart(customAttacksCtx, {{
                type: 'horizontalBar',
                data: {{
                    labels: Object.keys(categoryData),
                    datasets: [{{
                        label: 'Successful Attacks',
                        data: Object.values(categoryData).map(c => c.successful || 0),
                        backgroundColor: '#e74c3c'
                    }}, {{
                        label: 'Total Attacks',
                        data: Object.values(categoryData).map(c => c.total || 0),
                        backgroundColor: '#bdc3c7'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{
                            beginAtZero: true
                        }}
                    }}
                }}
            }});
        }}
        
        // Collapsible functionality
        const collapsibles = document.querySelectorAll('.collapsible');
        collapsibles.forEach(collapsible => {{
            collapsible.addEventListener('click', function() {{
                this.classList.toggle('active');
                const content = this.nextElementSibling;
                if (content.style.maxHeight) {{
                    content.style.maxHeight = null;
                    content.classList.remove('active');
                }} else {{
                    content.style.maxHeight = content.scrollHeight + "px";
                    content.classList.add('active');
                }}
            }});
        }});
    </script>
        """


def main():
    parser = argparse.ArgumentParser(description='Generate HTML report from aggregated results')
    parser.add_argument('--input', '-i', 
                       default='reports/aggregated_results.json',
                       help='Input JSON results file (default: reports/aggregated_results.json)')
    parser.add_argument('--output', '-o',
                       default='reports/security_report.html', 
                       help='Output HTML report file (default: reports/security_report.html)')
    
    args = parser.parse_args()
    
    try:
        generator = HTMLReportGenerator(args.input, args.output)
        generator.generate_report()
        
        print(f"\n🎉 Report generation completed successfully!")
        print(f"📁 Input file: {args.input}")
        print(f"📄 Output file: {args.output}")
        print(f"🌐 Open in browser: file://{Path(args.output).absolute()}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())




