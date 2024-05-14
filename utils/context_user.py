def context_user_getter(request):
    user = {
        'nama': request.session.get('nama'),
        'email': request.session.get('email'),
        'roles': request.session.get('roles'),
    }
     
    return user
