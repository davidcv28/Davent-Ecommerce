from rest_framework import mixins, viewsets, status, permissions
from ..serializers import userserializers
from django.contrib.auth.models import User
from ..permissions import IsAnonimousPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .. import filterset
from django_filters.rest_framework import DjangoFilterBackend
###############################################################
################STAFF USER VIEWSETS############################
###############################################################

####REGISTER STAFF VIEWSET
class RegisterAdminViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = userserializers.RegisterAdminSerializer
    queryset = User.objects.all()




####LIST USER VIEWSET
class ListUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filterset.UserUsernameFilters
    serializer_class = userserializers.ListUserSerializer
    queryset = User.objects.all()

###############################################################
############## NORMAL USER VIEWSETS############################
###############################################################

####REGISTER USER VIEWSET
class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAnonimousPermission]
    serializer_class = userserializers.RegisterUserSerializer
    queryset = User.objects.all()
###UPDATE USER VIEWSET
class UpdateUserViewSet(viewsets.GenericViewSet):
    permission_classes= [permissions.IsAuthenticated]
    parser_classes= [JSONParser, FormParser, MultiPartParser]
    def get_serializer_class(self):
        if self.action == 'update_info':
            return userserializers.UpdateUserSerializer
        if self.action == 'update_password':
            return userserializers.UpdatePasswordUserSerializer
        return userserializers.PerfilUpdateSerializer
    def get_queryset(self):
        if self.action == 'update_info':
            return User.objects.all()
    def get_object(self):
        if self.action == 'update_info':
            return self.request.user    
    #UPDATE INFO
    @action (detail = False, methods = ['get','patch'], url_path='update_info')
    def update_info(self,request):
        if request.method =='GET':
            serializer = self.get_serializer(request.user)
            return Response(
                serializer.data
            )
        serializer = self.get_serializer(data = request.data, instance = request.user, context = {'request':request}, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'exito':'Los datos se modificaron satisfactoriamente'
            }, status=status.HTTP_202_ACCEPTED
        )
    #UPDATE PASSWORD
    @action(detail = False, methods = ['post'], url_path='update_password')
    def update_password(self, request):
        serializer = self.get_serializer(data = request.data, instance = request.user, context={'request':request})
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(
            {
                'exito':'La contraseña de modifico satisfactoriamente'
            }, status=status.HTTP_200_OK
        )
    @action(detail=False, methods = ['post'], url_path='update_image_profile')
    def update_image_profile(self, request):
        serializer = self.get_serializer(data = request.data, instance = request.user, context = {'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'exito': 'La foto de perfil se modifico satisfactoriamente',
                'image_url':request.user.perfil.image.url
            }
        )
        
####AUTHENTICATE USER VIEWSET
class AuthenticateUserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAnonimousPermission]
    serializer_class = userserializers.UserAuthenticatedSerializer
    @action (detail=False, methods = ['post'], url_path='token')
    def login(self,request):
        serializer = self.get_serializer(data=request.data , context = {'request':request})
        serializer.is_valid(raise_exception= True)
        user = serializer.validated_data.get('user')
        token,created = Token.objects.get_or_create(user = user)
        return Response (
            {
                'token':token.key,
                'user_id':user.id
            }, status=status.HTTP_200_OK
        )
