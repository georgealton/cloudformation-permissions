from dataclasses import dataclass
from typing import Protocol, Iterable, Any

from ..domain.model import ShortResourceInfo

import json
import yaml


@dataclass
class CloudFormation(Protocol):
    client: Any

    def get_template_resources(
        self, template_source
    ) -> Iterable[ShortResourceInfo]: ...

    def permissions_for_resource_type(self, resource_type: str) -> Iterable[str]: ...
    @staticmethod
    def region_from_arn(arn: str) -> str:
        return arn.split(":")[3]


@dataclass
class StackAdapter(CloudFormation):
    def get_template_resources(self, template_source):
        for resource in paginator.paginate(StackName=template_source):
            for resource in resource["StackResourceSummaries"]:
                yield ShortResourceInfo(
                    TypeName=resource["ResourceType"],
                    LogicalId=resource["LogicalResourceId"],
                )

    def permissions_for_resource_type(
        self,
        resource_type: str,
    ) -> frozenset[str]:
        resource_type_description = self.client.describe_type(
            Type="RESOURCE", TypeName=resource_type
        )
        schema = json.loads(resource_type_description["Schema"])
        permission_set: set[str] = set()

        for operation, properties in schema["handlers"].items():
            if not properties["permissions"]:
                print(
                    f"Permissions Not Available for {operation} {resource_type_description}"
                )
            permission_set.update(properties["permissions"])
        return frozenset(permission_set)


@dataclass
class ChangeSetAdapter(CloudFormation):
    def get_template_resources(self, template_source):
        template = self.client.get_template(
            ChangeSetName=template_source, TemplateStage="Processed"
        )
        yield from resources_from_template_string(template["TemplateBody"])


@dataclass
class LocalAdapter(CloudFormation):
    def get_template_resources(self, template_source):
        for logical_id, properties in template_source["Resources"].items():
            yield ShortResourceInfo(
                LogicalId=logical_id,
                TypeName=properties["Type"],
            )
