from logging import exception
from django.template import context_processors
from accounts.models import Bloger,Reader



def get_avatar(request):
    if request.user.is_authenticated:
        try:
            avatar_image = Bloger.objects.filter(user=request.user).first()
            if avatar_image is None:
                raise exception
        except :
            avatar_image =  Reader.objects.filter(user=request.user).first()
        return {
            'avatar_image':avatar_image
            }
    else:
        return {
            'avatar_image':None
            }
            