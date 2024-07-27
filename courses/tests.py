from rest_framework.test import APITestCase
from rest_framework import status
from courses.models import Section, Material
from users.models import User


class SectionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass123412')
        self.other_user = User.objects.create(email='otheruser@example.com', password='otherpass123412')
        self.client.force_authenticate(user=self.user)
        self.section = Section.objects.create(
            title='Test Section',
            owner=self.user,
            description='This is a test section',
            is_public=False
        )

    def test_create_section(self):
        data = {
            'title': 'New Section',
            'description': 'This is a test section',
            'is_public': True
        }
        response = self.client.post('/courses/sections/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 2)
        self.assertEqual(Section.objects.latest('id').title, 'New Section')

    def test_list_sections(self):
        Section.objects.create(title='Section 1', owner=self.user, description='Section 1 Description', is_public=True)
        response = self.client.get('/courses/sections/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_section(self):
        response = self.client.get(f'/courses/sections/{self.section.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.section.title)

    def test_update_section(self):
        data = {
            'title': 'Updated Section',
            'description': 'Updated Description',
            'is_public': True
        }
        response = self.client.put(f'/courses/sections/{self.section.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.section.refresh_from_db()
        self.assertEqual(self.section.title, 'Updated Section')

    def test_delete_section(self):
        response = self.client.delete(f'/courses/sections/{self.section.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Section.objects.count(), 0)

    def test_update_section_permission_denied(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            'title': 'Updated Section by Other User',
            'description': 'Updated Description',
            'is_public': True
        }
        response = self.client.put(f'/courses/sections/{self.section.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_section_permission_denied(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/courses/sections/{self.section.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Section.objects.count(), 1)  # Количество разделов не изменяется


class MaterialTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass123412')
        self.other_user = User.objects.create(email='otheruser@example.com', password='otherpass123412')
        self.client.force_authenticate(user=self.user)
        self.section = Section.objects.create(
            title='Test Section',
            owner=self.user,
            description='This is a test section',
            is_public=False
        )
        self.material = Material.objects.create(
            section=self.section,
            owner=self.user,
            title='Test Material',
            content='This is test content',
            is_public=False
        )

    def test_create_material(self):
        data = {
            'section': self.section.id,
            'title': 'New Material',
            'content': 'This is new content',
            'is_public': True
        }
        response = self.client.post('/courses/materials/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Material.objects.count(), 2)
        self.assertEqual(Material.objects.latest('id').title, 'New Material')

    def test_list_materials(self):
        Material.objects.create(section=self.section, owner=self.user, title='Material 1', content='Content 1', is_public=True)
        response = self.client.get('/courses/materials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_material(self):
        response = self.client.get(f'/courses/materials/{self.material.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.material.title)

    def test_update_material(self):
        data = {
            'title': 'Updated Material',
            'content': 'Updated Content',
            'is_public': True,
            'section': self.material.section.id  # Добавляем ID связанного раздела
        }
        response = self.client.put(f'/courses/materials/{self.material.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material.refresh_from_db()
        self.assertEqual(self.material.title, 'Updated Material')

    def test_delete_material(self):
        response = self.client.delete(f'/courses/materials/{self.material.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Material.objects.count(), 0)

    def test_update_material_permission_denied(self):
        self.client.force_authenticate(user=self.other_user)
        data = {
            'title': 'Updated Material by Other User',
            'content': 'Updated Content',
            'is_public': True
        }
        response = self.client.put(f'/courses/materials/{self.material.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_material_permission_denied(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/courses/materials/{self.material.id}/delete/')
        print(response.data)  # Выводим данные ответа для анализа
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Material.objects.count(), 1)  # Количество материалов не изменяется
