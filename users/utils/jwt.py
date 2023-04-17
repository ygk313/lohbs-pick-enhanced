import os, jwt

# 토큰 암호화 복호화에 쓸 해싱 알고리즘과 비밀키
JWT_Algorithm = os.environ.get("JWT_ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")

# jwt 토큰 생성
def encode_jwt(data):
    # jwt.encode의 경우 반환 값이 바이트 스트링이기때문에, utf-8 문자열로 변환
    return jwt.encode(data, SECRET_KEY, algorithm=JWT_Algorithm).decode("utf-8")

# jwt 토큰 복호화 - verify the jwt token signature and return the token claims
def decode(access_token):
    return jwt.decode(
        access_token,
        SECRET_KEY,
        algorithms=[JWT_Algorithm],
        issuer = "LOHBS_PICK Web Backend",
        options = {"verify_aud" : False},
    )