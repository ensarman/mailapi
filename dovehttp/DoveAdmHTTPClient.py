""" HTTP Client library for Dovecot Doveadm HTTP API.
More details of the API itself can be found from:
http://wiki2.dovecot.org/Design/DoveadmProtocol/HTTP

Thanks to https://github.com/hnsk/doveadm-http-cli
"""

from base64 import b64encode
import requests


class DoveAdmHTTPClient(object):
    """ Client for accessing Dovecot Doveadm HTTP API """

    def __init__(self, apiurl=None, apikey=None, user="doveadm", password=None, sufix=""):
        """Constructor

        Args:
            apiurl (str, optional): the url of dovecot api. Defaults to None.
            apikey ('str', optional): the api key from dovecot . Defaults to None.
            user (str, optional): the username from dovecot. Defaults to "doveadm".
            password (str, optional): the password from dovecot. Defaults to None.
            sufix (str, optional): an optional sufix, . Defaults to "".
        """
        self.user = user
        self.password = password
        self.apiurl = apiurl
        self.apikey = apikey
        self.sufix = sufix
        self.commands = {}
        self.errors = {
            64: 'Incorrect parameters',
            65: 'Data error',
            67: 'User does not exist in userdb',
            68: 'Not found',
            73: 'Cannot create file, user out of quota',
            77: 'Authentication failure / permission denied',
            78: 'Invalid configuration'
        }
        self.reqs = requests.Session()
        if self.password:
            self.reqs.auth = (self.user, self.password)
        if self.apikey:
            self.reqs.headers.update({'Authorization': 'X-Dovecot-API ' + b64encode(self.apikey)})

    def get_commands(self):
        """ Retrieve list of available commands and their parameters from API """
        try:
            req = self.reqs.get(self.apiurl)
        except requests.exceptions.ConnectionError:
            return [["error", {"type": "connectionError"}, self.sufix]]

        if req.status_code == 200:
            commands = req.json()
            for command in commands:
                self.commands[command['command']] = {}
                for param in command['parameters']:
                    self.commands[command['command']][param['name']] = param['type']
            return req.text()
        else:
            return [["error", {"type": "httpError", "httpError": req.status_code}, self.sufix]]

    def run_command(self, command, parameters):
        """ Run any command with parameters """
        try:
            response = self.reqs.post(self.apiurl, json=[[command, parameters, self.sufix]])
            if response.status_code == 200:
                return response.json()
            return [["error", {"type": "httpError", "httpError": response.status_code}, self.sufix]]
        except requests.exceptions.ConnectionError:
            return [["error", {"type": "fatalError"}, self.sufix]]

    def is_error(self, response):
        return response[0][0] == 'error'

    def parse_error(self, response):
        """get the error description from the dovecot response error exitCode"""

        if response[0][0] == 'error' and response[0][0]['type'] == 'exitCode':
            return self.errors.get(
                response[0][1]['exitCode'],
                default=f"Error not listed: {response[0][1]['exitCode']}"
            )
        else:
            return "Not an error"

    def get_quota(self, user, key=None, key_type='STORAGE'):
        """gets any quota value from the given key and type

        Args:
            user ([type]): an username on the mail database
            key ([type]): ['value', 'limit', 'percent']
            key_type (str, optional): 'STORAGE', 'MESSAGE'. Defaults to 'STORAGE'.

        Returns:
            str: the spected value or an error description
            dict: all user quota data if no key is specified
        """

        keys = ['value', 'limit', 'percent']
        types = {
            'STORAGE': 0,
            'MESSAGE': 1
        }
        try:
            response = self.reqs.post(
                self.apiurl,
                json=[["quotaGet", {'user': user}, self.sufix]]
            )
            if response.status_code == 200:
                if self.is_error(response):
                    return self.parse_error(response)
                else:
                    if key:
                        if key in keys and key_type in types:
                            return response.json()[0][1][types.get(key_type)][key]
                        else:
                            return 'invalid key or type'
                    else:
                        if key_type in types:
                            return response.json()[0][1][types.get(key_type)]
                        else:
                            return 'invalid type'
            else:
                return f"Status Code not 200: {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Conection Error"
