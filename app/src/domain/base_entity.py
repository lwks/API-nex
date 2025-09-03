from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class BaseEntity:
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
