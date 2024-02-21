from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Note

class NoteAPITest(APITestCase):
    def setUp(self):
        self.valid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNzA4NzAzOTU2LCJpYXQiOjE3MDg0ODc5NTZ9.mUXJMuc5wxAbyp2zBU5iY65IG0SYS0IyRwrsOD4XN9c"
        self.invalid_token = "eyJ0eXAiOiJKV1QqLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNzA4NzAzOTU2LCJpYXQiOjE3MDg0ODc5NTZ9.mUXJMuc5wxAbyp2zBU5iY65IG0SYS0IyRwrsOD4XN9c"
        self.note_data = {
            "owner": "1",
            "content": "This is the test content of the model"
        }
        self.update_data = {
                "modifier": 2,
                "content": "This is not working"
}

    def test_create_note_success(self):
        url = reverse('create-note')
        response = self.client.post(url, self.note_data, format='json', headers={
            "Authorization": self.valid_token
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_note_unauthorized(self):
        url = reverse('create-note')
        response = self.client.post(url, self.note_data, format='json', headers={
            "Authorization": self.invalid_token
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_fetch_note_success(self):
        # Assuming 'id' is a valid note ID
        url = reverse('get-note', args=[1])
        response = self.client.get(url, headers={"Authorization": self.valid_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_note_not_found(self):
        # Assuming 'id' is an invalid note ID
        url = reverse('get-note', args=[999])
        response = self.client.get(url, headers={"Authorization": self.valid_token})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_share_note_success(self):
        # Create a note
        note = Note.object.create(owner="1", content="Test content")

        url = reverse('share-note')
        data = {
            "note": note.id,
            "user": "shared_user_id"
        }
        response = self.client.post(url, data, format='json', headers={
            "Authorization": f"Bearer {self.valid_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'Note shared with user')

    def test_share_note_unauthorized(self):
        # Create a note
        note = Note.object.create(owner="1", content="Test content")

        url = reverse('share-note')
        data = {
            "note": note.id,
            "user": "shared_user_id"
        }
        response = self.client.post(url, data, format='json', headers={
            "Authorization": f"Bearer {self.invalid_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_note_success(self):
        url = reverse('update-note', args=[1])
        response = self.client.put(url, self.update_data, format='json', headers={
            "Authorization": f"Bearer {self.valid_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Note updated and changes recorded")
        # Add more assertions as needed

    def test_update_note_unauthorized(self):
        url = reverse('update-note', args=[1])
        response = self.client.put(url, self.update_data, format='json', headers={
            "Authorization": f"Bearer {self.invalid_token}"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_changes_success(self):
        url = reverse('get-changes', args=[1])
        response = self.client.get(url, headers={"Authorization": f"Bearer {self.valid_token}"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add assertions to validate response data

    def test_get_changes_unauthorized(self):
        url = reverse('get-changes', args=[1])
        response = self.client.get(url, headers={"Authorization": f"Bearer {self.invalid_token}"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)