from __future__ import annotations

import punq

from .domain.commands import Command

from .adapters import iam, cloudformation
from .service.handlers import Handler


def bootstrap() -> dict[type[Command], Handler]:
    container = punq.Container()

    container.register("IAM", iam.IAM)
    container.register("CloudFormation", cloudformation.StackAdapter)

    return {
        Command: container.instantiate(Handler)
        for Command, Handler in Handler.registry.items()
    }
