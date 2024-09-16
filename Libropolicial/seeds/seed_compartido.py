import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Libropolicial.settings')

# Initialize Django
django.setup()

# Import the CuartoGuardiaUSH model from compartido
from compartido.models import CuartoGuardiaUSH

# Seeder function
def run():
    # List of cuartos de guardia to be inserted into the database
    cuartos = ['A', 'B', 'C', 'D']
    
    # Insert each cuarto into the database if it does not exist
    for cuarto in cuartos:
        CuartoGuardiaUSH.objects.get_or_create(cuarto=cuarto)
    
    print('Successfully seeded CuartoGuardiaUSH data.')

# Execute the function if the script is run directly
if __name__ == '__main__':
    run()
