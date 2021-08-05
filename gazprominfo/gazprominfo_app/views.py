from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from requests.exceptions import RequestException, MissingSchema
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from requests_html import HTMLSession
from .crud import save_new_emails, get_url_list
from .parsers import EmailHTMLParser


class UrlParserApiView(APIView):
    def _get_html(self, url: str) -> str:
        session = HTMLSession()
        try:
            return session.get(url).text
        except MissingSchema:
            err_msg = f"Url '{url}' is not valid." if url else "Empty url-to-parse get parameter"
            raise drf_exceptions.ParseError(detail=err_msg)
        except RequestException:
            raise drf_exceptions.APIException(detail=f"Resource {url} is not available or other connection error.")

    def get(self, request, format=None):
        url = request.GET.get("url-to-parse", "")
        html = self._get_html(url)
        result = EmailHTMLParser(html).parse()
        result = list(result)
        result.sort()
        save_new_emails(url, result)
        return Response({"url": url, "emails": result}, status=200)


class EmailApiView(APIView):
    email_validator = EmailValidator()

    def _get_email(self, request) -> str:
        email = request.GET.get("email", "")
        try:
            self.email_validator(email)
            return email
        except ValidationError:
            err_msg = f"{email} is not a valid email" if email else "Get parameter 'email' wasn't passed"
            raise drf_exceptions.ParseError(detail=err_msg)

    def get(self, request, format=None):
        email = self._get_email(request)
        return Response({"email": email, "urls": get_url_list(email)}, status=200)
