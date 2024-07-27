from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from courses.models import Material, Section
from exams.models import Exam
from users.models import User


class ExamAPITestCase(TestCase):
    def setUp(self):
        """
        Настройка тестового окружения:
        - Создание двух пользователей.
        - Создание секции и материала, привязанного к секции.
        - Создание экзамена, связанного с материалом.
        """
        # Создание пользователя
        self.user = User.objects.create(email='testuser@example.com', password='testpass123412')
        self.other_user = User.objects.create(email='otheruser@example.com', password='otherpass123412')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создание Section, к которому будет привязан Material
        self.section = Section.objects.create(
            title='Test Section',
            owner=self.user,
            description='Описание раздела'
        )

        # Создание Material
        self.material = Material.objects.create(
            section=self.section,
            owner=self.user,
            title='Test Material',
            content='Содержимое материалов',
            is_public=True
        )
        self.exam = Exam.objects.create(
            title='New Exam 1',
            description='This is a new exam 1',
            material=self.material,
            is_public=True,
            owner=self.user,
        )

    def test_create_exam(self):
        """
        Проверяет создание нового экзамена.
        Ожидается статус 201 Created и увеличение количества экзаменов на 1.
        """
        data = {
            'title': 'New Exam 2',
            'description': 'This is a new exam 2',
            'material': self.material.id,
            'is_public': True
        }
        response = self.client.post('/exams/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exam.objects.count(), 2)

    def test_list_exams(self):
        """
        Проверяет получение списка экзаменов.
        Ожидается статус 200 OK и наличие двух экзаменов в ответе.
        """
        data = {
            'title': 'New Exam 3',
            'description': 'This is a new exam 3',
            'material': self.material.id,
            'is_public': True
        }
        self.client.post('/exams/create/', data)
        response = self.client.get('/exams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_exam(self):
        """
        Проверяет получение конкретного экзамена по его ID.
        Ожидается статус 200 OK и совпадение заголовка экзамена с ожидаемым.
        """
        response = self.client.get(f'/exams/{self.exam.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.exam.title)

    def test_update_exam(self):
        """
        Проверяет обновление существующего экзамена.
        Ожидается статус 200 OK, и заголовок экзамена должен обновиться.
        """
        data = {
            'title': 'Updated Exam',
            'description': 'Updated Description',
            'is_public': False,
            'material': self.exam.material.id,
        }
        response = self.client.put(f'/exams/{self.exam.id}/update/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.exam.refresh_from_db()
        self.assertEqual(self.exam.title, 'Updated Exam')

    def test_delete_exam(self):
        """
        Проверяет удаление экзамена.
        Ожидается статус 204 No Content и уменьшение количества экзаменов на 1.
        """
        response = self.client.delete(f'/exams/{self.exam.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exam.objects.count(), 0)

    def test_create_exam_permission_denied(self):
        """
        Проверяет отказ в создании экзамена для пользователя, не имеющего прав.
        Ожидается статус 403 Forbidden.
        """
        self.client.force_authenticate(user=self.other_user)
        data = {
            'title': 'New Exam by Other User',
            'description': 'Description by Other User',
            'material': self.material.id,
            'is_public': True
        }
        response = self.client.post('/exams/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_exam_permission_denied(self):
        """
        Проверяет отказ в обновлении экзамена для пользователя, не имеющего прав.
        Ожидается статус 403 Forbidden.
        """
        self.client.force_authenticate(user=self.other_user)
        data = {
            'title': 'Updated Exam by Other User',
            'description': 'Updated Description by Other User',
            'is_public': False
        }
        response = self.client.put(f'/exams/{self.exam.id}/update/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_exam_permission_denied(self):
        """
        Проверяет отказ в удалении экзамена для пользователя, не имеющего прав.
        Ожидается статус 403 Forbidden и отсутствие изменений в количестве экзаменов.
        """
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(f'/exams/{self.exam.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Exam.objects.count(), 1)
