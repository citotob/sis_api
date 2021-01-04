from django.http import JsonResponse
# from rest_framework.response import Response


class Response:

    def base(self=None, data=None, count=0, status=200, success='True', message=''):
        if data is None:
            data = []

        return JsonResponse({
            'success': success,
            'count': count,
            'data': data,
            'message': message,
        }, status=status)

    @staticmethod
    def ok(data=None, count=0, success=True, message=''):
        return Response().base(success=True, data=data, count=count, status=200, message=message)

    @staticmethod
    def badRequest(data=None, count=0, success=False, message=''):
        return Response().base(success=success, data=data, count=count, status=400, message=message)
