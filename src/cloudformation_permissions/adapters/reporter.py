import json

from typing import Protocol, Self, TypedDict, Literal

from attrs import field, frozen
from rich.console import Console
from rich.text import Text
from rich.tree import Tree

from ..domain.model import ResourcePermissionSummary, TemplateSummary


class Reporter(Protocol):
    def add_summary(self, summary: ResourcePermissionSummary) -> Self: ...


@frozen
class ListReporter(Reporter):
    items: list[Text] = field(factory=list)

    def __rich_console__(self, console: Console, options):
        yield from self.items

    def add_summary(self, summary_item: ResourcePermissionSummary | TemplateSummary) -> Self:
        match summary_item:
            case ResourcePermissionSummary():
                for permission in sorted(summary_item.permissions):
                    self.items.append(Text(permission))

            case TemplateSummary():
                for resource in summary_item.resources.values():
                    for permission in sorted(resource.permissions):
                        self.items.append(Text(permission))
        return self


@frozen
class ResourceReporterTree(Reporter):
    tree: Tree = field(init=False, factory=lambda: Tree("t"))

    def __rich_console__(self, console: Console, options):
        yield self.tree

    def add_summary(self, summary_item: ResourcePermissionSummary | TemplateSummary) -> Self:
        match summary_item:
            case ResourcePermissionSummary():
                self.tree.label = Text(
                    str(summary_item.resource_type), style="bold")
                for permission in sorted(summary_item.permissions):
                    self.tree.add(Text(permission))

            case TemplateSummary():
                self.tree.label = str(summary_item.source)
                for logical_id, resource in summary_item.resources.items():
                    logical_tree = self.tree.add(Text(logical_id))
                    resource_type_tree = logical_tree.add(
                        resource.resource_type)
                    for permission in sorted(resource.permissions):
                        resource_type_tree.add(Text(permission))
        return self


class IAMPolicy(TypedDict):
    Effect: Literal['Allow', 'Deny']
    Action: list[str] | str
    Resource: list[str] | str


@frozen
class IAMPolicyReporter(Reporter):
    policy: IAMPolicy = field(factory=lambda: IAMPolicy(Effect='Allow', Action=[], Resource='*' ))

    def __rich_console__(self, console: Console, options):
        yield json.dumps(self.policy, indent=4)

    def add_summary(self, summary: ResourcePermissionSummary | TemplateSummary) -> Self:
        match summary:
            case ResourcePermissionSummary():
                actions = sorted(str(permission) for permission in summary.permissions)
                self.policy["Action"] = actions

            case TemplateSummary():
                actions = []
                for logical_id, resource in summary.resources.items():
                    for permission in sorted(resource.permissions):
                        actions.append(permission)
                self.policy["Action"] = actions
        return self

