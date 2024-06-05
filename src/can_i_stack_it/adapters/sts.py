from dataclasses import dataclass
from typing import Any, Protocol


class STSProtocol(Protocol):
    client: Any

    def __call__(self) -> str: ...


@dataclass
class STS(STSProtocol):
    client: Any

    def __build_role_from_session(self, arn: str) -> str:
        arn_prefix, _, resource_id = arn.partition("assumed-role")
        arn_prefix = arn_prefix.replace("sts", "iam")
        resource_id = resource_id.rpartition("/")[0]
        return f"{arn_prefix}role{resource_id}"

    def __get_current_role(self,) -> str:
        identity = self.client.get_caller_identity()
        arn = identity["Arn"]
        iam_role_arn = self.__build_role_from_session(arn)
        return iam_role_arn

    def __call__(self) -> str:
        return self.__get_current_role()
