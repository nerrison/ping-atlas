def test_create_endpoint(client, group_payload, endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']

    response = client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    assert response.json()["status"] == "UNKNOWN"
    assert response.status_code == 200

def test_create_duplicate_endpoint(client, group_payload, endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']

    first_response=client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )
    assert first_response.status_code == 200

    second_response = client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    assert second_response.json()["detail"] == "Endpoint already exists in this group"
    assert second_response.status_code == 409

def test_list_endpoints_per_group(client,group_payload,endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']
    client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    response = client.get(
        f"/groups/{group_id}/endpoints"
    )

    assert response.status_code == 200

def test_get_endpoint(client,group_payload,endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )
    group=group_create_response.json()

    group_id= group['id']
    endpoint_create_response=client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )
    endpoint = endpoint_create_response.json()

    endpoint_id = endpoint['id']
    response = client.get(
        f"/endpoints/{endpoint_id}"
    )

    assert response.status_code == 200

def test_list_endpoints(client,group_payload,endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']
    client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    response = client.get(
        "/endpoints"
    )
    
    
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

def test_endpoint_patch(client, group_payload,endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']
    endpoint_create_response=client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    endpoint = endpoint_create_response.json()
    endpoint_id = endpoint['id']

    response = client.patch(
        f"/endpoints/{endpoint_id}",
        json={
            "description": "Home page",
        })
    
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == "Home page"
    assert data["name"] == "Main website"

def test_endpoint_put(client, group_payload,endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']
    endpoint_create_response=client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    endpoint = endpoint_create_response.json()
    endpoint_id = endpoint['id']

    response = client.patch(
        f"/endpoints/{endpoint_id}",
        json={
            "name": "sign In",
            "type": "https",
            "url": "https://acounts.google.com/",
            "description": "Sign In page",
            "method": "POST"
        })
    
    assert response.status_code == 200
    data=response.json()

    assert data["name"] == "sign In"

def test_delete_endpoint(client, group_payload, endpoint_payload):
    group_create_response=client.post(
        "/groups",
        json=group_payload
    )

    group=group_create_response.json()
    
    group_id= group['id']
    endpoint_create_response=client.post(
        f"/groups/{group_id}/endpoints",
        json=endpoint_payload
    )

    endpoint = endpoint_create_response.json()
    endpoint_id = endpoint['id']

    response = client.delete(
        f"/endpoints/{endpoint_id}"
    )

    assert response.status_code == 200
    
    get_response = client.get(
        f"/endpoints/{endpoint_id}"
    )

    assert get_response.status_code == 404
    
