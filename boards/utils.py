from accounts.models import Bloger


def get_user(request):
    if request.user.is_authenticated:
        if Bloger.objects.filter(user=request.user).exists():
            bloger = 'bloger'
        else :
            bloger = 'None'
    else:
        bloger='None'
    return bloger 