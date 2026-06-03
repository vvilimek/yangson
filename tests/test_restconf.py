"""Test examples provided in the RFC 8040: RESTCONF Protocol.

We only focus on examples for module ietf-restconf.
"""

import pytest
from yangson import DataModel
from yangson.instance import ObjectMember, ObjectValue, ArrayValue, ArrayEntry, InstanceIdParser

@pytest.fixture
def data_model():
    return DataModel.from_file("yang-modules/test-restconf/yang-library.json", ["yang-modules/ietf"])

@pytest.fixture
def data_restconf():
    _data = {
        "ietf-restconf:restconf": {
            "data": {},
            "operations": {},
            "yang-library-version": "2016-06-21",
            },
        }
    return _data

@pytest.fixture
def data_errors():
    _data = {
        "ietf-restconf:errors": {
            "error": [
                    {
                    "error-type": "protocol",
                    "error-tag": "invalid-value",
                    "error-path": "/example-ops:input/delay",
                    "error-message": "Invalid input parameter",
                    },
                ],
            },
        }
    return _data


def test_restconf_instance(data_model, data_restconf):
    cooked = data_model.from_raw(data_restconf)
    restconf = cooked["ietf-restconf:restconf"]
    assert type(restconf) == ObjectMember
    assert restconf["data"].value == ObjectValue({})
    assert restconf["operations"].value == ObjectValue({})
    assert restconf["yang-library-version"].value == "2016-06-21"

def test_errors_instance(data_model, data_errors):
    cooked = data_model.from_raw(data_errors)
    errors = cooked["ietf-restconf:errors"]
    assert type(errors) == ObjectMember
    array = errors["error"]
    assert type(array.value) == ArrayValue
    err = array[0]
    assert type(err) == ArrayEntry
    assert err.value["error-type"] == "protocol"
    assert err.value["error-tag"] == "invalid-value"
    assert err.value["error-path"] == InstanceIdParser("/example-ops:input/delay").parse()
    assert err.value["error-message"] == "Invalid input parameter"

def test_nids(data_model):
    schema = data_model.schema
    route = data_model.schema_data.nid2route(
            nid="/ietf-restconf:errors",
            schema=schema)
    assert route == [("yang-errors", "ietf-restconf"), ("errors", "ietf-restconf")]

    expected_node = schema.get_child("yang-errors", "ietf-restconf").get_child("errors", "ietf-restconf")
    assert schema.get_schema_descendant(route) is expected_node

    route = data_model.schema_data.nid2route(
            nid="/ietf-restconf:errors/error/error-type",
            schema=schema)
    assert route == [("yang-errors", "ietf-restconf"), ("errors", "ietf-restconf"), ("error", "ietf-restconf"), ("error-type", "ietf-restconf")]

    expected_node = expected_node.get_child("error", "ietf-restconf").get_child("error-type", "ietf-restconf")
    assert schema.get_schema_descendant(route) == expected_node

