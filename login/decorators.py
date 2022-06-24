from django.shortcuts import redirect


# Only show the page when the user is admin
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('request-evaluation')

    return wrapper_func
