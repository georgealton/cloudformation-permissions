import re

from boto3 import client
from cloudformation_permissions.adapters import sts


def test_sts():
    c = client("sts")
    s = sts.STS(c)
    role_pattern = "arn:aws:iam::.*:role/.*"
    assert re.fullmatch(role_pattern, str(s())) is not None
