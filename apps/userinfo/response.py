from django.http import JsonResponse


class Response:

    def base(self, values=None, message="", status=200, success='True'):
        if values is None:
            values = []

        return JsonResponse({
            'success': success,
            'values': values,
            'message': message
        }, status=status)

    @staticmethod
    def ok(values=None, message="", success=True):
        return Response().base(success=True, values=values, message=message, status=200)

    @staticmethod
    def badRequest(values=None, message="", success=False):
        return Response().base(success=success, values=values, message=message, status=400)
