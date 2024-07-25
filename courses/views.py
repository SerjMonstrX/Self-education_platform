from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from exams.models import Exam
from .models import Section, Material
from .serializers import SectionSerializer, MaterialSerializer
from django.db.models import Q
from courses.permissions import IsModerator, IsModeratorReadOnly, IsOwner


class SectionCreateAPIView(generics.CreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SectionListAPIView(generics.ListAPIView):
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Возвращаем разделы пользователя или публичные разделы
            return Section.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            # Возвращаем только публичные разделы для неаутентифицированных пользователей
            return Section.objects.filter(is_public=True)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class SectionUpdateAPIView(generics.UpdateAPIView):
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
            # Если пользователь не владелец урока и не модератор, не допускать редактирование
            raise PermissionDenied("У вас нет разрешения редактировать этот раздел.")


class SectionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class MaterialCreateAPIView(generics.CreateAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        section = serializer.validated_data['section']
        if section.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого раздела.")
        serializer.save(owner=self.request.user)


class MaterialListAPIView(generics.ListAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Возвращаем материалы пользователя или публичные материалы
            return Material.objects.filter(Q(owner=user) | Q(is_public=True))
        else:
            # Возвращаем только публичные материалы для неаутентифицированных пользователей
            return Material.objects.filter(is_public=True)


class MaterialRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]


class MaterialUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]

    def perform_update(self, serializer):
        user = self.request.user
        exam_id = self.kwargs['pk']
        exam = Exam.objects.get(pk=exam_id)
        material = exam.smaterial

        # Проверка, что пользователь является владельцем материала и раздела, или модератором
        if (exam.owner == user and material.owner == user) or user.groups.filter(name='Moderators').exists():
            serializer.save()
        else:
            raise PermissionDenied("У вас нет разрешения редактировать этот материал.")


class MaterialDestroyAPIView(generics.DestroyAPIView):
    serializer_class = MaterialSerializer
    queryset = Material.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwner | IsModerator]
