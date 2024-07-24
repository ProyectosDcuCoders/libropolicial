import os
import sys
import django

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')
django.setup()

from divisioncomunicaciones.models import EncargadoGuardia, PersonalGuardia

def run():
    encargados = [
        "Fabio Pantoja", "Mario Meza", "Analia Leguizamon", "Martin Perea",
        "Tamara Obligado", "Alejandro Galdeano", "Maximiliano Cortez",
        "Carlos Caliva", "Jorge Rojas", "Brian Fazano",
        "Jonathan Segovia", "Solange Andrade"
    ]

    for nombre in encargados:
        EncargadoGuardia.objects.get_or_create(nombre_apellido=nombre)
        PersonalGuardia.objects.get_or_create(nombre_apellido=nombre)

    print('Successfully seeded the database for EncargadoGuardia and PersonalGuardia')

if __name__ == '__main__':
    run()
