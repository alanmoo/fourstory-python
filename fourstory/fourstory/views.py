import foursquare
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required


client = foursquare.Foursquare(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI
    )

def login(request):

    auth_uri = client.oauth.auth_url()

    return redirect(auth_uri, False)

def index(request):

    code = request.GET.get('code') or request.session.__getitem__('code')
    if not code:
	return render(request, 'logged-out.html')

    else:
	request.session.__setitem__('code', code)
	access_token = client.oauth.get_token(code)
	client.set_access_token(access_token)
	checkin = client.users.checkins(params={'limit': 1})

	return render(request, 'authorized.html', {'checkin':checkin})


def recentCheckins(request):
    code = request.session.__getitem__('code')

    # request.session.__setitem__('code', code)
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    user = client.users()
    checkins = client.users.checkins()

    return render(request, 'recent.html', {'checkins':checkins, 'user':user})
