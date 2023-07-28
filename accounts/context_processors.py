from accounts.models import Wallet,Users

def add_username_to_context(request):
    # Assuming you are using Django's built-in authentication system
    if 'user_exists' in request.session:
        user = Users.objects.get(username = request.session['user_exists'])
        return {'user_exists': request.session['user_exists'],'wallet':Wallet.objects.get(user = user).amount}
    return {}