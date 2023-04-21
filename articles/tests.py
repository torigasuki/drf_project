from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from faker import Faker
from articles.serializers import ArticleSerializer
from articles.models import Article

from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200,200)
    color = (255,0,0,0)
    image = Image.new('RGBA', size=size, color=color)
    image.save(temp_file, 'png')
    return temp_file



class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email': 'john', 'password': 'johnpassword'}
        cls.article_data = {'title':'title','content':'content'}
        cls.user = User.objects.create_user('john','johnpassword')

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # def setUp(self):
    #     self.user_data = {'email': 'john', 'password': 'johnpassword'}
    #     self.article_data = {'title':'title','content':'content'}
    #     self.user = User.objects.create_user('john','johnpassword')
    #     self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    def test_fail_if_not_logged_in(self):
        url = reverse('article_view')
        response= self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article(self):
        response = self.client.post(
            path=reverse('article_view'),
            data=self.article_data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_create_article_with_image(self):

        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = 'test.png'
        temp_file = get_temporary_image(temp_file)
        temp_file.seek(0)
        self.article_data['image'] = temp_file

        response = self.client.post(
            path=reverse('article_view'),
            data = encode_multipart(data = self.article_data, boundary = BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.user = User.objects.create_user(cls.faker.email(),cls.faker.password())
            cls.articles.append(Article.objects.create(title=cls.faker.sentence(),content=cls.faker.text(),user=cls.user))

    def test_get_articles(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer_data = ArticleSerializer(article).data
            for key, value in serializer_data.items():
                self.assertEqual(response.data[key], value)
                print(key,value)
            self.assertEqual(article.title, response.data['title'])
