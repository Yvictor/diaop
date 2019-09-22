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
        is_locked = self.get_is_locked(account_id, http_client)
        if is_locked:
            raise FailedTooManyTimesException()

        password_from_db = self.get_password_from_db(account_id)
        hashed_password = self.get_hashed_password(password)
        current_opt = self.get_current_otp(account_id, http_client)
        if (password_from_db == hashed_password) and (current_opt == otp):
            self.reset_failed_count(account_id, http_client)
            return True
        else:
            self.add_failed_count(account_id, http_client)

            self.log_failed_count(account_id, http_client)

            self.notify(account_id)

            return False

    def reset_failed_count(self, account_id, http_client):
        http_client.request("POST", "api/failedCounter/Reset", account_id)

    def get_is_locked(self, account_id, http_client):
        response = http_client.request("POST", "api/failedCounter/IsLocked", account_id)
        is_locked = response.plain_text == "true"
        return is_locked

    def notify(self, account_id):
        message = f"{account_id} try to login failed"
        slack_client = SlackClient('api token')
        slack_client.post_message("my channel", message, "my bot name")

    def log_failed_count(self, account_id, http_client):
        failed_count = self.get_failed_count(account_id, http_client)
        logger = logging.getLogger(__class__)
        logger.info(f"accountId:{account_id} failed times:{failed_count}")

    def get_failed_count(self, account_id, http_client):
        response = http_client.request("POST", "api/failedCounter/GetFailedCount", account_id)
        failed_count = int(response.plain_text)
        return failed_count

    def add_failed_count(self, account_id, http_client):
        http_client.request("POST", "api/failedCounter/Add", account_id)

    def get_current_otp(self, account_id, http_client):
        response = http_client.request("POST", "/api/otps", account_id).getresponse()
        if response.status != 200:
            raise Exception(f"web api error, accountId:{account_id}")
        current_opt = response.plain_text
        return current_opt

    def get_hashed_password(self, password: str) -> str:
        hashobj = hashlib.sha256(password.encode('utf8'))
        hashed_password = hashobj.hexdigest()
        return hashed_password

    def get_password_from_db(self, account_id: str) -> str:
        connect = sqlite3.connect('connecthost')
        password_from_db = connect.execute(f"spGetUserPassword{account_id}").fetchone()
        return password_from_db


if __name__ == "__main__":
    pass