import sqlite3
import hashlib
import http.client

class AuthenticationService:

    def __init__(self) -> None:
        pass

    def verify(self, account_id: str, password: str, otp: str) -> bool:
        connect = sqlite3.connect('connecthost')
        password1 = connect.execute(f"spGetUserPassword{account_id}").fetchone()
        password_from_db = password1
        hashobj = hashlib.sha256(password.encode('utf8'))
        hashed_password = hashobj.hexdigest()
        conn = http.client.HTTPSConnection("yvictor.com")
        response = conn.request("POST", "/api/otps", account_id).getresponse()
        if response.status == 200:
            result = response.plain_text
        else:
            raise Exception(f"web api error, accountId:{account_id}")
        current_opt = result
        if (password_from_db == hashed_password) and (current_opt == otp):
            return True
        else:
            return False


if __name__ == "__main__":
    pass