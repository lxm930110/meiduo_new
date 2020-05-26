from django.contrib.auth.models import Group

from rest_framework import serializers

from users.models import User


class UserModelSerializer(serializers.ModelSerializer):


    class Meta:

        model = User
        fields = ['id','username','mobile','email','password']

        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        # 添加两个字段
        validated_data['is_superuser'] = True
        validated_data['is_staff'] = True
        user = super().create(validated_data)
        password = user.password
        # 给新增用户密码加密
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # 添加两个字段
        user = super().update(instance,validated_data)
        password = user.password
        # 给新增用户密码加密
        user.set_password(password)
        user.save()
        return user


class GroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id','name']

