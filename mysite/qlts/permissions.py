from rest_framework.permissions import BasePermission, SAFE_METHODS
class Kiem_Tra_Phan_Quyen_User(BasePermission):
    """
    - Admin (is_staff=True): được quyền GET, POST, PUT, DELETE
    - User thường (is_staff=False): chỉ được GET
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_staff
