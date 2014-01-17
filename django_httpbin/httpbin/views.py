from django.shortcuts import render_to_response
from django.http.response import HttpResponse, HttpResponseBadRequest, \
    HttpResponseServerError, HttpResponseRedirect, HttpResponseRedirectBase
from json import dumps
from re import compile, sub

# Views

def main_page(request):
    return render_to_response('django_httpbin.html', {})

def ip(request):
    ip = extract_ip(request)
    if ip:
        response = HttpResponse(dumps({"origin" : ip}))
        response['Content-Type'] = 'application/json'
        return response
    return HttpResponseBadRequest("HTTP 400 Bad Request")

def user_agent(request):
    useragent = extract_user_agent(request)
    if useragent:
        response = HttpResponse(dumps({"user-agent" : useragent}))
        response['Content-Type'] = 'application/json'
        return response
    return HttpResponseBadRequest("HTTP 400 Bad Request")

def headers(request):
    response = HttpResponse(dumps({"headers": extract_headers(request)}, sort_keys=True))
    response['Content-Type'] = 'application/json'
    return response

def get(request):
    ip = extract_ip(request)
    headers = extract_headers(request)
    getparams = extract_get_params(request)
    response = HttpResponse(dumps({"args": getparams, "origin": ip, \
       "headers": headers, "url": request.build_absolute_uri()}, sort_keys=True))
    response['Content-Type'] = 'application/json'
    return response

def status(request, statuscode):
    message = ""
    if int(statuscode) == 418:
        message = """
    -=[ teapot ]=-

       _...._
     .'  _ _ `.
    | .\"` ^ `\". _,
    \_;`\"---\"`|//
      |       ;/
      \_     _/
        `\"\"\"`
        """
    response = HttpResponse(message, status=int(statuscode))
    response['Content-Type'] = 'text/plain; charset=UTF-8'
    return response

def response_headers(request):
    params = extract_get_params(request)
    response = HttpResponse()
    response['Content-Type'] = 'application/json'
    for param in params:
        response[param] = params[param]
    resp_headers = {h:v for (h, v) in response._headers.values()}
    resp_headers.update(params)
    response.content = dumps(resp_headers)
    return response

def redirect_to(request):
    target_url = request.GET.get('url', None)
    if target_url:
        return HttpResponseRedirect(target_url)
    else:
        return HttpResponseServerError()

# Helper methods

def extract_headers(request):
    regex = compile('^HTTP_')
    dehyphenize = lambda x: sub("_", "-", x)
    hds = [(dehyphenize(regex.sub('', header).title()), value) for (header, value) 
       in request.META.items() if header.startswith('HTTP_')]
    headers = dict(hds)
    if 'CONTENT_LENGTH' in request.META:
        headers['Content-Length'] = request.META['CONTENT_LENGTH']
    return headers

def extract_user_agent(request):
    if 'HTTP_USER_AGENT' in request.META:
        return request.META['HTTP_USER_AGENT']

def extract_ip(request):
    if 'REMOTE_ADDR' in request.META:
        return request.META['REMOTE_ADDR']
    
def extract_get_params(request):
    return dict((p.encode('ascii'), v.encode('ascii')) for (p, v) in request.GET.items())