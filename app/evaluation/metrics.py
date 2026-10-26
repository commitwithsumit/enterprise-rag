def calculate_accuracy(correct: int, total: int) -> float:
    if total == 0:
        return 0.0

    return correct / total


def calculate_precision(
    relevant_retrieved: int,
    total_retrieved: int,
) -> float:

    if total_retrieved == 0:
        return 0.0

    return relevant_retrieved / total_retrieved


def calculate_recall(
    relevant_retrieved: int,
    total_relevant: int,
) -> float:

    if total_relevant == 0:
        return 0.0

    return relevant_retrieved / total_relevant


def calculate_f1(
    precision: float,
    recall: float,
) -> float:

    if precision + recall == 0:
        return 0.0

    return (
        2 * precision * recall
        / (precision + recall)
    )