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
from comisarias.models import CodigoPolicialUSH, CodigosSecundarios, CuartoGuardiaUSH

# Función principal para poblar la base de datos
def run():
    # Lista de códigos policiales y secundarios a insertar en la base de datos
    codigos = ['00', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', 'Constancia']
    codigos_secundarios = ['00', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34']
    # Lista de cuartos de guardia a insertar en la base de datos
    cuartos = ['A', 'B', 'C', 'D']

    # Inserta cada código en la base de datos si no existe
    for codigo in codigos:
        CodigoPolicialUSH.objects.get_or_create(codigo=codigo)

    # Inserta cada código secundario en la base de datos si no existe
    for codigo in codigos_secundarios:
        CodigosSecundarios.objects.get_or_create(codigo=codigo)

    # Inserta cada cuarto en la base de datos si no existe
    for cuarto in cuartos:
        CuartoGuardiaUSH.objects.get_or_create(cuarto=cuarto)

    print('Successfully seeded the database for comisarias')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
