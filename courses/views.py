from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from exams.models import Exam
from .models import Section, Material
from .serializers import SectionSerializer, MaterialSerializer
from django.db.models import Q
from courses.permissions import IsModerator, IsModeratorReadOnly, IsOwner


class SectionCreateAPIView(generics.CreateAPIView):
    """
    API-представление для создания нового раздела.
    Позволяет аутентифицированным пользователям создавать разделы.
    """
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SectionListAPIView(generics.ListAPIView):
    """
    API-представление для получения списка разделов.
    Возвращает разделы, принадлежащие аутентифицированному пользователю, или публичные разделы.
    """
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Section.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            return Section.objects.filter(is_public=True)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    """
    API-представление для получения информации о конкретном разделе.
    Доступно только владельцу или модераторам.
    """
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class SectionUpdateAPIView(generics.UpdateAPIView):
    """
    API-представление для обновления информации о разделе.
    Обновление доступно только владельцу или модераторам.
    """
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        section_id = self.kwargs['pk']
        section = Section.objects.get(pk=section_id)
        if section.owner == user or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class SectionDestroyAPIView(generics.DestroyAPIView):
    """
    API-представление для удаления раздела.
    Удаление доступно только владельцу или модераторам.
    """
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class MaterialCreateAPIView(generics.CreateAPIView):
    """
    API-представление для создания нового материала.
    Позволяет аутентифицированным пользователям создавать материалы в их разделах.
    """
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        section = serializer.validated_data['section']
        if section.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого раздела.")
        serializer.save(owner=self.request.user)


class MaterialListAPIView(generics.ListAPIView):
    """
    API-представление для получения списка материалов.
    Возвращает материалы, принадлежащие аутентифицированному пользователю, или публичные материалы.
    """
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Material.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            return Material.objects.filter(is_public=True)


class MaterialRetrieveAPIView(generics.RetrieveAPIView):
    """
    API-представление для получения информации о конкретном материале.
    Доступно только владельцу или модераторам.
    """
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class MaterialUpdateAPIView(generics.UpdateAPIView):
    """
    API-представление для обновления информации о материале.
    Обновление доступно только владельцу или модераторам.
    """
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        section = serializer.validated_data['section']
        if section.owner != user or user.groups.filter(name='Moderators').exists():
            raise PermissionDenied("У вас нет разрешения редактировать этот материал.")
        serializer.save(owner=self.request.user)


class MaterialDestroyAPIView(generics.DestroyAPIView):
    """
    API-представление для удаления материала.
    Удаление доступно только владельцу или модераторам.
    """
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]
