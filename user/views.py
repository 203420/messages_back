from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json 

from user.models import userModel
from user.serializers import usersSerializerAll, usersSerializerProfiles, contactsSerializer

# Create your views here.
class UsersView(APIView):
    def post(self, request, format=None):
        serializer = usersSerializerAll(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'id': serializer.data['id'],
                'img': serializer.data['img'],
                'name': serializer.data['name'],
                'data': serializer.data['data'],
                'state': serializer.data['isLoged'],
                'firebaseId': serializer.data['firebaseId'],
            }
            return Response(data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, email):
        try:
            return userModel.objects.get(email=email)
        except userModel.DoesNotExist:
            return None

    def get(self, request, format=None):
        email = request.data.get('email', None)
        if email:
            instance = self.get_object(email)
            if instance:
                return Response(True, status=status.HTTP_200_OK)
        return Response(False, status=status.HTTP_200_OK)
    
    def delete(self, request, format=None):
        try:
            userModel.objects.all().delete()
            return Response("Usuarios eliminados", status=status.HTTP_200_OK)
        except:
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)


class SingleUserView(APIView):
    def get_object(self, pk):
        try:
            return userModel.objects.get(pk = pk)
        except userModel.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        id_response = self.get_object(pk)
        if id_response != 0:
            id_response = usersSerializerProfiles(id_response)
            return Response(id_response.data, status=status.HTTP_200_OK)
        return Response("No hay datos", status=status.HTTP_400_BAD_REQUEST)
    
    
class ContactsView(APIView):
    def get_object(self, pk):
        try:
            return userModel.objects.get(pk=pk)
        except userModel.DoesNotExist:
            return 0

    def post(self, request, pk, format=None):
        email = request.data.get('email', None)
        user = self.get_object(pk)
        if user != 0:
            current_contacts = user.contacts
            new_contact = email
            
            # Agrega el nuevo correo electrónico solo si no está presente en la lista actual
            if new_contact and new_contact not in current_contacts:
                new_contacts = current_contacts + new_contact + ","
                user.contacts = new_contacts
                user.save()
            
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ContactsViewList(APIView):
    def get_object(self, pk):
        try:
            return userModel.objects.get(pk = pk)
        except userModel.DoesNotExist:
            return 0

    def get(self, request, pk, format=None):
        id_response = self.get_object(pk)
        if id_response != 0:
            id_response = contactsSerializer(id_response)
            data = str(id_response.data['contacts']).split(",")[:-1]

            instances = userModel.objects.filter(email__in=data)
            if instances:
                serializer = usersSerializerProfiles(instances, many=True)
                response = {
                    'contacts': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response("No hay datos", status=status.HTTP_400_BAD_REQUEST)