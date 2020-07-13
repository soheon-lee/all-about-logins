import json
import bcrypt
import jwt

from django.views           import View
from django.http            import HttpResponse
from django.http            import JsonResponse
from django.core.validators import (
    validate_email,
    ValidationError
)

from local_settings import (
    SECRET_KEY,
    ALGORITHM
)
from .models        import Account

class SignUpView(View):
    def post(self, request):
        payload = json.loads(request.body)

        try:
            validate_email(payload['email'])

            try:
                if Account.objects.filter(email_account = payload['email']).exists():
                    return JsonResponse({'message': 'DUPLICATED_EMAIL'}, status = 400)

                print("1) original password: ", payload['password'])
                print("2) encoded password: ", payload['password'].encode())
                print("3) bcrypt hashed with gensalt: ", bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt()))
                print("4) decoded password: ", bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt()).decode())

                password = bcrypt.hashpw(
                    payload['password'].encode(), 
                    bcrypt.gensalt()
                ).decode()

                Account(
                    name          = payload['name'],
                    email_account = payload['email'],
                    password      = password
                ).save()

                return HttpResponse(status = 200)

            except KeyError as e:
                return JsonResponse({'message': f'MISSING_{e}'}, status = 400)

        except ValidationError:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)

class SignInView(View):
    def post(self, request):
        payload  = json.loads(request.body)
        email    = payload['email']
        password = payload['password']

        try:
            validate_email(email)

            try:
                if Account.objects.filter(email_account = email).exists():
                    user = Account.objects.get(email_account = email)

                    if bcrypt.checkpw(password.encode(), user.password.encode()):
                        token = jwt.encode({'user_email':email}, SECRET_KEY, algorithm = ALGORITHM).decode()
                        return JsonResponse({'Authorization': token}, status = 200)

                    return HttpResponse(status = 401)

                return HttpResponse(status = 401)

            except KeyError as e:
                return JsonResponse({'message': f'MISSING_{e}'}, status = 400)

        except ValidationError:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)

