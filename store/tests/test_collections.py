from rest_framework import status
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from model_bakery import baker
from store.models import Collection, Product

User = settings.AUTH_USER_MODEL


class TestCreateCollection(TestCase):

    def create_collection(self, data):
        url = reverse('collection-list')
        return self.client.post(url, data, content_type='application/json')

    def authenticate(self, is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        self.client.force_login(user)

    def test_if_user_is_anonymous_returns_401(self):
        data = {'name': 'a'}

        response = self.create_collection(data)

        # This must be HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_is_not_admin_returns_403(self):
        data = {'name': 'a'}
        self.authenticate()

        response = self.create_collection(data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        data = {}
        self.authenticate(is_staff=True)

        response = self.create_collection(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_returns_201(self):
        data = {'name': 'a'}
        self.authenticate(is_staff=True)

        response = self.create_collection(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(response.data['id'], 0)


class TestRetrieveCollection(TestCase):

    def get_collection(self, collection_id):
        url = reverse('collection-detail', kwargs={'pk': collection_id})
        return self.client.get(url)

    def test_if_collection_does_not_exists_returns_404(self):
        response = self.get_collection(0)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_if_collection_exists_returns_200(self):
        collection = baker.make(Collection)

        response = self.get_collection(collection.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], collection.id)


class TestDeleteCollection(TestCase):

    def delete_collection(self, collection_id):
        url = reverse('collection-detail', kwargs={'pk': collection_id})
        return self.client.delete(url)

    def authenticate(self, is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        self.client.force_login(user)

    def test_if_user_is_anonymous_returns_401(self):
        collection = baker.make(Collection)

        response = self.delete_collection(collection.id)

        # This must be HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_is_not_admin_returns_403(self):
        collection = baker.make(Collection)
        self.authenticate()

        response = self.delete_collection(collection.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_cannot_be_deleted_returns_405(self):
        product = baker.make(Product)
        self.authenticate(is_staff=True)

        response = self.delete_collection(product.collection.id)

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.data['detail'], 'Collection cannot be deleted, because it includes one or more products.')

    def test_if_collection_deleted_returns_204(self):
        collection = baker.make(Collection)
        self.authenticate(is_staff=True)

        response = self.delete_collection(collection.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestPatchCollection(TestCase):

    def patch_collection(self, collection_id, data):
        url = reverse('collection-detail', kwargs={'pk': collection_id})
        return self.client.patch(url, data, content_type='application/json')

    def authenticate(self, is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        self.client.force_login(user)

    def test_if_user_is_anonymous_returns_401(self):
        collection = baker.make(Collection)
        data = {'name': 'a'}

        response = self.patch_collection(collection.id, data)

        # This must be HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_is_not_admin_returns_403(self):
        collection = baker.make(Collection)
        self.authenticate()
        data = {'name': 'a'}

        response = self.patch_collection(collection.id, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        collection = baker.make(Collection)
        self.authenticate(is_staff=True)
        data = {'name': ''}

        response = self.patch_collection(collection.id, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_returns_200(self):
        collection = baker.make(Collection)
        self.authenticate(is_staff=True)
        data = {'name': 'a'}

        response = self.patch_collection(collection.id, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])


class TestPutCollection(TestCase):

    def put_collection(self, collection_id, data):
        url = reverse('collection-detail', kwargs={'pk': collection_id})
        return self.client.put(url, data, content_type='application/json')

    def authenticate(self, is_staff=False):
        user = baker.make(User, is_staff=is_staff)
        self.client.force_login(user)

    def test_if_user_is_anonymous_returns_401(self):
        collection = baker.make(Collection)
        data = {'name': 'a'}

        response = self.put_collection(collection.id, data)

        # This must be HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_user_is_not_admin_returns_403(self):
        collection = baker.make(Collection)
        self.authenticate()
        data = {'name': 'a'}

        response = self.put_collection(collection.id, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self):
        collection = baker.make(Collection)
        self.authenticate(is_staff=True)
        data = {'name': ''}

        response = self.put_collection(collection.id, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_data_is_valid_returns_200(self):
        collection = baker.make(Collection)
        self.authenticate(is_staff=True)
        data = {'name': 'a'}

        response = self.put_collection(collection.id, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
