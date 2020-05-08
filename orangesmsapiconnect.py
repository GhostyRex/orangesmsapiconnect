import requests


# The the access token required to send a text message.
class CreateToken:

    # Get access token.
    @classmethod
    def get_access_token(cls, authorization_header):
        # Take the authorization header of your app and returns the access token.
        headers = {
            "Authorization": authorization_header
        }

        # NB: Normal dictionary data like the one below, use data variable parameter and not json.
        data = {
            'grant_type': 'client_credentials'
        }

        response = requests.post(
            'https://api.orange.com/oauth/v2/token',
            headers=headers,
            data=data
        )

        # Print out the status code.
        # Rename the gotten access token from tk to something else
        access_token = response.json()['access_token']
        access_token_expiration = float(response.json()['expires_in'])
        print('ACCESS TOKEN: {}'.format(access_token))
        print('EXPIRES IN: {} days'.format(access_token_expiration / 86400))
        return access_token


# TODO: simpleorangesmsapiconnect.
# TODO: You can change the below class to sms. sms can send messages, can get info on messages.

# This class sends a single message to a single number.
class Sms:

    @classmethod
    def send_message(cls, access_token, sender, receiver, message):
        # Form the header.
        authorization_header = {
            'Authorization': 'Bearer ' + access_token,
            'Content-type': 'application/json'
        }

        # put the data in a json format.
        data = {
            "outboundSMSMessageRequest":
                {
                    # "address": "tel:+237652195180",
                    "address": "tel:+" + str(receiver),
                    "senderAddress": "tel:+" + str(sender),
                    "outboundSMSTextMessage":
                        {
                            "message": "{}".format(message)
                        }
                }
        }

        # Send the post request.
        response = requests.post(
            'https://api.orange.com/smsmessaging/v1/outbound/tel:+237656726914/requests',
            headers=authorization_header,
            json=data
        )

        # TODO: IF THE ERROR CODE IS NOT BTW 200 AND 201, THEN THE MESSAGE HAS NOT BEEN SENT OR
        #  ALWAYS CHECK THE SMS COUNT AFTER EVERY MESSAGE HAS BEEN SENT TO SEE IF LESS THAN AND DECREMENT.
        # print(r.text)
        if response.status_code == 201 or response.status_code == 200:
            return True
        else:
            print(response.json())
            return False


class AuthorizationHeader:
    """Class takes in an authorization token and returns the header"""

    def __init__(self, access_token):
        self.params = {
            'Authorization': 'Bearer ' + access_token,
            'Content-type': 'application/json'
        }

    def get_header(self):
        return self.params


# TODO: Another class is api app data. Get app balances, app usage statistics, purchase history etc.
class App:
    """This class returns the usage statistic of your app"""

    @classmethod
    def get_balance(cls, params):
        response = requests.get(
            "https://api.orange.com/sms/admin/v1/contracts",
            headers=params
        )

        remaining_sms_number = response.json()["partnerContracts"]["contracts"][0]["serviceContracts"][0][
            "availableUnits"]
        sms_expiration_date = ' '.join(
            response.json()["partnerContracts"]["contracts"][0]["serviceContracts"][0]["expires"].split('T'))

        # print('[INFO] NUMBER OF REMAINING SMS: {}'.format(remaining_sms_number))
        # print('[INFO] SMS EXPIRATION DATE: {}'.format(sms_expiration_date))

        return {'sms': remaining_sms_number, 'expires': sms_expiration_date}

    @classmethod
    def usage_statistics(cls, params):
        response = requests.get(
            "https://api.orange.com/sms/admin/v1/statistics",
            headers=params
        )
        return response.json()

    # Retrieves the purchase history of your api bundles.
    @classmethod
    def get_purchase_history(cls, params):
        response = requests.get(
            "https://api.orange.com/sms/admin/v1/purchaseorders",
            headers=params
        )
        return response.json()


# Takes in an error and returns a dictionary of the error and a string explanation.
class Error:
    # Class has one function which returns a json of the error code and meaning.

    @classmethod
    def error(cls, code):
        # ERROR CODES.
        # Informational responses (100–199),
        # Successful responses (200–299),
        # Redirects (300–399),
        # Client errors (400–499),
        # and Server errors (500–599).
        http_error_codes = {
            '200': 'SUCCESS OK!',
            '201': 'RESPONSE RECEIVED',
            '301': 'URL MOVED PERMANENTLY',
            '302': 'CHANGED TEMPORALLY',
            '400': 'BAD REQUEST',  # SERVER COULD NOT UNDERSTAND YOUR REQUEST.
            '401': 'UNAUTHORIZED',
            '403': 'FORBIDDEN',
            '404': 'NOT FOUND',
            '500': 'INTERNAL SERVER ERROR',
            '501': 'NOT SUPPORTED METHOD',
            '502': 'BAD GATEWAY',
            '503': 'SERVICE UNAVAILABLE'
        }
        try:
            return {str(code): http_error_codes[str(code)]}
        except KeyError:
            return {'error': 'None Existence Code..Please check orange api error code manual'}


# Remove the below when continuing the django part.
if __name__ == '__main__':
    # Get the token so as to access the ability to send text. Use token.
    token = CreateToken.get_access_token(authorization_header='tokenizer')
    Sms.send_message(access_token=token, sender='237652195180', receiver='237652195180', message='Hello there')
    header = AuthorizationHeader(access_token='token here')
    App.get_balance(header)
    App.usage_statistics(header)
    Error.error(200)
