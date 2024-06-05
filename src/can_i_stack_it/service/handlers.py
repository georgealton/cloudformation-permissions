from dataclasses import dataclass
from types import MappingProxyType
from typing import Protocol, Self, get_type_hints

from ..adapters.iam import IAMProtocol
from ..adapters.cloudformation import CloudFormationProtocol
from ..adapters.sts import STSProtocol
from ..domain.commands import Command, ListPermissions, VerifyPermissions


class Handler(Protocol):
    __registry: dict[type[Command], type[Self]] = {}
    registry = MappingProxyType(__registry)

    def __init_subclass__(CommandHandler) -> None:
        command_type: type[Command] = get_type_hints(CommandHandler.__call__)["command"]
        Handler.__registry[command_type] = CommandHandler

    def __call__(self, command: Command) -> None: ...


@dataclass
class HandleListPermissions(Handler):
    cloudformation: CloudFormationProtocol

    def __call__(self, command: ListPermissions):
        template_source = command.TemplateSource
        self.cloudformation.get_template_resources(template_source)


@dataclass
class HandleVerifyPermissions(Handler):
    cloudformation: CloudFormationProtocol
    iam: IAMProtocol
    sts: STSProtocol

    def __call__(self, command: VerifyPermissions):
        template_source = command.TemplateSource
        if (role := command.Role) is None:
            role = self.sts()

        self.cloudformation.get_template_resources(template_source)
        self.iam.simulate(role)
