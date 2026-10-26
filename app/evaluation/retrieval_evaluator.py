from app.retrieval.retriever import retrieve


RETRIEVAL_TEST_CASES = [
    {
        "query": "What was the Q3 financial variance?",
        "expected_source": "financial_records.csv",
    },
    {
        "query": "Were there multiple login failures for Kavya?",
        "expected_source": "authentication_events.json",
    },
    {
        "query": "What happened during the security incident?",
        "expected_source": "security_events.json",
    },
]


def evaluate_retrieval():

    correct = 0
    total = len(RETRIEVAL_TEST_CASES)

    for case in RETRIEVAL_TEST_CASES:

        results = retrieve(
            case["query"],
            top_k=3,
        )

        source_ids = [
            result.source_id
            for result in results
        ]

        expected = case["expected_source"]

        matched = expected in source_ids

        if matched:
            correct += 1

        print("\nQuery:", case["query"])
        print("Expected source:", expected)
        print("Retrieved sources:", source_ids)
        print("Relevant source found:", matched)

    accuracy = correct / total

    return accuracy