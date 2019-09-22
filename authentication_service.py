import sqlite3
import hashlib
import http.client

class AuthenticationService:

    def __init__(self) -> None:
        pass

    def verify(self, account: str, password: str, otp: str) -> bool:

        raise NotImplementedError()


def get_password(account_id: str) -> str:
    connect = sqlite3.connect('connecthost')
    password = connect.execute("spGetUserPassword").fetchone()
    return password

def get_hash(plain_text: str) -> str:
    hashobj = hashlib.sha256(plain_text.encode('utf8'))
    return hashobj.hexdigest()

def get_otp(account_id: str) -> str:
    conn = http.client.HTTPSConnection("yvictor.com")
    response = conn.request("POST", "/api/otps", account_id).getresponse()
    if response.status == 200:
        return response.plain_text
    else:
        raise Exception(f"web api error, accountId:{account_id}")