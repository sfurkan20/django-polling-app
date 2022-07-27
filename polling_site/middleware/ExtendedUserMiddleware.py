from accounts.models import ExtendedUser


class ExtendedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            extendedUser = ExtendedUser.objects.filter(user__username=request.user.username)
            if len(extendedUser) > 0:
                request.extendedUser = extendedUser

        response = self.get_response(request)
        
        return response