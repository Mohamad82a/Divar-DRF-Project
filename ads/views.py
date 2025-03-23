from django.db.models import Q
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from yaml import serialize
from .models import Ad
from .serializers import AdSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from .pagination import CustomPageNumberPagination
from .permissions import IsPublisherOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter


class AdsListView(APIView, CustomPageNumberPagination):
    serializer_class = AdSerializer

    def get(self, request):
        ads = Ad.objects.filter(is_public=True)
        paginated_ads = self.paginate_queryset(ads, request)
        serializer = AdSerializer(instance=paginated_ads, many=True)
        return self.get_paginated_response(serializer.data)


class AdCreateView(APIView):
    serializer_class = AdSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = request.user
            serializer.validated_data['is_public'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdDetailView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        serializer = AdSerializer(instance=ad)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AdEditView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsPublisherOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Ad.objects.all(), id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(instance=ad, validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdDeletetView(APIView):
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticated, IsPublisherOrReadOnly,)

    def get_object(self, pk):
        obj = get_object_or_404(Ad.objects.all(), id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def delete(self, request, pk):
        ad = self.get_object(pk)
        ad.delete()
        return Response({'response': 'Ad deleted successfully'}, status=status.HTTP_200_OK)


class AdSearchView(APIView, CustomPageNumberPagination):
    serializer_class = AdSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Search ads by title or caption",
            )
        ],
        responses={200: AdSerializer(many=True)},
    )

    def get(self, request):
        query = request.GET.get('search', '')
        if not query:
            return Response({'message': 'No search term'}, status=status.HTTP_400_BAD_REQUEST)

        searched_ads = Ad.objects.filter(Q(title__icontains=query) | Q(caption__icontains=query))

        if not searched_ads:
            return Response({'message': 'No results found'}, status=status.HTTP_400_BAD_REQUEST)

        paginated_search = self.paginate_queryset(searched_ads, request)
        serializer = AdSerializer(instance=paginated_search, many=True)
        return self.get_paginated_response(serializer.data)