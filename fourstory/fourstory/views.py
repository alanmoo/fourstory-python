import foursquare
from django.shortcuts import redirect, render
from django.conf import settings

client = foursquare.Foursquare(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    redirect_uri=settings.REDIRECT_URI
    )

def login(request):

    auth_uri = client.oauth.auth_url()

    return redirect(auth_uri, False)

def index(request):

    code = request.GET.get('code')
    if not code:
	return render(request, 'logged-out.html')

    else:
	access_token = client.oauth.get_token(code)
	client.set_access_token(access_token)
	checkin = client.users.checkins(params={'limit': 1})

	return render(request, 'authorized.html', {'checkin':checkin})
