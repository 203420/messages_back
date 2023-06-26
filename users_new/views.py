from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json 

from users_new.models import userModel
from users_new.serializers import usersSerializerAll, usersSerializerProfiles, contactsSerializer

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
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        if user  != 0:
            serializer = usersSerializerProfiles(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
            new_contact = userModel.objects.get(email=email)

            if new_contact is not None:
                current_contacts = user.contacts.all()

                if new_contact not in current_contacts:
                    user.contacts.add(new_contact)
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
            contacts = id_response.contacts.all()
            serializer = usersSerializerProfiles(contacts, many=True)
        
            response = {
                'contacts': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response("No hay datos", status=status.HTTP_400_BAD_REQUEST)

class UsersFirebaseView(APIView):
    # def get_object(self, firebaseId):
    #     try:
    #         return userModel.objects.get(firebaseId = firebaseId)
    #     except userModel.DoesNotExist:
    #         return 0

    # def get(self, request, pk, format=None):
    #     id_response = self.get_object(pk)
    #     if id_response != 0:
    #         id_response = usersSerializerProfiles(id_response)
    #         return Response(id_response.data, status=status.HTTP_200_OK)
    #     return Response("No hay datos", status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, firebaseId):
        try:
            return userModel.objects.get(firebaseId=firebaseId)
        except userModel.DoesNotExist:
            return None

    def get(self, request, format=None):
        fid = request.data.get('firebaseId', None)
        print(fid)
        if fid:
            instance = self.get_object(fid)
            instance = usersSerializerProfiles(instance)
            if instance:
                return Response(instance.data, status=status.HTTP_200_OK)
        return Response("No hay datos", status=status.HTTP_200_OK)