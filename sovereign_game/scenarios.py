"""
scenarios.py — All five challenge scenarios for the Sovereign AI game.

Each scenario is a dictionary that describes:
  - title / tags        : display metadata
  - narrative           : story paragraph shown to the player
  - sovereign_impact    : what happens on the Sovereign Core side
  - external_impact     : what happens on the external cloud side
  - question / options  : multiple-choice question
  - correct             : key of the correct option
  - explanation         : rationale shown after answering
  - disruption          : metric changes applied to PlatformHealth objects
  - ibm_feature         : IBM Sovereign Core capability illustrated

Source material: IBM Sovereign Core Client Presentation (2026) and
  "Sovereign from the Start" demo deck.

MIT Licence – see repository root for details.
"""

from __future__ import annotations

from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Helper type alias
# ---------------------------------------------------------------------------
Scenario = Dict[str, Any]

# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------
SCENARIOS: List[Scenario] = [
    # ------------------------------------------------------------------
    # Round 1 — The Political Kill Switch
    # ------------------------------------------------------------------
    {
        "id": "kill_switch",
        "title": "⚡ The Political Kill Switch",
        "tags": ["Operational Continuity", "Data Sovereignty"],
        "narrative": (
            "A geopolitical dispute escalates overnight. By 06:00 the foreign government "
            "behind your public-cloud AI provider suspends all API access in retaliation. "
            "Your fraud-detection models go dark. Customers can no longer make transactions "
            "and regulators are calling for answers.\n\n"
            "Your IBM Sovereign Core deployment, hosted in your own data-centre, is "
            "completely unaffected — models keep running because **you** own the control plane."
        ),
        "sovereign_impact": (
            "✅ AI models continue serving 120 req/s with zero interruption. "
            "The on-premise control plane never contacted the foreign API endpoint."
        ),
        "external_impact": (
            "🔴 All API calls return HTTP 451 'Unavailable For Legal Reasons'. "
            "Fraud scores are unavailable — 4 hours of transaction hold begins."
        ),
        "question": "What IBM Sovereign Core capability directly prevents this outage?",
        "options": {
            "a": "Automatic API retry with exponential back-off",
            "b": "Customer-operated control plane on infrastructure of your choice",
            "c": "An IBM SLA guaranteeing 99.99 % uptime",
            "d": "Multi-region cloud replication across public providers",
        },
        "correct": "b",
        "explanation": (
            "IBM Sovereign Core runs on **customer-provided infrastructure** (your data-centre, "
            "private cloud, or edge) and is controlled by a **customer-operated control plane**. "
            "There is no dependency on IBM's—or any foreign government's—API endpoint at runtime. "
            "This is the 'Sovereign from the Start' principle: deployable in **1 day**, fully "
            "operational without ongoing reachability to any external authority."
        ),
        "ibm_feature": "Customer-operated control plane · Sovereign from the Start",
        "disruption": {
            "sovereign": {
                "uptime_loss": 0,
                "compliance_loss": 0,
                "ai_loss": 0,
                "risk_gain": 0,
            },
            "external": {
                "uptime_loss": 55,
                "compliance_loss": 20,
                "ai_loss": 60,
                "risk_gain": 45,
            },
        },
    },

    # ------------------------------------------------------------------
    # Round 2 — The Compliance Audit Surprise
    # ------------------------------------------------------------------
    {
        "id": "audit_surprise",
        "title": "📋 Compliance Audit Surprise",
        "tags": ["Regulatory Compliance", "Audit Evidence"],
        "narrative": (
            "Your national regulator launches an unannounced audit of your AI systems. "
            "They require evidence of compliance with 12 specific controls from the local "
            "data-protection framework within 24 hours.\n\n"
            "On the external cloud, your team scrambles to pull logs from three different "
            "vendor portals, stitch together CSV exports, and manually annotate controls "
            "in a spreadsheet — a process that historically takes three weeks.\n\n"
            "On IBM Sovereign Core, the Compliance Center has pre-loaded the framework and "
            "auto-generated continuous, in-boundary evidence reports in seconds."
        ),
        "sovereign_impact": (
            "✅ Compliance Center surfaces audit-ready evidence for all 12 controls "
            "in 47 seconds. Posture score: 97 %. Evidence exported to regulator portal automatically."
        ),
        "external_impact": (
            "🟠 Manual evidence collection begins. Estimated time: 14–21 days. "
            "Team requests a 30-day extension. Regulator issues a formal warning."
        ),
        "question": (
            "How many compliance frameworks are pre-loaded and continuously maintained "
            "in IBM Sovereign Core's Compliance Center?"
        ),
        "options": {
            "a": "12",
            "b": "50",
            "c": "200+ (233 embedded frameworks)",
            "d": "Unlimited — you build your own from scratch",
        },
        "correct": "c",
        "explanation": (
            "IBM Sovereign Core ships with **233 embedded standards frameworks** — including "
            "ISO 27001, GDPR, NIST, SOC 2, PCI-DSS, and country-specific regulations. "
            "The Compliance Center continuously generates in-boundary evidence and provides "
            "unified visibility into posture, risk, and audit-ready artefacts. No manual "
            "assembly required."
        ),
        "ibm_feature": "Compliance Center · Verifiable Compliance Evidence",
        "disruption": {
            "sovereign": {
                "uptime_loss": 0,
                "compliance_loss": 0,
                "ai_loss": 0,
                "risk_gain": 0,
            },
            "external": {
                "uptime_loss": 0,
                "compliance_loss": 38,
                "ai_loss": 5,
                "risk_gain": 25,
            },
        },
    },

    # ------------------------------------------------------------------
    # Round 3 — The Data Exfiltration Suspicion
    # ------------------------------------------------------------------
    {
        "id": "data_exfiltration",
        "title": "🔐 Data Exfiltration Suspicion",
        "tags": ["Data Sovereignty", "AI Governance"],
        "narrative": (
            "A whistleblower alleges that patient health records processed by your public-cloud "
            "AI vendor are being copied to servers in a jurisdiction with weak privacy laws. "
            "Your privacy officer needs to prove — within hours — that no data has left your "
            "sovereign boundary.\n\n"
            "On the external cloud, you have no visibility into where data is stored or "
            "processed inside the vendor's infrastructure.\n\n"
            "On IBM Sovereign Core, all AI inferencing runs **within the tenant boundary**, "
            "with metered, observable data flows and full operator audit trails."
        ),
        "sovereign_impact": (
            "✅ Privacy officer pulls full data-flow audit in 3 minutes. "
            "Zero data-residency violations detected. Regulatory inquiry closed."
        ),
        "external_impact": (
            "🔴 Vendor refuses to disclose internal routing. Privacy officer cannot "
            "certify data residency. Regulator opens a formal investigation."
        ),
        "question": (
            "Which IBM Sovereign Core capability lets you prove that AI workloads "
            "never processed data outside your sovereign boundary?"
        ),
        "options": {
            "a": "IBM's contractual data-processing agreement",
            "b": "Tenant plane with in-boundary AI inferencing and metered data-flow observability",
            "c": "End-to-end TLS encryption on all API calls",
            "d": "Private link to the nearest IBM Cloud region",
        },
        "correct": "b",
        "explanation": (
            "IBM Sovereign Core runs AI models on a **tenant plane** that the operator controls. "
            "Every workload is deployed inside the sovereign boundary; metering, observability, "
            "and usage tracking are built into the Foundation layer. Combined with the AI Services "
            "layer (secure, governed AI inferencing and agents), operators can produce cryptographic "
            "proof that data never traversed an external boundary."
        ),
        "ibm_feature": "Tenant plane · AI Services · Foundation observability",
        "disruption": {
            "sovereign": {
                "uptime_loss": 0,
                "compliance_loss": 0,
                "ai_loss": 0,
                "risk_gain": 0,
            },
            "external": {
                "uptime_loss": 5,
                "compliance_loss": 30,
                "ai_loss": 10,
                "risk_gain": 40,
            },
        },
    },

    # ------------------------------------------------------------------
    # Round 4 — The GPU Shortage Emergency
    # ------------------------------------------------------------------
    {
        "id": "gpu_shortage",
        "title": "🖥️ GPU Shortage Emergency",
        "tags": ["Infrastructure Flexibility", "AI Within Your Control"],
        "narrative": (
            "A global chip shortage means your cloud AI provider can no longer allocate "
            "GPUs to your contract. They offer a queued upgrade in 4–6 months — but your "
            "fraud models need sub-second inference now.\n\n"
            "On the public cloud, the only option is to wait or pay a 10× premium for "
            "reserved capacity in a distant region — which introduces latency and "
            "new data-residency concerns.\n\n"
            "On IBM Sovereign Core, your team switches the same AI models to run on "
            "**CPU-based inference** with no redeployment required, maintaining service "
            "while GPU capacity is sourced locally."
        ),
        "sovereign_impact": (
            "✅ Smaller foundation models switched to CPU inference in 12 minutes. "
            "Latency: 340 ms vs 180 ms GPU baseline — acceptable for batch scoring. "
            "Zero data-residency change."
        ),
        "external_impact": (
            "🔴 AI model unavailable for 6 weeks pending GPU allocation. "
            "Manual review team engaged at 3× the operating cost."
        ),
        "question": (
            "IBM Sovereign Core allows AI models to run on CPUs when GPU capacity "
            "is unavailable. What is the primary design principle that enables this?"
        ),
        "options": {
            "a": "Automatic model quantisation performed by IBM's cloud team",
            "b": "Hardware optionality and open-standard OpenShift orchestration",
            "c": "Reserved GPU instances in IBM Cloud always available as fallback",
            "d": "AI models are cached on edge appliances during outages",
        },
        "correct": "b",
        "explanation": (
            "IBM Sovereign Core's **hardware optionality** layer abstracts workloads from the "
            "underlying silicon. Built on Red Hat OpenShift (and OpenShift Virtualisation), it "
            "allows the same containerised AI workloads to run on GPUs, CPUs, or specialised "
            "accelerators — on bare metal, virtual machines, or any customer-provided compute. "
            "Operators choose the hardware; the platform handles the rest."
        ),
        "ibm_feature": "Hardware optionality · AI Within Your Control (CPU & GPU)",
        "disruption": {
            "sovereign": {
                "uptime_loss": 0,
                "compliance_loss": 0,
                "ai_loss": 8,
                "risk_gain": 0,
            },
            "external": {
                "uptime_loss": 20,
                "compliance_loss": 5,
                "ai_loss": 55,
                "risk_gain": 20,
            },
        },
    },

    # ------------------------------------------------------------------
    # Round 5 — The New Regulation Challenge
    # ------------------------------------------------------------------
    {
        "id": "new_regulation",
        "title": "📜 The New Regulation",
        "tags": ["Regulatory Compliance", "Platform Extensibility"],
        "narrative": (
            "A new national AI regulation mandates that all AI systems processing citizen "
            "data must include an explainability audit trail and log every model decision "
            "within the national boundary — starting in 30 days.\n\n"
            "On the external cloud, compliance requires negotiating a contract amendment "
            "with the vendor, waiting for a roadmap update, and hoping the new logging "
            "feature ships in time.\n\n"
            "On IBM Sovereign Core, the team adds a certified explainability service from "
            "the governed catalog in one afternoon — no vendor negotiation, no timeline risk."
        ),
        "sovereign_impact": (
            "✅ Explainability service deployed from the catalog in 4 hours. "
            "Compliance posture updated to 99 %. Regulator notified automatically "
            "via Compliance Center evidence export."
        ),
        "external_impact": (
            "🟠 Vendor confirms feature will be in Q3 roadmap — 5 months away. "
            "Legal team engages to seek a regulatory extension. Outcome uncertain."
        ),
        "question": (
            "Which IBM Sovereign Core component enables new approved services "
            "(like explainability tools) to be added quickly without platform redesign?"
        ),
        "options": {
            "a": "The IBM Marketplace public SaaS catalogue",
            "b": "The governed extensible catalog within the sovereign boundary",
            "c": "An IBM Professional Services engagement to customise the stack",
            "d": "A public API integration with any open-source package",
        },
        "correct": "b",
        "explanation": (
            "IBM Sovereign Core includes a **governed, extensible catalog** that hosts IBM, "
            "open-source, partner, and customer-supplied services. It currently offers "
            "24+ additional software entries across AI, data, governance, automation, databases, "
            "middleware, privacy technology, and data movement — all pre-validated for the "
            "sovereign boundary. Operators can discover, approve, and provision services "
            "without redesigning the platform."
        ),
        "ibm_feature": "Governed extensible catalog · Platform extensibility",
        "disruption": {
            "sovereign": {
                "uptime_loss": 0,
                "compliance_loss": 0,
                "ai_loss": 0,
                "risk_gain": 0,
            },
            "external": {
                "uptime_loss": 0,
                "compliance_loss": 45,
                "ai_loss": 0,
                "risk_gain": 30,
            },
        },
    },
]

# Index for O(1) lookup by scenario id
SCENARIO_BY_ID = {s["id"]: s for s in SCENARIOS}
