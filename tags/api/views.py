from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from tags.models import Tag
from tags.api.serializers import TagSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.select_related('user').all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
