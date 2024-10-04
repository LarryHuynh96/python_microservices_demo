import os
import requests


def login(request):
    auth = request.authorization
    if not auth:
        return None, ("Missing credentials", 401)
    basic_auth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.getenv('AUTH_SVC_ADDRESS')}/login",
        auth=basic_auth
    )
    if response.status_code == 200:
        return response.txt, None
    else:
        return None, (response.txt, response.status_code)
