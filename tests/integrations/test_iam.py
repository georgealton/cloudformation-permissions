import pytest

from boto3 import client
from can_i_stack_it.domain.model import ActionPermission, Action, PermissionStatus
from can_i_stack_it.adapters import iam


@pytest.mark.parametrize(
    "role, actions, result",
    [
        (
            "arn:aws:iam::737710810646:role/PlanGitHubRoles",
            [
                "sts:GetCallerIdentity",
            ],
            [
                ActionPermission(
                    Action("sts:GetCallerIdentity"), PermissionStatus.ALLOWED
                ),
            ],
        ),
        (
            "arn:aws:iam::737710810646:role/PlanGitHubRoles",
            [
                "ec2:RunInstances",
            ],
            [
                ActionPermission(Action("ec2:RunInstances"), PermissionStatus.DENIED),
            ],
        ),
        (
            "arn:aws:iam::737710810646:role/PlanGitHubRoles",
            [
                "sts:GetCallerIdentity",
                "ec2:RunInstances",
            ],
            [
                ActionPermission(
                    Action("sts:GetCallerIdentity"), PermissionStatus.ALLOWED
                ),
                ActionPermission(Action("ec2:RunInstances"), PermissionStatus.DENIED),
            ],
        ),
    ],
    ids=[
        "Allowed",
        "Denied",
        "AllowedAndDenied",
    ],
)
def test_simulate(role, actions, result):
    iam_client = client("iam")
    adapter = iam.IAM(iam_client)
    assert result == list(adapter.simulate(role, actions))
