from rest_framework.serializers import ModelSerializer,BaseSerializer

from users.models import User


class UserModelSerializer(ModelSerializer):
    '''
    user序列化器
    '''
    class Meta:

        model = User
        fields = ['id','username','email','mobile','password']

        extra_kwargs = {
            'username':{'max_length':20,'min_length':5},
            'password': {'max_length': 20, 'min_length': 8,'write_only':True},
        }
    #　重写create方法
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        return user