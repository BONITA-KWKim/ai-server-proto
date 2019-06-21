from rest_framework.permissions import AllowAny


def get_permissions(self):
    if self.action == 'list':
        permission_classes = [AllowAny, ]
    else:
        permission_classes = [AllowAny, ]
    return [permission() for permission in permission_classes]
