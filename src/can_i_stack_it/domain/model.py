from enum import StrEnum, auto
from dataclasses import dataclass


class PermissionStatus(StrEnum):
    ALLOWED = auto()
    DENIED = auto()
    UNKNOWN = auto()


Action = type[str]


@dataclass
class ActionPermission:
    action: Action
    permission: PermissionStatus


@dataclass
class ShortResourceInfo:
    TypeName: str
    LogicalId: str


@dataclass
class TemplatePermissionsSummary:
    source: str

    def verify(
        self,
    ):
        pass

    def list_permissions(
        self,
    ):
        pass
