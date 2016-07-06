# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse


class BaseContentTypeMiddleware:

    def process_request(self, request):
        return None

    def bad_request(self, content=None, content_type=None):
        content = content or "Bad request"
        content_type = content_type or 'text/plain'
        return HttpResponse(content, content_type=content_type, status=400)


class JsonMiddleware(BaseContentTypeMiddleware):
    """Check JSON requests validity and parse data.
    If request content type is JSON, parse the request body as JSON and put
    the result parsed object in request.JSON, also available as request.DATA.
    If JSON parsing failed, return a "400 Bad Request" response.
    """

    content_type_re = re.compile(r'(application|text)/([a-z0-9_.-]+\+)?json')

    def process_request(self, request):
        content_type = request.META['CONTENT_TYPE']
        if JsonMiddleware.content_type_re.match(content_type):
            try:
                request.JSON = json.loads(request.body)
            except ValueError:
                return self.bad_request("Invalid JSON format")
            request.DATA = property(lambda s: s.JSON)
            return None
        return super().process_request(request)


class XmlMiddleware(BaseContentTypeMiddleware):
    """Check XML requests validity and parse data.
    If request content type is XML, parse the request body as XML and put
    the result parsed object in request.XML, also available as request.DATA.
    If XML parsing failed, return a "400 Bad Request" response.

    Requires `xmltodict` module.
    """

    content_type_re = re.compile(r'(application|text)/([a-z0-9_.-]+\+)?xml')

    def process_request(self, request):
        import xmltodict  # import here to avoid import errors if the module is
                          # not installed and we don't need XmlMiddleware.
        content_type = request.META['CONTENT_TYPE']
        if XmlMiddleware.content_type_re.match(content_type):
            try:
                request.XML = xmltodict.parse(request.body)
            except:
                return self.bad_request("Invalid XML format")
            request.DATA = property(lambda s: s.XML)
            return None
        return super().process_request(request)


class ContentTypeMiddleware(JsonMiddleware, XmlMiddleware):
    """Handles the following content types:
        - JSON
        - XML
    """
