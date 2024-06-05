from __future__ import annotations
from collections.abc import Mapping

import punq

from .domain.commands import Command

from .adapters import iam, cloudformation, sts
from .service.handlers import Handler


def bootstrap() -> Mapping[type[Command], Handler]:
    container = punq.Container()

    container.register(iam.IAMProtocol, iam.IAM)
    container.register(cloudformation.CloudFormationProtocol, cloudformation.StackAdapter)
    container.register(sts.STSProtocol, sts.STSProtocol)

    return {
        Command: container.instantiate(Handler)
        for Command, Handler in Handler.registry.items()
    }
