import json
import bcrypt
import jwt

from datetime import (
    datetime,
    timedelta
)

from django.views           import View
from django.http            import HttpResponse
from django.http            import JsonResponse
from django.core.validators import (
    validate_email,
    ValidationError
)

from config  import (
    SECRET_KEY,
    ALGORITHM
)
from .models import Account

class SignUpView(View):
    def post(self, request):
        payload  = json.loads(request.body)
        email    = payload.get('email', None)
        password = payload.get('password', None)

        if email and password:
            try:
                validate_email(payload['email'])

                if Account.objects.filter(email_account = payload['email']).exists():
                    return JsonResponse({'message': 'DUPLICATED_EMAIL'}, status = 400)

                password = bcrypt.hashpw(
                    payload['password'].encode(),
                    bcrypt.gensalt()
                ).decode()

                Account(
                    email_account = payload['email'],
                    password      = password
                ).save()

                return JsonResponse({'message': 'SUCCESS'}, status = 200)

            except ValidationError:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)

        return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        payload  = json.loads(request.body)
        email    = payload.get('email', None)
        password = payload.get('password', None)

        if email and password:
            try:
                if Account.objects.filter(email_account = email).exists():
                    user = Account.objects.get(email_account = email)

                    if bcrypt.checkpw(password.encode(), user.password.encode()):
                        exp   = datetime.utcnow() + timedelta(hours = 1)
                        token = jwt.encode(
                            {
                                'user_id' : user.id,
                                'exp'     : exp
                            }, SECRET_KEY, algorithm = ALGORITHM).decode()

                        return JsonResponse({'Authorization': token}, status = 200)

                    return JsonResponse({'message': 'UNAUTHORIZED'}, status = 401)

                return JsonResponse({'message': 'UNAUTHORIZED'}, status = 401)

        return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

