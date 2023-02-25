import datetime
import pytz
import operator
from functools import reduce

from django.shortcuts import redirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


from .models import UploadedFile, User, TempUrl, randomString
from .serializers import UserSerializer, validate_image_format, FileBasicSerializer, FilePremiumSerializer, FileEnterpriseSerializer, TempUrlSerializer



def get_serializer_for_tier(tier):
    if tier == 'Enterprise':
        return FileEnterpriseSerializer
    elif tier == 'Premium':
        return FilePremiumSerializer
    else:
        return FileBasicSerializer


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        q = reduce(operator.or_, (Q(x) for x in filter.items()))
        return get_object_or_404(queryset, q)


class UploadedFileViewset(viewsets.ViewSet):
    queryset = UploadedFile.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        """
        Method that lists all uploaded files for the authenticated user
        """
        images = self.queryset.filter(created_by__id=request.user.id)
        serializer = get_serializer_for_tier(request.user.tier)(images, context={"request": request}, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk):
        """
        Retrieve the Uploaded image with given id (pk) for authenticated user.
        """
        image_instance = get_object_or_404(self.queryset, pk=pk, created_by__id=request.user.id)
        serializer = get_serializer_for_tier(request.user.tier)(image_instance, context={"request": request})

        try:
            print(serializer.data)
        except Exception as e:
            print(e)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Method that creates a new uploaded file with the given data
        :param request: new file located at request.data
        """
        new_file = request.data.get('new_file')

        # validating the file format
        try:
            file_format = validate_image_format(new_file.content_type)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        new_data = {
            "name": new_file.name,
            "file_format": file_format,
            "image_url": new_file,
            'created_by': request.user.pk
        }

        serializer = get_serializer_for_tier(request.user.tier)(data=new_data, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        """
        Updates the Upload Image object with given id (pk) if exists for authenticated user.
        """
        image_instance = get_object_or_404(self.queryset, pk=pk, created_by__id=request.user.id)

        updated_file = request.data.get('new_file')
        try:
            file_format = validate_image_format(updated_file.content_type)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        updated_data = {
            "name": updated_file.name,
            "file_format": file_format,
            "image_url": updated_file
        }

        serializer = get_serializer_for_tier(request.user.tier)(instance=image_instance, data=updated_data, partial=True, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Deletes the Uploaded image object with given id (pk) if exists for authenticated user
        """
        image_instance = get_object_or_404(self.queryset, pk=pk, created_by__id=request.user.id)
        image_instance.delete()

        return Response({"result": "Image deleted"}, status=status.HTTP_200_OK)


class TempUrlViewset(MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """
    Generic View for creating and using Temporary Urls for Enterprise Users.
    """
    queryset = TempUrl.objects.all()
    permission_classes = [IsAuthenticated, ]
    lookup_fields = ('file_id', 'token')
    min_duration = 300
    max_duration = 30000

    @action(detail=True, methods=['get'], name='Expiry Link',  url_path='generate', url_name='generate_link')
    def generate_link(self, request, file_id):
        """
        Method that creates a temporary url for an uploaded file for Enterprise Users
        Expects a query parameter for the number of seconds until expiration (between 300 and 30000).
        If not given, the default is the minimum option
        """

        if request.user.tier != 'Enterprise':
            return Response({"error": "Given account tier does not support this feature"},
                            status=status.HTTP_403_FORBIDDEN)
        original_file = get_object_or_404(UploadedFile, pk=file_id)

        link_time = int(self.request.query_params.get('time', 300))
        if link_time < self.min_duration or link_time > self.max_duration:
            return Response({"error": f"Time requested: {link_time}. Allowed range: {self.min_duration}-{self.max_duration}"},
                            status=status.HTTP_400_BAD_REQUEST)

        req = {
            'token': randomString(stringLength=20),
            'expiry_date': datetime.datetime.now() + datetime.timedelta(seconds=link_time)
        }
        serializer = TempUrlSerializer(data=req, context={"request": request})

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, related_file=original_file)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], lookup_field='token', name='Use Expiry Link', url_name='use')
    def use(self, request, token):
        """
        Method that handles a temporary url for an uploaded file for Enterprise Users
        If the link is still active, it redirects to the file information
        """
        if request.user.tier != 'Enterprise':
            return Response({"error": "Given account tier does not support this feature"},
                            status=status.HTTP_403_FORBIDDEN)

        # check if this is an existing temporary url
        temp_url = get_object_or_404(self.queryset, token=token)

        if datetime.datetime.now().replace(tzinfo=pytz.utc) > temp_url.expiry_date:
            return Response({"error": "This url has expired"},
                            status=status.HTTP_403_FORBIDDEN)

        return redirect('UploadedFile-detail', temp_url.related_file_id)


class UserViewset(viewsets.ReadOnlyModelViewSet):
    """
    Generic View for listing the Users.
    Only accessible by admin users currently.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
