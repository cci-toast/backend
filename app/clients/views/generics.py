from rest_framework.response import Response
from rest_framework import generics, status

from clients.serializers import IDSerializer, ClientIDSerializer


class ModelView(generics.GenericAPIView):
    model_class = None

    def get_queryset(self):
        queryset = self.queryset.all()
        for field in self.model_class._meta.get_fields():
            field_val = self.request.data.get(field.name, None)
            if field_val is not None:
                queryset = queryset.filter(**{field.name: field_val})

        return queryset


    def get_object(self):
        id_serializer = IDSerializer(queryset=self.get_queryset(), data=self.request.data)
        id_serializer.is_valid(raise_exception=True)
        object_id = id_serializer.data['id']
        return self.get_queryset().get(id=object_id)


    def get(self, request):
        serializer_class = self.get_serializer_class()
        object_id = request.data.get('id', None)
        if object_id is None:
            # get list of advisors if no id provided
            data = self.get_queryset()
            serializer = serializer_class(data, many=True, context={'request': request})
        else:
            # retrieve info of a model
            model_object = self.get_object()
            serializer = serializer_class(model_object)

        return Response(serializer.data)


    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def patch(self, request):
        serializer_class = self.get_serializer_class()
        model_object = self.get_object()
        serializer = serializer_class(model_object,
                                      data=request.data,
                                      partial=True,
                                      context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


    def delete(self, request):
        serializer_class = self.get_serializer_class()
        advisor = self.get_object()
        advisor.delete()
        serializer = serializer_class(advisor)
        return Response(serializer.data)



class ClientDependModelView(generics.GenericAPIView):
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
            # get list of objects of a client if no id provided
            data = self.get_queryset()
            serializer = response_serializer_class(data,
                                                   many=True,
                                                   context={'request': request})
        else:
            # get the detail of a object with the id
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
