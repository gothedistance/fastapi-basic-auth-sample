import base64

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


def check_permission(method, path, auth):
    if method == "GET" and path == "_healthcheck":
        return True
    # Basic認証は Basic eurarear= みたいな文字列がAuthenticationに入る
    # BASE64エンコードされる仕様
    # Authenticationヘッダが万が一空の場合はスペースに置換して、それをsplitで1回だけ分割
    scheme, data = (auth or " ").split(" ", 1)
    # 無いと思うけど、ブラウザが送ってきたAuthenticationヘッダの認証スキームが
    # BasicじゃないならFalse
    if scheme != "Basic":
        return False
    # ユーザー名とパスワードがBase64でエンコードされたバイト配列でやってくるので
    # byte配列から文字列に復元している
    username, password = base64.b64decode(data).decode().split(":", 1)
    if username == "test" and password == "test123":
        return True


@app.middleware("http")
async def check_authentication(request: Request, call_next):
    # Basic認証の場合、Authorizationヘッダに入力されたユーザー名とパスワードが入ってくること
    auth = request.headers.get("Authorization")
    # 認証不可の場合、Basic認証をブラウザに要求するレスポンスヘッダを返す
    if not check_permission(request.method, request.url.path, auth):
        return JSONResponse(None, 401, {"WWW-Authenticate": "Basic"})
    # 認証OKだったら、エンドポイントの処理を実行
    return await call_next(request)


@app.get("/test")
def test():
    return {"message": "Hello World"}


@app.get("/test2")
def test2():
    return {"message": "Hello World2"}


@app.get("/test3")
def test3():
    return {"message": "Hello World3"}
