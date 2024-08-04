"""A set of non-exhaustive tests for user permissions in different scenarios."""


def test_unverified_user_permissions(unverified_client):
    """Test permissions for an unverified user."""
    client = unverified_client
    response = client.get("/samples/")
    assert response.status_code == 200

    response = client.post("/new-sample/", json={"item_id": "test"})
    assert response.status_code == 401

    response = client.get("/starting-materials/")
    assert response.status_code == 200


def test_deactivated_user_permissions(deactivated_client):
    """Test permissions for a deactivated user."""
    client = deactivated_client
    response = client.get("/samples/")
    assert response.status_code == 200

    response = client.post("/new-sample/", json={"item_id": "test"})
    assert response.status_code == 401

    response = client.get("/starting-materials/")
    assert response.status_code == 200


def test_unauthenticated_user_permissions(unauthenticated_client):
    """Test permissions for an unauthenticated user."""
    client = unauthenticated_client
    response = client.get("/samples/")
    assert response.status_code == 401

    response = client.post("/new-sample/", json={"item_id": "test"})
    assert response.status_code == 401

    response = client.get("/starting-materials/")
    assert response.status_code == 401


def test_basic_permissions_update(admin_client, admin_user_id, client, user_id):
    """Test that an admin can share an item with a normal user."""

    response = admin_client.get("/new-sample/", json={"item_id": "test-admin-sample"})
    assert response.status_code == 200

    response = admin_client.get("/get-item-data/test-admin-sample")
    assert response.status_code == 200
    refcode = response["item_data"]["refcode"]

    response = client.get(f"/items/{refcode}")
    assert response.status_code == 404

    admin_client.patch(f"/items/{refcode}", json={"creators": [{"immutable_id": user_id}]})
    assert response.status_code == 200

    response = client.get(f"/items/{refcode}")
    assert response.status_code == 200

    client.patch(f"/items/{refcode}", json={"creators": []})
    assert response.status_code == 200

    response = client.get(f"/items/{refcode}")
    assert response.status_code == 404
