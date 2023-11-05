from dataclasses import dataclass


@dataclass(slots=True)
class User:
    "用户信息"
    id: str
    name: str = ""
    avatar: str | None = None


@dataclass(slots=True)
class Group:
    "群聊信息"
    id: str
    name: str = ""
    avatar: str | None = None
    owner_id: str | None = None
    member_count: int | None = None
    max_members: int | None = None
