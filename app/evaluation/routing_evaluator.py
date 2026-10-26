from app.query.analyzer import analyze_query
from app.query.router import route_query


TEST_CASES = [
    {
        "query": "What does the security incident response policy say?",
        "expected_intent": "POLICY_SEARCH",
        "expected_sources": ["DOCUMENT"],
    },
    {
        "query": "What was the Q3 financial variance?",
        "expected_intent": "FINANCIAL_QUERY",
        "expected_sources": ["STRUCTURED"],
    },
    {
        "query": "Were there multiple login failures for Kavya?",
        "expected_intent": "SECURITY_EVENT_QUERY",
        "expected_sources": ["JSON_LOG"],
    },
    {
        "query": "What is the project status?",
        "expected_intent": "PROJECT_QUERY",
        "expected_sources": ["STRUCTURED"],
    },
    {
        "query": "What is the Authentication API error rate?",
        "expected_intent": "OPERATIONAL_QUERY",
        "expected_sources": [
            "STRUCTURED",
            "JSON_LOG",
        ],
    },
    {
        "query": "What happened during the security incident?",
        "expected_intent": "INCIDENT_ANALYSIS",
        "expected_sources": [
            "JSON_LOG",
            "STRUCTURED",
            "DOCUMENT",
        ],
    },
]


def evaluate_routing():

    correct_intents = 0
    correct_sources = 0

    total = len(TEST_CASES)

    for case in TEST_CASES:

        analysis = analyze_query(case["query"])
        actual_sources = route_query(analysis)

        intent_match = (
            analysis.intent
            == case["expected_intent"]
        )

        source_match = (
            actual_sources
            == case["expected_sources"]
        )

        if intent_match:
            correct_intents += 1

        if source_match:
            correct_sources += 1

        print("\nQuery:", case["query"])
        print("Expected intent:", case["expected_intent"])
        print("Actual intent:", analysis.intent)
        print("Expected sources:", case["expected_sources"])
        print("Actual sources:", actual_sources)

    intent_accuracy = correct_intents / total
    source_accuracy = correct_sources / total

    return {
        "intent_accuracy": intent_accuracy,
        "source_accuracy": source_accuracy,
    }