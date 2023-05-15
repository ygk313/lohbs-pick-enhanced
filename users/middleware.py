# 인증이 필요한 요청이 올 때 토큰을 확인하기
# 토큰을 복호화하기
# 복호화한 토큰의 내용이 유효한지 확인하기

from os import access
from django.contrib.auth.models import User
# 인증실패 시 Response를 반환하기 위함
from http import HTTPStatus
from django.http import JsonResponse
# 인증 실패 예외 처리를 위함.
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from users.utils.jwt import decode_jwt
# 만료 토큰 예외 처리를 위함.
from jwt.exceptions import ExpiredSignatureError
import pdb

class JsonWebTokenMiddleWare(object):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            if (request.path != "/accounts/login/" and request.path != "/accounts/signup/" and "admin" not in request.path and request.path != "/login_page/"):
                
                # header에서 access_token 추출
                # headers = request.headers
                # access_token = headers.get("Authorization", None)
                access_token = request.COOKIES.get('jwt')
                # pdb.set_trace()
                if not access_token:
                    if request.path == "/": return self.get_response(request)
                    raise PermissionDenied()
                
                # access_token 복호화해서 payload 얻기
                payload = decode_jwt(access_token)
                username = payload.get("aud", None)
                
                if not username:
                    raise PermissionDenied()

                user = User.objects.get(username=username)
                request.user = user
                # pdb.set_trace()

            response = self.get_response(request)
        
            return response

        # 예외 처리
        except (PermissionDenied, User.DoesNotExist):
            return JsonResponse(
                {"error" : "Authroization Error"}, status = HTTPStatus.UNAUTHORIZED
            )
        except ExpiredSignatureError:
            return JsonResponse(
                {
                    "error" : "Expired token. Please log in again"
                },
                status = HTTPStatus.FORBIDDEN
            )

