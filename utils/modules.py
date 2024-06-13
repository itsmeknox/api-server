import json
import requests
import tls_client

from colorama import Style, Fore
from datetime import datetime
import tls_client.response
from typing_extensions import Literal, Union





class Logging:
    def __init__(self, debug_level: Literal[False, 'BASIC', 'ADVANCED']="ADVANCED", max_message_length: Union[bool, int] = None, max_log_message: int = None) -> None:
        self.debug_level = debug_level
        self.max_message_length = max_message_length
        self.max_log_message = max_log_message

        self.logged_messages = []
        self.disabled = False

    def disable_logging(self):
        self.disabled = True
    
    def enable_logging(self):
        self.disabled = False

    def load(self):
        message = "\n".join(self.logged_messages)
        print(message)

    def __printable_token(self, token: str) -> str:
        if len(token) > 10:
            return token[:10]
        else:
            return token

    def __process_output(self, message: str):
        if not self.disabled:
            print(message)

        if self.max_log_message:
            self.logged_messages.append(message)
            if len(self.logged_messages) > self.max_log_message:
                self.logged_messages = self.logged_messages[-self.max_log_message:]

    def __format_message(self, message: str, max_length: int = 30) -> str:
        if not max_length:
            return message
        max_length = max_length - 1

        if len(message) <= max_length:
            spaces = max_length - len(message)
            formatted_message = f"{message}{' ' * spaces}"
        else:
            formatted_message = message[:max_length]
        return formatted_message
    
    def __process_kwargs(self, **kwargs) -> str:
        string = ""
        for key, value in kwargs.items():
            if key == "token":
                value = self.__printable_token(value)
            string += f'{Fore.LIGHTBLACK_EX}{key}{Fore.WHITE}="{value}" '

        return string

    def info(self, message: str, **kwargs):
        message = self.__format_message(message, max_length=self.max_message_length)
        options = self.__process_kwargs(**kwargs)

        self.__process_output(f'{Fore.LIGHTBLACK_EX}{Style.BRIGHT}[{datetime.now().strftime("%H:%M:%S")}] {Fore.GREEN}✅ INFO  {Fore.LIGHTBLACK_EX}: {Fore.GREEN}{message} {Fore.LIGHTWHITE_EX}{f"-> {options}" if options else ""}{Style.RESET_ALL}')

    def error(self, message: str, **kwargs):
        message = self.__format_message(message, max_length=self.max_message_length)
        options = self.__process_kwargs(**kwargs)

        self.__process_output(f'{Fore.LIGHTBLACK_EX}{Style.BRIGHT}[{datetime.now().strftime("%H:%M:%S")}] {Fore.RED}❌ ERROR {Fore.LIGHTBLACK_EX}: {Fore.RED}{message} {Fore.WHITE}{f"-> {options}" if options else ""}{Style.RESET_ALL}')

    def debug(self, message: str, **kwargs):
        message = self.__format_message(message, max_length=self.max_message_length)
        options = self.__process_kwargs(**kwargs)

        self.__process_output(f'{Fore.LIGHTBLACK_EX}{Style.BRIGHT}[{datetime.now().strftime("%H:%M:%S")}] {Fore.YELLOW}🔍 DEBUG {Fore.LIGHTBLACK_EX}: {Fore.YELLOW}{message} {Fore.WHITE}{f"-> {options}" if options else ""}{Style.RESET_ALL}')

    def warn(self, message: str, **kwargs):
        message = self.__format_message(message, max_length=self.max_message_length)
        options = self.__process_kwargs(**kwargs)

        self.__process_output(f'{Fore.LIGHTBLACK_EX}{Style.BRIGHT}[{datetime.now().strftime("%H:%M:%S")}] {Fore.LIGHTCYAN_EX}⛔ WARN  {Fore.LIGHTBLACK_EX}: {Fore.LIGHTCYAN_EX}{message} {Fore.LIGHTWHITE_EX}{f"-> {options}" if options else ""}{Style.RESET_ALL}')

    def debug_response(self, message: str, response: Union[requests.Response, 'tls_client.response.Response'], **kwargs):
        if self.debug_level != "ADVANCED":
            return
        
        try:
            response_text = response.text
            response_json = json.dumps(json.loads(response_text), indent=2)
        except json.JSONDecodeError:
            response_json = response_text

        self.debug_log(message=message, response=response_json, **kwargs)
