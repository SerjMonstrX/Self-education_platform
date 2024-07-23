from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderators').exists()


class IsModeratorReadOnly(BasePermission):
    """
    Правило доступа, позволяющее модераторам только просматривать и редактировать объекты,
    но не создавать и не удалять их.
    """
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь модератором
        return request.user.groups.filter(name='Moderators').exists()

    def has_object_permission(self, request, view, obj):
        # Проверяем, что для объекта разрешено только чтение и редактирование
        return request.user.groups.filter(name='Moderators').exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return request.method in ['GET', 'PUT', 'PATCH', 'DELETE']
        return False
