from django.contrib.auth.models import Group

def global_user_permissions(request):
    """Agrega permisos globales al contexto de las plantillas."""
    user = request.user
    if not user.is_authenticated:
        return {'can_access_comisarias': False}

    # Verifica si el usuario cumple los criterios para ver las comisarías
    can_access_comisarias = (
        user.is_superuser or
        user.groups.filter(name='dcu101').exists()
    )

    return {'can_access_comisarias': can_access_comisarias}
