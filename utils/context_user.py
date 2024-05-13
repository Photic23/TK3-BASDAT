def context_user_getter(request):
    context = {
        'nama': request.session.get('nama'),
        'password': request.session.get('password'),
        'gender': request.session.get('gender'),
        'tempat_lahir': request.session.get('tempat_lahir'),
        'is_verified': request.session.get('is_verified'),
        'kota_asal': request.session.get('kota_asal'),
        'roles': request.session.get('roles'),
    }
     
    return context
