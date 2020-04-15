from rest_framework.response import Response
from rest_framework import generics, status

from clients.serializers import IDSerializer, ClientIDSerializer


class ClientDependView(generics.GenericAPIView):
    def get_queryset(self):
        client_id_serializer = ClientIDSerializer(data=self.request.data)
        client_id_serializer.is_valid(raise_exception=True)
        client_id = client_id_serializer.validated_data['client']
        return self.queryset.filter(client=client_id)


    def get_object(self):
        id_serializer = IDSerializer(queryset=self.get_queryset(), data=self.request.data)
        id_serializer.is_valid(raise_exception=True)
        object_id = id_serializer.data['id']
        return self.get_queryset().get(id=object_id)


    def get(self, request):
        object_id = request.data.get("id", None)
        serializer_class = self.get_serializer_class()
        response_serializer_class = serializer_class.response_serializer
        if object_id is None:
            # get list of partners of a client if no id provided
            data = self.get_queryset()
            serializer = response_serializer_class(data,
                                                   many=True,
                                                   context={'request': request})
            return Response(serializer.data)
        else:
            # get the detail of a partner with the id
            client_object = self.get_object()
            serializer = response_serializer_class(client_object)
            return Response(serializer.data)


    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # not include client attribute in json
        response_serializer_class = serializer_class.response_serializer
        response_serializer = response_serializer_class(serializer.instance)

        return Response(response_serializer.data)


    def patch(self, request):
        client_object = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(client_object,
                                      data=request.data,
                                      partial=True,
                                      context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # not include client attribute in json
        response_serializer_class = serializer_class.response_serializer
        response_serializer = response_serializer_class(serializer.instance)

        return Response(response_serializer.data)


    def delete(self, request):
        client_object = self.get_object()
        client_object.delete()

        # not include client attribute in json
        serializer_class = self.get_serializer_class()
        response_serializer_class = serializer_class.response_serializer
        response_serializer = response_serializer_class(client_object)

        return Response(response_serializer.data)
