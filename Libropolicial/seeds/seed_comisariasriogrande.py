import os
import sys
import django

# Agrega el directorio raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')
django.setup()

from comisariasriogrande.models import CodigoPolicialRG, CuartoGuardiaRG

def run():
    codigos = ['00', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34']
    cuartos = ['A', 'B', 'C', 'D']

    for codigo in codigos:
        CodigoPolicialRG.objects.get_or_create(codigo=codigo)

    for cuarto in cuartos:
        CuartoGuardiaRG.objects.get_or_create(cuarto=cuarto)

    print('Successfully seeded the database for comisariasriogrande')

if __name__ == '__main__':
    run()
