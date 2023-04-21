from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


# class UserRegisterAPIViewTestCase(APITestCase):
#     def test_registration(self):
#         url = reverse('user_view')
#         user_data={
#             'username': 'testuser',
#             'fullname': 'testuser',
#             'email': 'test@test.com',
#             'password': 'testpassword',
#         }
#         response = self.client.post(url, user_data)
#         self.assertEqual(response.status_code, 201)

#     def test_login(self):
#         url = reverse('token_obtain_pair')
#         user_data={
#             'username': 'testuser',
#             'fullname': 'testuser',
#             'email': 'test@test.com',
#             'password': 'testpassword',
#         }
#         response = self.client.post(url, user_data)
#         print(response.data)
#         self.assertEqual(response.status_code, 200)



class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email': 'john', 'password': 'johnpassword'}
        self.user = User.objects.create_user('john','johnpassword')

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        user = User.get_absolute_url(user_id=self.user.id)
        access_teken = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(
            path=user,
            HTTP_AUTHORIZATION=f'Bearer {access_teken}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.data['email'])