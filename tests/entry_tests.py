import json
from rest_framework import status
from rest_framework.test import APITestCase
from commonplaceapi.models import Entry, Topic
from commonplaceapi.models.commonplace_user import CommonplaceUser



class EntryTests(APITestCase):
    """
        Tests for EntryView functions
    """

    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "email@gmail.com",
            "password": "thisisapassword",
            "first_name": "First Name",
            "last_name": "Last Name"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Seed database with one topic
        topic = Topic()
        topic.name = "this is a topic"
        topic.save()

    def test_create_entry(self):
        """
        Ensure we can create a new entry.
        """
        # Define entry properties
        url = "/entries"
        data = {
            "user": 1,
            "title": "This is a title",
            "body": "This is a body",
            "created_on": "2006-10-25 14:30:59",
            "entry_topics": [1]
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "This is a title")
        self.assertEqual(json_response["body"], "This is a body")

    def test_get_entry(self):
        """
        Ensure we can get an existing entry.
        """
        user = CommonplaceUser.objects.get(pk=1)

        # Seed the database with an entry
        entry = Entry()
        entry.title = "This is a title"
        entry.body = "This is a body"
        entry.created_on = "2006-10-25 14:30:59"
        entry.user = user
        entry.save()
        entry.entry_topics.set([1])
        
        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/entries/{entry.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "This is a title")
        self.assertEqual(json_response["body"], "This is a body")

    def test_change_entry(self):
        """
        Ensure we can change an existing entry.
        """
        user = CommonplaceUser.objects.get(pk=1)

        entry = Entry()
        entry.title = "This is a title"
        entry.body = "This is a body"
        entry.created_on = "2006-10-25 14:30:59"
        entry.user = user
        entry.save()
        entry.entry_topics.set([1])

        # Define new properties for entry
        data = {
            "user": 1,
            "title": "This is a new title",
            "body": "This is a new body",
            "created_on": "2006-10-25 14:30:59",
            "entry_topics": [1]
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/entries/{entry.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get entry again to verify change
        response = self.client.get(f"/entries/{entry.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "This is a new title")
        self.assertEqual(json_response["body"], "This is a new body")

    def test_delete_entry(self):
        """
        Ensure we can delete an existing entry.
        """
        user = CommonplaceUser.objects.get(pk=1)

        entry = Entry()
        entry.title = "This is a title"
        entry.body = "This is a body"
        entry.created_on = "2006-10-25 14:30:59"
        entry.user = user
        entry.save()
        entry.entry_topics.set([1])

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/entries/{entry.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get entry again to verify change
        response = self.client.get(f"/entries/{entry.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)