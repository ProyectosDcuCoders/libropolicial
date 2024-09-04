import os
import sys
import django

# Agrega el directorio raíz del proyecto al sys.path para que los módulos del proyecto puedan ser importados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Establece la variable de entorno para las configuraciones de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Inicializa la configuración de Django
django.setup()

# Importa los modelos necesarios
from comisarias.models import (
    CodigoPolicialUSH, CodigosSecundarios, CuartoGuardiaUSH, DependenciasSecundarias, 
    SolicitanteCodigo, ServiciosEmergencia, InstitucionesHospitalarias, 
    DependenciasMunicipales, DependenciasProvinciales
)

# Función principal para poblar la base de datos
def run():
    # Lista de códigos policiales y secundarios a insertar en la base de datos junto con sus nombres
    codigos = [
        ('00', 'PERSONA FALLECIDA'),
        ('01', 'HOMICIDIO'),
        ('02', 'SUICIDIO'),
        ('03', 'ROBO'),
        # Agrega más códigos aquí según sea necesario
        ('04', 'ACCIDENTE DE TRANSITO'),
        ('05', 'DAÑOS'),
        ('06', 'CONTRAVENCION'),
        ('07', 'APOYO POLICIAL'),
        ('08', 'VIOLENCIA DE GENERO'),
        ('09', 'VIOLENCIA DE GENERO EN CURSO'),
        ('10', 'VIOLENCIA DE GENERO CON AGRECIONES FISICAS'),
        ('11', 'INCENDIO'),
        ('12', 'PERSONA CON PROHIBICION DE ACERCAMIENTO'),
        ('13', 'PERSONA ARMADA'),
        ('14', 'PERSONA TIRADA EN LA VIA PUBLICA'),
        ('15', 'PERSONA HERIDA'),
        ('16', 'PERSONA CON ABUSO SEXUAL'),
        ('17', 'PERSONA CON INTENTO DE SUICIDIO'),
        ('18', 'PERSONA EXTRAVIADA O PERDIDA'),
        ('19', 'PRESENCIA DE DROGAS'),
        ('20', 'PEDIDO DE AUXILIO'),
        ('21', 'VIOLENCIA FAMILIAR EN CURSO'),
        ('22', 'VIOLENCIA FAMILIAR HISTORICA'),
        ('23', 'AMENAZA DE BOMBA'),
        ('24', 'ARTEFACTO EXPLOSIVO'),
        ('25', 'ANIMALES SUELTOS'),
        ('26', 'CORDON SANITARIO'),
        ('27', 'FUGA DE GAS'),
        ('28', 'USURPACION'),
        ('29', 'PICADAS, EXCESO DE VELOCIDAD/MANIOBRAS PELIGROSAS CON AUTOMOTORES EN VIA PUBLICA'),
        ('30', 'CORTE O DESVIO DE TRANSITO'),
        ('31', 'MANIFESTACION O GRUPOS DE PERSONAS'),
        ('32', 'RUIDOS MOLESTOS'),
        ('33', 'ALARMA'),
        ('34', 'PRESENCIA POLICIAL')
    ]

    codigos_secundarios = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34']
    
    # Lista de cuartos de guardia a insertar en la base de datos
    cuartos = ['A', 'B', 'C', 'D']
    
    # Lista de dependencias secundarias
    dependencias_secundarias = ['C.G. y F.Nº1U.', 'C.G. y F.Nº2U.', 'D.P.C.U', 'D.S.E.U']

    # Lista de solicitantes de código
    solicitantes_codigo = ['D.C.U', 'PARTICULAR', 'COMISARIA', 'OTRO']

    # Lista de servicios de emergencia
    servicios_emergencia = ['BOMBEROS 2 DE ABRIL', 'BOMBEROS ZONA NORTE', 'BOMBEROS ZONA CENTRO', 'DTO. KUANIP']

    # Lista de instituciones hospitalarias
    instituciones_hospitalarias = ['H.R.U', 'CLINICA SAN JORGE', 'BAHIA SALUD', 'FUEGUINA SALUD', 'SANOS']

    # Lista de dependencias municipales
    dependencias_municipales = ['TRANSITO MUNICIPAL', 'HABILITACIONES COMERCIALES', 'DIRECCION DE TRANSPORTE', 'SEC. DE HABITAT Y ORDENAMIENTO URBANO', 'ZOONOSIS', 'RESGUARDO DE FAUNA', 'AREA DE BROMATOLOGIA', 'SERVICIOS GENERALES', 'SECRETARIA DE EQUINOS', 'JUZGADO ADM. MUNICIPAL DE FALTAS', 'SEC. MEDIO AMBIENTE Y DESARROLLO SUSTENTABLE', 'SECRETARIA DE LA MUJER']

    # Lista de dependencias provinciales
    dependencias_provinciales = ['CAMUZZI USHUAIA', 'D.P.E', 'TRANSPORTE PROVINCIAL', 'D.P.O.S.S.', 'MANEJO DEL FUEGO', 'RECURSOS NATURALES', 'PROTECCION CIVIL', 'MINISTERIO DE TRABAJO', 'SERVICIOS GENERALES', 'DIR. PROV. DE VIALIDAD', 'I.P.V', 'A.R.E.F', 'O.S.E.F', 'DIV. PROV. PUERTOS' ]

    # Inserta cada código en la base de datos si no existe
    for codigo, nombre in codigos:
        CodigoPolicialUSH.objects.update_or_create(codigo=codigo, defaults={'nombre_codigo': nombre})

    # Inserta cada código secundario en la base de datos si no existe
    for codigo in codigos_secundarios:
        CodigosSecundarios.objects.get_or_create(codigo=codigo)

    # Inserta cada cuarto en la base de datos si no existe
    for cuarto in cuartos:
        CuartoGuardiaUSH.objects.get_or_create(cuarto=cuarto)

    # Inserta cada dependencia secundaria en la base de datos si no existe
    for dependencia in dependencias_secundarias:
        DependenciasSecundarias.objects.get_or_create(dependencia=dependencia)

    # Inserta cada solicitante de código en la base de datos si no existe
    for solicitante in solicitantes_codigo:
        SolicitanteCodigo.objects.get_or_create(codigo=solicitante)

    # Inserta cada servicio de emergencia en la base de datos si no existe
    for servicio in servicios_emergencia:
        ServiciosEmergencia.objects.get_or_create(nombre=servicio)

    # Inserta cada institución hospitalaria en la base de datos si no existe
    for institucion in instituciones_hospitalarias:
        InstitucionesHospitalarias.objects.get_or_create(nombre=institucion)

    # Inserta cada dependencia municipal en la base de datos si no existe
    for dependencia in dependencias_municipales:
        DependenciasMunicipales.objects.get_or_create(nombre=dependencia)

    # Inserta cada dependencia provincial en la base de datos si no existe
    for dependencia in dependencias_provinciales:
        DependenciasProvinciales.objects.get_or_create(nombre=dependencia)

    print('Successfully seeded the database for comisarias')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
