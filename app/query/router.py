from app.query.models import QueryAnalysis


SOURCE_PRIORITY = {
    "POLICY_SEARCH": [
        "DOCUMENT",
    ],

    "FINANCIAL_QUERY": [
        "STRUCTURED",
    ],

    "EMPLOYEE_QUERY": [
        "STRUCTURED",
    ],

    "PROJECT_QUERY": [
        "STRUCTURED",
    ],

    "SECURITY_EVENT_QUERY": [
        "JSON_LOG",
    ],

    "OPERATIONAL_QUERY": [
        "STRUCTURED",
        "JSON_LOG",
    ],

    "INCIDENT_ANALYSIS": [
        "JSON_LOG",
        "STRUCTURED",
        "DOCUMENT",
    ],

    "GENERAL_QUERY": [
        "DOCUMENT",
    ],
}


def route_query(
    analysis: QueryAnalysis,
) -> list[str]:

    return SOURCE_PRIORITY.get(
        analysis.intent,
        ["DOCUMENT"],
    )