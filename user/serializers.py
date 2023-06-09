from rest_framework import serializers
from user.models import userModel

class usersSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('id','name','data','img','email','password', 'isLoged', 'firebaseId')

class usersSerializerProfiles(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('id','name','data','img', 'firebaseId')

class contactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = ('contacts',)

