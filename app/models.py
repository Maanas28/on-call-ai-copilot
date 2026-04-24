from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Incident:
    id: str
    title: str
    severity: str
    status: str
    assigned_to: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    created_at: str = ""


@dataclass
class Engineer:
    id: str
    name: str
    is_on_call: bool