def add_username_to_context(request):
    # Assuming you are using Django's built-in authentication system
    if 'user_exists' in request.session:
        return {'user_exists': request.session['user_exists']}
    return {}