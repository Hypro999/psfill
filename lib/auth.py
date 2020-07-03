from bs4 import BeautifulSoup  # type: ignore
from requests import Session
from settings import url

def authenticate(session: Session, txtemail: str, txtpass: str) -> None:
    print("Logging in... ", end="", flush=True)
    login_url = url("/Login.aspx")

    # We need to fetch the login page with a GET request instead of directly posting because
    # this is an ASPX application and there are some specific POST parameters that we will
    # need to provide using the credentials from the fetched page. This is similar to needing
    # to GET before POSTing to extract a CSRF token for HTML forms.
    response = session.get(login_url)
    if response.status_code != 200:
        print("Failure.\nCould not fetch the login page.")
        exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    view_state = soup.find(id="__VIEWSTATE")["value"]
    view_state_generator = soup.find(id="__VIEWSTATEGENERATOR")["value"]
    event_validator= soup.find(id="__EVENTVALIDATION")["value"]

    # Now login using the user-supplied credentials and the page parameters.
    # The web application has this stupid design where if you specify incorrect credentials,
    # instead of getting a 401 you get a 200 and there is a little script tacked on to the
    # top of the HTML document saying that the provided credentials are correct.
    # But then again this application wasn't designed to be used as an API, so I guess I can't
    # blame them?
    # If you login with the right credentials then you will be redirected to the dashboard (302).
    form_data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": view_state,
        "__VIEWSTATEGENERATOR": view_state_generator,
        "__EVENTVALIDATION": event_validator,
        "TxtEmail": txtemail,
        "txtPass": txtpass,
        "Button1": "Login",
        "txtEmailId": "",
    }
    response = session.post(login_url, data=form_data, allow_redirects=False)
    if response.status_code != 302:
        print("Failure.\nAre the credentials you provided correct?")
        exit(1)
    session.get(url(response.headers["Location"]))  # This redirect-triggered request will actually validate the session cookie. Which is weird...

    # Now we have a valid session cookie stored as "ASP.NET_SessionId".
    print("Success.")
    return

