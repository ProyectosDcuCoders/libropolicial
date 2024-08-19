# compartido/utils.py
def user_is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
