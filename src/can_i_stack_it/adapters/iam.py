from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol, Any, Literal, TypedDict
from ..domain.model import Action, PermissionStatus, ActionPermission


type EvalDecision = Literal["allowed", "implicitDeny", "explicitDeny"]


class IAMEvaluationResult(TypedDict):
    EvalActionName: str
    EvalDecision: EvalDecision


@dataclass(frozen=True)
class IAMProtocol(Protocol):
    client: Any

    def simulate(
        self,
        role: str,
        actions: Iterable[str],
    ) -> Iterable[ActionPermission]: ...


@dataclass(frozen=True)
class IAM(IAMProtocol):
    client: Any

    def simulate(
        self,
        role: str,
        actions: Iterable[str],
    ) -> Iterable[ActionPermission]:
        paginator = self.client.get_paginator("simulate_principal_policy")
        for page in paginator.paginate(PolicySourceArn=role, ActionNames=list(actions)):
            for result in page["EvaluationResults"]:
                evaluation_result = IAMEvaluationResult(result)

                action = Action(evaluation_result["EvalActionName"])

                match evaluation_result["EvalDecision"]:
                    case "allowed":
                        permission = PermissionStatus.ALLOWED
                    case "implicitDeny" | "explicitDeny":
                        permission = PermissionStatus.DENIED
                    case _:
                        permission = PermissionStatus.UNKNOWN

                yield ActionPermission(action=action, permission=permission)
