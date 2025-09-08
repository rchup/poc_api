from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass(frozen=True)
class ClientConfig:
    base_url: str
    timeout_seconds: float = 10.0
    max_retries: int = 3
    backoff_factor: float = 0.3
    verify_ssl: bool = True
    api_key: Optional[str] = None
    default_headers: Dict[str, str] = field(default_factory=dict)
    log_level: str = "INFO"
