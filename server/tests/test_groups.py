def test_create_group(client, group_payload):
    response = client.post(
        "/groups",
        json=group_payload
    )

    print(response.json())
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "STMicroelectronics"
    assert data["slug"] == "stmicroelectronics"

def test_create_duplicate_group(client, group_payload):

    first_response = client.post(
        "/groups",
        json=group_payload
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/groups",
        json=group_payload
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Group already exists"

def test_create_group_name_too_short(client):
    response = client.post(
        "/groups",
        json={
            "name": "ST",
            "type": "customer",
            "description": "semiconductor manufacturing and design company"
        })
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Name too short"

def test_list_groups(client, group_payload):
    client.post(
        "/groups",
        json=group_payload
    )

    response = client.get("/groups")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "STMicroelectronics"

def test_get_group(client, group_payload):
    create_response = client.post(
        "/groups",
        json=group_payload
    )

    group = create_response.json()

    response = client.get(
        f"/groups/{group['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "STMicroelectronics"


def test_update_group(client, group_payload):
    create_response = client.post(
        "/groups",
        json=group_payload
    )

    group = create_response.json()

    response = client.put(
        f"/groups/{group['id']}",
        json={
            "name": "ST Updated",
            "slug": "st-updated",
            "type": "customer",
            "description": "updated description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "ST Updated"

def test_patch_group(client, group_payload):
    create_response = client.post(
        "/groups",
        json=group_payload
    )

    group = create_response.json()

    response = client.patch(
        f"/groups/{group['id']}",
        json={
            "description": "new description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "new description"
    assert data["name"] == "STMicroelectronics"

def test_delete_group(client, group_payload):
    create_response = client.post(
        "/groups",
        json=group_payload
    )

    group = create_response.json()

    response = client.delete(
        f"/groups/{group['id']}"
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/groups/{group['id']}"
    )

    assert get_response.status_code == 404