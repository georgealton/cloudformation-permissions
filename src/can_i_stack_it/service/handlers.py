from dataclasses import dataclass
from types import MappingProxyType
from typing import Self, get_type_hints

from ..adapters.iam import IAMAdapter
from ..adapters.cloudformation import CloudFormation
from ..domain.commands import Command, ListPermissions, VerifyPermissions

class Handler:
    __registry: dict[type[Command], type[Self]] = {}
    registry = MappingProxyType(__registry)

    def __init_subclass__(cls) -> None:
        command_type: type[commands.Command] = get_type_hints(cls.__call__)["command"]
        Handler.__registry[command_type] = cls

    def __call__(self, command: Command) -> None: ...

@dataclass
class HandleListPermissions(Handler):
    cloudformation: CloudFormation

    def __call__(self, command: ListPermissions):
        template_source = command.TemplateSource
        self.cloudformation.get_template_resources(template_source)


@dataclass
class HandleVerifyPermissions(Handler):
    CloudFormation: CloudFormation
    IAM: IAMAdapter

    def __call__(self, command: VerifyPermissions):
        template_source = command.TemplateSource
        role = command.Role

        self.CloudFormation.get_template_resources(template_source)
        self.IAM.simulate(role)
