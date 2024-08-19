import os
import sys
import django

# Agrega el directorio raíz del proyecto al sys.path para que los módulos del proyecto puedan ser importados
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Establece la variable de entorno para las configuraciones de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Inicializa la configuración de Django
django.setup()

# Importa los modelos necesarios desde la aplicación divisioncomunicaciones
from divisioncomunicaciones.models import EncargadoGuardia, PersonalGuardia

# Función principal para poblar la base de datos
def run():
    # Lista de nombres de encargados de guardia
    encargados = [
        "Fabio Pantoja", "Mario Meza", "Analia Leguizamon", "Martin Perea",
        "Tamara Obligado", "Alejandro Galdeano", "Maximiliano Cortez",
        "Carlos Caliva", "Jorge Rojas", "Brian Fazano",
        "Jonathan Segovia", "Solange Andrade"
    ]

    # Itera sobre cada nombre en la lista de encargados
    for nombre in encargados:
        # Crea o obtiene un objeto EncargadoGuardia con el nombre dado
        EncargadoGuardia.objects.get_or_create(nombre_apellido=nombre)
        # Crea o obtiene un objeto PersonalGuardia con el nombre dado
        PersonalGuardia.objects.get_or_create(nombre_apellido=nombre)

    print('Successfully seeded the database for EncargadoGuardia and PersonalGuardia')

# Ejecuta la función principal si el script se está ejecutando directamente
if __name__ == '__main__':
    run()
