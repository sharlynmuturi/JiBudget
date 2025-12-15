from .forms import ProfileForm

def account_form(request):
    if request.user.is_authenticated:
        form = ProfileForm(instance=request.user)
    else:
        form = None
    return {'account_form': form}
