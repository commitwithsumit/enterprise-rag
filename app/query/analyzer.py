import re

from app.query.models import QueryAnalysis


def analyze_query(
    query: str,
) -> QueryAnalysis:

    normalized = query.lower().strip()

    # --------------------------------
    # Policy / document queries
    # --------------------------------

    policy_keywords = [
        "policy",
        "procedure",
        "guideline",
        "architecture",
        "document",
        "what does",
    ]

    if any(
        keyword in normalized
        for keyword in policy_keywords
    ):

        return QueryAnalysis(
            original_query=query,
            intent="POLICY_SEARCH",
            source_types=["DOCUMENT"],
            reasoning=(
                "Query contains policy/document "
                "related terminology."
            ),
        )

    # --------------------------------
    # Financial queries
    # --------------------------------

    finance_keywords = [
        "revenue",
        "operating cost",
        "financial",
        "finance",
        "variance",
        "budget",
        "profit",
    ]

    if any(
        keyword in normalized
        for keyword in finance_keywords
    ):

        quarter = extract_quarter(
            normalized
        )

        entities = {}

        if quarter:
            entities["quarter"] = quarter

        retrieval_hints = {}
        retrieval_hints = {
            "structured": [
                "financial_records.csv"
            ]
        }

        return QueryAnalysis(
            original_query=query,
            intent="FINANCIAL_QUERY",
            source_types=["STRUCTURED"],
            entities=entities,
            retrieval_hints=retrieval_hints,
            reasoning=(
                "Query contains financial terminology."
            ),
        )

    # --------------------------------
    # Incident analysis
    # --------------------------------

    incident_keywords = [
        "what happened",
        "investigate",
        "investigation",
        "root cause",
        "incident analysis",
        "during the incident",
    ]

    if any(
        keyword in normalized
        for keyword in incident_keywords
    ):

        retrieval_hints = {
            "documents": [
                "security_incident_response.pdf"
            ],
            "structured": [
                "operational_metrics.csv"
            ],
            "json_logs": [
                "security_events.json",
                "authentication_events.json",
                "application_events.json"
            ]
        }

        return QueryAnalysis(
            original_query=query,
            intent="INCIDENT_ANALYSIS",
            source_types=[
                "JSON_LOG",
                "STRUCTURED",
                "DOCUMENT",
            ],
            retrieval_hints=retrieval_hints,
            reasoning=(
                "Query appears to require "
                "cross-source incident analysis."
            ),
        )

    # --------------------------------
    # Security event queries
    # --------------------------------

    security_keywords = [
        "login failure",
        "login failures",
        "authentication failure",
        "authentication failures",
        "security event",
        "security incident",
        "unauthorized access",
        "privileged access",
    ]

    if any(
        keyword in normalized
        for keyword in security_keywords
    ):

        user = extract_user(normalized)
        entities = {}
        if user:
            entities["user"] = user

        return QueryAnalysis(
            original_query=query,
            intent="SECURITY_EVENT_QUERY",
            source_types=["JSON_LOG"],
            entities=entities,
            reasoning=(
                "Query refers to authentication "
                "or security events."
            ),
        )

    # --------------------------------
    # Project queries
    # --------------------------------

    project_keywords = [
        "project status",
        "project",
        "milestone",
        "project manager",
    ]

    if any(
        keyword in normalized
        for keyword in project_keywords
    ):

        return QueryAnalysis(
            original_query=query,
            intent="PROJECT_QUERY",
            source_types=["STRUCTURED"],
            reasoning=(
                "Query refers to project information."
            ),
        )

    # --------------------------------
    # Operational queries
    # --------------------------------

    operational_keywords = [
        "availability",
        "error rate",
        "requests per second",
        "latency",
        "operational",
        "service health",
    ]

    if any(
        keyword in normalized
        for keyword in operational_keywords
    ):

        return QueryAnalysis(
            original_query=query,
            intent="OPERATIONAL_QUERY",
            source_types=[
                "STRUCTURED",
                "JSON_LOG",
            ],
            reasoning=(
                "Query refers to operational "
                "service metrics."
            ),
        )

    # --------------------------------
    # General query
    # --------------------------------

    return QueryAnalysis(
        original_query=query,
        intent="GENERAL_QUERY",
        source_types=["DOCUMENT"],
        reasoning=(
            "No specialized intent detected."
        ),
    )


def extract_quarter(
    query: str,
) -> str | None:

    match = re.search(
        r"\bq[1-4]\b",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(0).upper()

    return None

def extract_user(
    query: str,
) -> str | None:

    known_users = [
        "kavya",
        "aarav",
        "neha",
        "ishita",
        "pooja",
        "amit",
        "tanya",
        "dev",
    ]

    normalized = query.lower()

    for user in known_users:

        if user in normalized:
            return user

    return None