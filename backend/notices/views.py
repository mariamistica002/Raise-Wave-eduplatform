from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Notice
from .serializers import NoticeSerializer


class NoticeListCreateView(generics.ListCreateAPIView):
    serializer_class = NoticeSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['institution', 'priority', 'target_audience', 'is_published']
    search_fields    = ['title', 'content']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Notice.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(published_by=self.request.user)


class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]
