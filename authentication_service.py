import sqlite3
import hashlib
import http.client
import logging


class FailedTooManyTimesException(Exception):
    pass


class AuthenticationService:

    def __init__(self) -> None:
        pass

    def verify(self, account_id: str, password: str, otp: str) -> bool:
        http_client = http.client.HTTPSConnection("yvictor.com")
        response = http_client.request("POST", "api/failedCounter/IsLocked", account_id)
        if response.plain_text == "true":
            raise FailedTooManyTimesException()

        connect = sqlite3.connect('connecthost')
        password1 = connect.execute(f"spGetUserPassword{account_id}").fetchone()
        password_from_db = password1
        hashobj = hashlib.sha256(password.encode('utf8'))
        hashed_password = hashobj.hexdigest()
        response = http_client.request("POST", "/api/otps", account_id).getresponse()
        if response.status == 200:
            result = response.plain_text
        else:
            raise Exception(f"web api error, accountId:{account_id}")
        current_opt = result
        if (password_from_db == hashed_password) and (current_opt == otp):
            http_client.request("POST", "api/failedCounter/Reset", account_id)
            return True
        else:
            http_client.request("POST", "api/failedCounter/Add", account_id)

            response = http_client.request("POST", "api/failedCounter/GetFailedCount", account_id)
            failed_count = int(response.plain_text)
            logger = logging.getLogger(__class__)
            logger.info(f"accountId:{account_id} failed times:{failed_count}")

            message = f"{account_id} try to login failed"
            slack_client = SlackClient('api token')
            slack_client.post_message("my channel", message, "my bot name")

            return False


if __name__ == "__main__":
    pass