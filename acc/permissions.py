from rest_framework import permissions

class ADorReadO(permissions.BasePermission):
    message = "Лише адміністратор може додавати, змінювати та видаляти дані каталогу."
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS :
            return True
        else:
           return bool(request.user and request.user.is_staff) 

