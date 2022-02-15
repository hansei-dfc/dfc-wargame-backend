import json
from flask import Flask, Response

def make_packet(statusCode = 200, message = "", data = None):
    return Response(
        response=json.dumps({
            "is_success": statusCode == 200,
            "message": message,
            "data": data
        }),
        status=statusCode,
        mimetype='application/json'
    )
