from dataclasses import dataclass, field


@dataclass
class QueryAnalysis:
    original_query: str
    intent: str
    source_types: list[str] = field(
        default_factory=list
    )
    entities: dict = field(
        default_factory=dict
    )
    retrieval_hints: dict = field(default_factory=dict)
    reasoning: str = ""