from __future__ import annotations

from collections.abc import Iterable

from app.core.auth import hash_password
from app.models.domain import AlertRecord, AuthorityUser


class AuthorityRepository:
    def __init__(self) -> None:
        self._users = {
            "admin": AuthorityUser(
                username="admin",
                hashed_password=hash_password("glofsentinel123"),
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


authority_repository = AuthorityRepository()
alert_repository = AlertRepository()
