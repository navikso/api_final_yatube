# from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
# from rest_framework.response import Response

from posts.models import Group, Post, Follow
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          GroupSerializer,
                          PostSerializer,
                          FollowSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    # def get(self, request):
    #     queryset = self.get_queryset()
    #     serializer = PostSerializer(queryset, many=True)
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = PostSerializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #     return Response({'posts': serializer.data})

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(
                'Изменение поста другого автора недоступно.'
            )
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление поста другого автора недоступно.'
            )
        super(PostViewSet, self).perform_destroy(instance)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Доступно только автору комментария')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Удаление комментария другого автора недоступно.'
            )
        super(CommentViewSet, self).perform_destroy(instance)


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(
            user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class FollowViewSet(viewsets.ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializer
#     permission_classes = (IsAuthenticated, )

#     def get_queryset(self):
#         return self.request.user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
