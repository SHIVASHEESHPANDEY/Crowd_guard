from __future__ import annotations

from collections.abc import Iterable

from app.core.auth import hash_password
from app.models.domain import AlertRecord, AuthorityUser, TouristIdentity


class AuthorityRepository:
    def __init__(self) -> None:
        self._users = {
            "admin": AuthorityUser(
                username="admin",
                hashed_password=hash_password("crowdguard123"),
            )
        }

    def get_by_username(self, username: str) -> AuthorityUser | None:
        return self._users.get(username)


class AlertRepository:
    def __init__(self) -> None:
        self._alerts: list[AlertRecord] = []

    def add(self, alert: AlertRecord) -> None:
        self._alerts.insert(0, alert)

    def all(self) -> list[AlertRecord]:
        return list(self._alerts)

    def unresolved(self) -> Iterable[AlertRecord]:
        return (item for item in self._alerts if not item.resolved)


class TouristRepository:
    def __init__(self) -> None:
        self._tourists: dict[str, TouristIdentity] = {}

    def save(self, tourist: TouristIdentity) -> None:
        self._tourists[tourist.tourist_id] = tourist

    def get(self, tourist_id: str) -> TouristIdentity | None:
        return self._tourists.get(tourist_id)


authority_repository = AuthorityRepository()
alert_repository = AlertRepository()
tourist_repository = TouristRepository()
