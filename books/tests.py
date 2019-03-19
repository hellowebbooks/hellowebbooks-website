from django.test import TestCase

# Create your tests here.
class PageTest(TestCase): 
    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_no_logic_page(self):
        r = self.client.get('/about/')
        self.assertEqual(r.status_code, 200)
