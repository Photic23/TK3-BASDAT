def context_user_getter(request):
    user = {
        'nama': request.session.get('nama'),
        'email': request.session.get('email'),
        'roles': request.session.get('roles'),
        'premium_status': request.session.get('premium_status')
    }
     
    return user
