from rest_framework import permissions


class IsReadAllCreateAdmin(permissions.BasePermission):
    """
    create category if user in group or user is_superuser
    read all users
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (
                request.method == 'POST'
                and (request.user.groups.filter(name='group_create_read_category').exists()
                     or request.user.is_superuser)
        ):
            return True


class IsRetrieveDestroyUpdateDefinedUsers(permissions.BasePermission):
    """
    Update, Delete category only if user there are in the group
    """

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='retrieve_update_delete_category').exists():
            return True
