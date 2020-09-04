import jwt
import json
import bcrypt
import requests

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
from .models import (
    Account,
    SocialMedia,
    Dog
)

class SignUpView(View):
    def get(self, request):
        users = Account.objects.all()
        user_data = [{
            'email': user.email_account
        } for user in users]
        return JsonResponse({'users': user_data}, status = 200)

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

        missing_key = (
            '\'email\'' * (not email) +
            ' and ' * ((not email) * (not password))+
            '\'password\'' * (not password)
        )

        return JsonResponse({'message': 'KEY_ERROR: ' + missing_key}, status = 400)

class SignInView(View):
    def post(self, request):
        payload  = json.loads(request.body)
        email    = payload.get('email', None)
        password = payload.get('password', None)

        if email and password:
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

class KakaoLoginView(View):
    def post(self, request):

        SOCIAL_MEDIA   = SocialMedia.objects.get(name = 'kakao')
        KAKAO_AUTH_URL = 'https://kapi.kakao.com/v2/user/me'

        try:
            access_token   = request.headers.get('Authorization', None)
            headers        = {'Authorization': f'Bearer {access_token}'}
            kakao_response = requests.request("POST", kakao_url, headers = headers).json()
            kakao_email    = kakao_response['kakao_account']['email']

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status = 400)

        if Account.objects.filter(email_account = kakao_email, social_media = SOCIAL_MEDIA).exists():
            user         = Account.objects.get(email_account = kakao_email, social_media = SOCIAL_MEDIA)
            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

            return JsonResponse({'access_token' : access_token}, status = 200)

        user         = Account(email_account = kakao_email, social_media = SOCIAL_MEDIA).save()
        access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

        return JsonResponse({'access_token' : access_token}, status = 200)

class GoogleLoginView(View):
    def post(self, request):
        SOCIAL_MEDIA    = SocialMedia.objects.get(name = 'google')
        GOOGLE_AUTH_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='

        access_token = request.headers.get('Authorization', None)
        response     = requests.get(GOOGLE_AUTH_URL + access_token)
        email        = response.json()['email']

        if Account.objects.filter( email_account = email, social_media = SOCIAL_MEDIA).exists():

            user = Account.objects.get(
                email_account = email,
                social_media  = SOCIAL_MEDIA
            )
            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

            return JsonResponse({'access_token' : access_token}, status = 200)

        user = Account(
            email_account = email,
            social_media  = SOCIAL_MEDIA
        )
        user.save()

        access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

        return JsonResponse({'access_token' : access_token}, status = 200)


class DogView(View):

    def get(self, request):

        doggy = Dog.objects.values()

        return JsonResponse({'my_dogs' : list(doggy)}, status = 200)

    def delete(self, request):

        data = json.loads(request.body)
        puppy_name = data['name']

        Dog.objects.get(name = puppy_name).delete()

        return JsonResponse({'message': 'DOG_DELTED!'}, status = 200)

    def post(self, request):

        data = json.loads(request.body)

        puppy_name = data['name']
        puppy_jong = data['jong']
        puppy_age = data['dog_age']

        Dog.objects.create(
            name = puppy_name,
            jong = puppy_jong,
            age = puppy_age
        )


        return JsonResponse({'message': 'DOG_SAVED!'}, status = 201)


