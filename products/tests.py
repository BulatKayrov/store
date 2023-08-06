from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self.assertEquals(response.context['title'], 'Store')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')
