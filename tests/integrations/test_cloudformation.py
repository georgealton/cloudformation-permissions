import pytest

from boto3 import client
from can_i_stack_it.adapters import cloudformation


def test_local():
    c = client("cloudformation")
    s = cloudformation.LocalAdapter(c)
    r = s.get_template_resources(
        """
        Resources:
            Test:
                Type: AWS::IAM::Role
                Properties:
        """
    )
    assert list(r) == [False]
