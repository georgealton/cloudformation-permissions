import json

from dataclasses import dataclass
from typing import Protocol, Iterable, Any, TypedDict

from ..domain.model import Action, ShortResourceInfo


type Permission = str
class Handler(TypedDict):
    permissions: list[Permission]
    timeoutInMinutes: int

class HandlerTypes(TypedDict):
    create: Handler
    update: Handler
    delete: Handler
    read: Handler
    list: Handler

class ResourceProviderSchema(TypedDict):
    handlers: HandlerTypes

@dataclass
class CloudFormationProtocol(Protocol):
    client: Any

    def get_template_resources(
        self,
        template_source: str,
    ) -> Iterable[ShortResourceInfo]: ...

    def permissions_for_resource_type(
        self,
        resource_type: str,
    ) -> Iterable[Action]: ...

    @staticmethod
    def region_from_arn(arn: str) -> str:
        return arn.split(":")[3]


@dataclass
class StackAdapter(CloudFormationProtocol):
    client: Any

    def get_template_resources(
        self,
        template_source: str,
    ):
        for resource in paginator.paginate(StackName=template_source):
            for resource in resource["StackResourceSummaries"]:
                yield ShortResourceInfo(
                    TypeName=resource["ResourceType"],
                    LogicalId=resource["LogicalResourceId"],
                )

    def permissions_for_resource_type(
        self,
        resource_type: str,
    ) -> frozenset[Action]:
        resource_type_description = self.client.describe_type(
            Type="RESOURCE", TypeName=resource_type
        )
        schema: ResourceProviderSchema = json.loads(resource_type_description["Schema"])
        permission_set: set[Action] = set()

        handlers = schema["handlers"]
        for operation, properties in handlers.items():
            if not properties["permissions"]:
                print(
                    f"Permissions Not Available for {operation} {resource_type_description}"
                )
            permission_set.update(properties["permissions"])
        return frozenset(permission_set)


@dataclass
class ChangeSetAdapter(CloudFormationProtocol):
    client: Any

    def get_template_resources(
        self,
        template_source: str,
    ) -> ShortResourceInfo:
        template = self.client.get_template(
            ChangeSetName=template_source,
            TemplateStage="Processed",
        )
        yield from resources_from_template_string(template["TemplateBody"])


@dataclass
class LocalAdapter(CloudFormationProtocol):
    client: Any

    def get_template_resources(
        self,
        template_source: str,
    ) -> ShortResourceInfo:
        for logical_id, properties in template_source["Resources"].items():
            yield ShortResourceInfo(
                LogicalId=logical_id,
                TypeName=properties["Type"],
            )
