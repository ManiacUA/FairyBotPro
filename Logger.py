"""How to write logs for FairyBotPro.
What should be logged:
1) Start at the start of a function.
2) Finish at the end of function.
3) Result of any calculation/request.

Rules:
1) Logs initialisation should be first step of initialisation of module;
2) Entities should never be monitored;
"""

from collections import deque
import datetime
import Tool


class Logger:
    tab = "  "  # for saving space purpose tab is 2 spaces

    def __init__(self, module, account, show_logs=True, show_warnings=True):
        self.module = module
        self.show_logs = show_logs
        self.show_warnings = show_warnings
        self.email = account.email
        self.func = deque()
        self.log_func_start('__init__')

    def check_func(self):
        if not self.func:
            raise ValueError("Function value in logger is not set.")

    def log(self, text):
        if self.show_logs:
            self._message(text=text, pretext='...')

    def log_func_start(self, func):
        self.func.append(func)
        if self.show_logs:
            self.log("Started.")

    def log_func_finish(self):
        if self.show_logs:
            self.log("Finished.")
        self.func.pop()

    def warning(self, text):
        if self.show_warnings:
            self._message(text=text, pretext='!!!')

    def error(self, text):
        self._message(text=text, pretext='<ERROR>')
        raise ValueError(text)

    def _message(self, text, pretext=""):
        self.check_func()
        time_string = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        text = "{}{}[{}] {}{}({}): {}".format(pretext,
                                              time_string,
                                              self.email,
                                              (len(self.func)-1) * self.tab,
                                              self.module,
                                              self.func[len(self.func)-1],
                                              text)

        text = Tool.surrogate_decoding(text)
        print(text)
