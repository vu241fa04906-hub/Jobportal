from rest_framework.response import Response


def api_response(data=None, message="Success", status_code=200, errors=None):
    return Response(
        {
            "success": errors is None,
            "message": message,
            "data": data,
            "errors": errors,
        },
        status=status_code,
    )

