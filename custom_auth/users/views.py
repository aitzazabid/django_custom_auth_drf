# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from users.models import UserProfile,User,Post

from rest_framework import viewsets,status
from users.serializers import UserSerializer,PostSerializer
from rest_framework.response import Response
from users.validations import Validation


class UserList(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        List all USERS
        ---
        """
        return super(UserList, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        email = request.data['email'] if 'email' in request.data else None
        password = request.data['password'] if 'password' in request.data else None
        display_name = request.data['display_name'] if 'display_name' in request.data else None
        phone_number = request.data['phone_number'] if 'phone_number' in request.data else None
        if email is None or password is None or display_name is None or phone_number is None :
            return Response({'message': 'keys missing'})

        elif len(email)==0 or len(password)==0 or len(display_name)==0  or len(phone_number)==0 :
                return Response({'message': 'keys value missing'})

        if Validation.validate_email(email):
            return Response({
                'message': 'Enter the email in valid format'
            })
        if not Validation.validate_password(password):
            return Response({
                'message': 'Password must be 8 character and must have 1 number and 1 upercase letter'
            })
        if not Validation.email_exists(email):
            user = User.objects.create(email=email)
            user.set_password(password)
            user_profile = UserProfile.objects.create(user=user,display_name=display_name,phone_number=phone_number)
            dataCustomer = UserSerializer(user_profile, many=False,
                                          context={"request": request,}).data

            return Response(dataCustomer, status=status.HTTP_200_OK)
        return Response({'message': 'email already exists'},status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a particular USERS

        """
        return super(UserList, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a particular USERS

        """
        return super(UserList, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Partial Update a particular USERS

        """
        return super(UserList, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a particular USERS

        """
        return super(UserList, self).destroy(request, *args, **kwargs)


class Posts(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        """
        List all POSTS
        ---
        """
        return super(Posts, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.data['user']
        post = request.data['post']
        post = Post.objects.create(user_id=user, posts=post)
        return Response({
            'user':user,
            'post': post.posts,
            'id': post.id
        })
        # return super(Posts, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a particular POSTS

        """
        return super(Posts, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a particular POSTS

        """
        print("in the update")
        user = request.data['user']
        post_id = request.data['post_id']
        post_message = request.data['post']

        try:
            post = Post.objects.get(user_id=user, id=post_id)
            post.posts = post_message
            post.save()
            return Response({
                'user': user,
                'post': post.posts,
                'id': post.id
            })
        except Post.DoesNotExist:
            return Response({
                'message':'You can not edit other posts'
            })


    def destroy(self, request, *args, **kwargs):
        """
        Delete a particular POSTS

        """
        user = request.data['user']
        post_id = request.data['post_id']
        try:
            Post.objects.filter(user_id=user, id=post_id).delete()
            return Response({
                'user': user,
                'id': post_id,
                'message':"deleted permanently"
            })
        except Post.DoesNotExist:
            return Response({
                'message':'You can not delete other posts'
            })


