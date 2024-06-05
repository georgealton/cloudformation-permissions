from enum import StrEnum, auto
from dataclasses import dataclass
from typing import NewType


class PermissionStatus(StrEnum):
    ALLOWED = auto()
    DENIED = auto()
    UNKNOWN = auto()


Action = NewType("Action", str)


@dataclass
class ActionPermission:
    action: Action
    permission: PermissionStatus


@dataclass
class ShortResourceInfo:
    TypeName: str
    LogicalId: str


@dataclass
class TemplateResourcesPermissionsSummary:
    source: str

    def verify(
        self,
    ):
        pass

    def list_permissions(
        self,
    ):
        pass
