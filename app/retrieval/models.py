from dataclasses import dataclass, field


@dataclass
class RetrievalResult:
    source_type: str
    source_id: str
    content: str
    metadata: dict = field(default_factory=dict)
    score: float | None = None