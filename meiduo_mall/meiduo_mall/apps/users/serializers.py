from rest_framework import serializers

from users.models import User


class UserInfoSerializer(serializers.Serializer):

    username = serializers.CharField(required=True,max_length=20)
    mobile = serializers.CharField(required=True,min_length=11)
    email = serializers.CharField(required=False)
    email_active = serializers.CharField(required=False)
    # password = serializers.CharField(required=True)
    # pwd = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        pwd = attrs.get('pwd')
        if pwd != password:
            raise serializers.ValidationError('密码不一致')
        else:
            return attrs


class UserInfoModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
