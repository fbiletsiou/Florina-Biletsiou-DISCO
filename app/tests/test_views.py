from rest_framework import status
from django.urls import reverse
from django.test import tag


from .test_setup import *

from app.image_hosting.views import ImageAPIView, ImageDetailAPIView, UserList, UserDetail


class TestViews(TestSetUp):

    def test_image_list_view_not_authenticated(self):
        # get API response
        response = self.client.get(reverse('backoffice:image_list_create_view'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_image_list_view_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        # get API response
        response = self.client.get(reverse('backoffice:image_list_create_view'), HTTP_AUTHORIZATION=self.token)

        # get data from db
        all_files = UploadedFile.objects.all()
        serializer = UploadedFileSerializer(all_files, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

"""


    @tag("Tag", "View", "not_authenticated")
    def test_TagsViewSet_post_not_authenticated(self):
        tag3 = {'name': 'Tag3', 'color': 'rgba(255,255,255,0.3)'}
        # get API response
        response = self.client.post(reverse('backoffice:TagsViewSet_list_post'), tag3)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("Tag", "View", "authenticated")
    def test_TagsViewSet_post_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        tag3 = {'name': 'Tag3', 'color': 'rgba(255,255,255,0.3)'}
        # get API response
        response = self.client.post(reverse('backoffice:TagsViewSet_list_post'), tag3, HTTP_AUTHORIZATION=self.token)
        # get data from db
        _tag = Tag.objects.filter(name='Tag3')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'ok')
        self.assertTrue(_tag.exists())

    # The name or color can be an empty string
    @tag("Revisit")
    @tag("Tag", "View", "authenticated")
    def test_TagsViewSet_post_authenticated_fields_missing(self):
        self.client.force_authenticate(user=self.admin_user)
        tag4 = {'name': 'WrongTag', }
        # get API response
        response = self.client.post(reverse('backoffice:TagsViewSet_list_post'), tag4, HTTP_AUTHORIZATION=self.token)
        # get data from db
        _tag = Tag.objects.filter(name='WrongTag')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b'{"error": "body requires \'color\' key with type String"}')
        self.assertTrue(not _tag.exists())

    @tag("Tag", "View", "authenticated")
    def test_TagsViewSet_post_authenticated_already_exists(self):
        self.client.force_authenticate(user=self.admin_user)
        already_existing_tag = self.tag2_attributes
        # get API response
        response = self.client.post(reverse('backoffice:TagsViewSet_list_post'), already_existing_tag,
                                    HTTP_AUTHORIZATION=self.token)
        # get data from db
        _tag = Tag.objects.filter(name='Tag2')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.content.decode(),
                         '{"error": "A tag with that name already exists (tag_id=%s)"}' % (_tag.first().id))
        self.assertTrue(_tag.exists())

    @tag("ClientProfile", "View", "not_authenticated")
    def test_ClientDetailViewSet_update_client_not_authenticated(self):
        # Finding a client id to test
        _client = ClientProfile.objects.all().first()
        _new_client_first_name = 'New Name'
        # get API response
        response = self.client.patch(
            reverse('backoffice:ClientDetailViewSet_retrieve_update_client', args=(_client.id,), ),
            {'first_name': _new_client_first_name})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("Revisit")
    @tag("ClientProfile", "View", "authenticated")
    def test_ClientDetailViewSet_update_client_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        # Finding a client id to test
        _client = ClientProfile.objects.all().first()
        _new_client_first_name = 'New Name'
        # get API response
        response = self.client.patch(
            reverse('backoffice:ClientDetailViewSet_retrieve_update_client', args=(_client.id,), ),
            {'first_name': _new_client_first_name}, HTTP_AUTHORIZATION=self.token)
        # get data from db
        client_profile = ClientProfile.objects.get(id=_client.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'ok')
        self.assertEqual(client_profile.first_name, _new_client_first_name)
    @tag("ClientProfileNote", "View", "not_authenticated")
    def test_ClientProfileNoteViewSet_destroy_not_authenticated(self):
        # Finding a client id to test
        _client = ClientProfile.objects.get(client__email='unit_test2@test.com')
        # new note to be deleted
        _note_to_delete = ClientProfileNote.objects.get(clientprofile=_client)

        # get API response
        response = self.client.delete(reverse('backoffice:ClientProfileNoteViewSet_partial_update_destroy',
                                              args=(_client.id, _note_to_delete.id,), ), )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @tag("ClientProfileNote", "View", "authenticated")
    def test_ClientProfileNoteViewSet_destroy_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        # Finding a client id to test
        _client = ClientProfile.objects.get(client__email='unit_test2@test.com')
        # new note to be deleted
        _note_to_delete = ClientProfileNote.objects.get(clientprofile=_client)

        # get API response
        response = self.client.delete(reverse('backoffice:ClientProfileNoteViewSet_partial_update_destroy',
                                              args=(_client.id, _note_to_delete.id), ), HTTP_AUTHORIZATION=self.token)

        note_exists = ClientProfileNote.objects.filter(note=_note_to_delete.note, clientprofile=_client).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'ok')
        self.assertTrue(not note_exists)

"""
