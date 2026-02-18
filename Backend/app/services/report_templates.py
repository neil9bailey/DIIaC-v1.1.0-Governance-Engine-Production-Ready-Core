# app/services/report_templates.py

REPORT_TEMPLATES = {
    "vendorlogic_v1": {
        "template_file": "vendorlogic_report_v1.docx",
        "version": "1.0.0",
        "sections": [
            "executive_summary",
            "strategic_objectives",
            "constraints_and_risks",
            "strategy_and_roadmap",
        ],
        "disclaimer": (
            "This report is generated from validated decision records. "
            "Language has been normalised for clarity. "
            "No guarantees of correctness or outcomes are implied."
        ),
    }
}
