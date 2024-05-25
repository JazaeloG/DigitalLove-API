import json
from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from api.models import AtributosUsuario, Usuario
from api.serializers.ia_serlializers import AtributosSerializer, CompararRostrosSerializer
import requests

@extend_schema(
    methods=['POST'], 
    tags=['IA'], 
    description='Extraer atributos de fotos',
    request={
        'multipart/form-data': AtributosSerializer,
    },
    responses={200: AtributosSerializer}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, FileUploadParser])
def extraer_atributos(request, usuario_id):
    serializer = AtributosSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    file = serializer.validated_data['file']
    file_content = file.read()

    respuesta_ia = requests.post(settings.IA_EXTRACCION, files={'file': (file.name, file_content, file.content_type)})
    if respuesta_ia.status_code == 200:
        response_json = json.loads(respuesta_ia.content)
        attributes = {}
        hair_color_attributes = ['Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Gray_Hair']
        hair_type_attributes = ['Straight_Hair', 'Wavy_Hair']

        for face in response_json['result'][0]['face']:
            label = face['label']
            prob = float(face['prob'])
            attributes[label] = prob

        piel_blanca = attributes.get('Pale_Skin', 0) > 0.1
        lentes = attributes.get('Eyeglasses', 0) > 0.5
        cara_ovalada = attributes.get('Oval_Face', 0) > 0.18

        usuario = Usuario.objects.get(id=usuario_id)

        atributos_usuario, created = AtributosUsuario.objects.get_or_create(usuario=usuario)
        atributos_usuario.caraOvalada = cara_ovalada
        atributos_usuario.lentes = lentes
        atributos_usuario.pielBlanca = piel_blanca
        atributos_usuario.save()
        max_hair_color_label = max(hair_color_attributes, key=lambda x: attributes.get(x, 0))
        max_type_label = max(hair_type_attributes, key=lambda x: attributes.get(x, 0))

        desired_attributes = {
            'CaraOvalada': cara_ovalada,
            'Lentes': lentes,
            'PielBlanca': piel_blanca,
            'ColorCabello': max_hair_color_label,
            'TipoCabello': max_type_label
        }

        return Response(desired_attributes, status=status.HTTP_200_OK, content_type='application/json')
    else:  
        return Response({'message': 'Error al extraer atributos'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=['POST'], 
    tags=['IA'], 
    description='Comparar rostro con identificacion de usuario',
    request= CompararRostrosSerializer,
    responses={200: CompararRostrosSerializer}
)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, FileUploadParser])
def comparar_rostros(request):
    serializer = CompararRostrosSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    file = serializer.validated_data['imagenRostro']
    fileIdentificacion = serializer.validated_data['imagenIdentificacion']
    file_content = file.read()
    fileIdentificacion_content = fileIdentificacion.read()

    respuesta_ia = requests.post(settings.IA_COMPARACION, files={'imagenRostro': (file.name, file_content, file.content_type), 'imagenIdentificacion': (fileIdentificacion.name, fileIdentificacion_content, fileIdentificacion.content_type)})

    if respuesta_ia.status_code == 200:
        response_json = json.loads(respuesta_ia.content)
        return Response(response_json, status=status.HTTP_200_OK, content_type='application/json')
    else:  
        return Response({'message': 'Error al comparar rostros'}, status=status.HTTP_400_BAD_REQUEST)
