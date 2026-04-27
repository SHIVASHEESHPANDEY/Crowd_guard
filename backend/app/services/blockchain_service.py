import hashlib
import json


class BlockchainService:
    def anchor_identity(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def verify_hash(self, payload: dict, blockchain_hash: str) -> bool:
        return self.anchor_identity(payload) == blockchain_hash


blockchain_service = BlockchainService()
