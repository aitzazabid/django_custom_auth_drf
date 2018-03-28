# write the serializer here
from rest_framework import serializers

from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    @staticmethod
    def get_email(obj):
        user = obj.user.email
        return user

    class Meta:
        model = UserProfile
        fields = ('id',
                  'display_name',
                  'phone_number',
                  'email',

                  )
