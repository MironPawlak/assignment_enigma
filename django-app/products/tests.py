import io
import shutil
import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Category, Product

MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ProductsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        im = Image.new('RGBA', size=(500, 500), color=(256, 0, 0))
        img_bytes = io.BytesIO()
        im.save(img_bytes, format='png')
        cls.image = ImageFile(io.BytesIO(img_bytes.getvalue()), name='test.png')
        user = get_user_model().objects.create_user(username='admin', password='admin', email='admin@admin.pl')
        user.is_superuser = True
        user.save()
        category = Category(name='Test')
        category.save()
        cls.category = category
        cls.product_data = {'description': 'Test', 'price': 10, 'category': cls.category,
                            'image': cls.image}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client.login(username='admin', password='admin')

    def test_product_create(self):
        data = {**self.product_data, 'name': 'Test', 'category': 1}
        response = self.client.post(reverse('products:product-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_product_get(self):
        product = Product(**self.product_data, name='Test')
        product.save()
        response = self.client.get(reverse('products:product-list'))
        self.assertContains(response, product.name)

    def test_product_patch(self):
        product = Product(**self.product_data, name='Test')
        product.save()
        response = self.client.patch(reverse('products:product-detail', kwargs={'pk': product.id}),
                                     {'name': 'New Test'}, content_type='application/json')
        self.assertEqual(Product.objects.all().first().name, 'New Test')

    def test_order(self):
        product = Product(**self.product_data, name='Test')
        product.save()
        product2 = Product(**self.product_data, name='Test2')
        product2.save()
        data = {'username': 'admin', 'delivery_address': 'Testowa 7',
                'product_list': [{'quantity': 2, 'product': product.id}, {'quantity': 2, 'product': product2.id}]}
        response = self.client.post(reverse('products:order'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
