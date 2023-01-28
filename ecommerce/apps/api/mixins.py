from .permissions import IsStaffEditorPermission
from rest_framework import permissions

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


class UserQuerySetMixin():
    user_field = 'user'
    allowed_staff_view = False
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {self.user_field: user}
        # lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        return qs if self.allowed_staff_view and user.is_staff else qs.filter(**lookup_data)
