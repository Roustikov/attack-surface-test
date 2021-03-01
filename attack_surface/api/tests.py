from django.test import SimpleTestCase
from api.models import VM
'''
Simple test cases. Since neo4j is coupled to Django very loosely -
we must rely on a separate DB instance running in docker container.
The instance must be available at TEST_URL and be initialized by
python manage.py install_labels
'''
TEST_URL = 'http://127.0.0.1/api/v1'


class TestViews(SimpleTestCase):
    def test_attack(self):
        response = self.client.get(f'{TEST_URL}/attack')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')

    def test_attack_with_id(self):
        vm = VM.nodes.first()
        vm_id = vm.vm_id
        response = self.client.get(f'{TEST_URL}/attack?vm_id={vm_id}')
        self.assertEqual(response.status_code, 200)

    def test_attack_with_unreal_id(self):
        response = self.client.get(f'{TEST_URL}/attack?vm_id=xyz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'[]')

    def test_stats(self):
        response = self.client.get(f'{TEST_URL}/stats')
        self.assertEqual(response.status_code, 200)
