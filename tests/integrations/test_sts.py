import pytest

from boto3 import client
from can_i_stack_it.adapters import sts


def test_sts():
    c = client("sts")
    s = sts.STS(c)
    assert (
        s()["Arn"]
        == "arn:aws:sts::737710810646:assumed-role/AWSReservedSSO_EvertzIOAdmin_e2e5cb6ac866872e/galton@evertz.com"
    )
