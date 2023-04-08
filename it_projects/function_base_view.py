import traceback

from django.http import JsonResponse
from my_site_django.settings import DEBUG

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}


def ret(json_object, status=200):
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    res = {"errorMessage": str(exception)}
    if DEBUG:
        tracebacks = traceback.format_exc()
        res |= {'traceback': tracebacks}

    return ret(res, status=400)
