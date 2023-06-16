from rest_framework import serializers
from users_new.models import userModel

class usersSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('id','name','data','img','email','password', 'isLoged', 'firebaseId')

class usersSerializerProfiles(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('id','name','data','img', 'firebaseId', 'isLoged')

class contactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('contacts',)

