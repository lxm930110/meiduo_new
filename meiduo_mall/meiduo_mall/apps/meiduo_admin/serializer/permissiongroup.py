from django.contrib.auth.models import Permission,ContentType,Group

from rest_framework import serializers


class GroupModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Group
        fields = '__all__'



class PermissionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id','name']
        # fields = '__all__'
