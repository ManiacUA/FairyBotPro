import Tool
import datetime


class Logger:
    def __init__(self,module, additional_indent=0, show_logs=True):
        self.additional_indent = additional_indent
        self.module = module
        self.show_logs = show_logs

    def log(self, indent, place, text):
        Tool.Sprint(self._message(indent, place, text))

    def warning(self, indent, place, text):
        Tool.Sprint("!!! " + self._message(indent, place, text))

    def error(self, indent, place, text):
        Tool.Sprint("-->" + self._message(indent, place, text))
        exit()  # TODO: check if that thing will stop thread or whole script or probably just throw exception

    def _message(self, indent, place, text):
        time_string = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        whole_text = "{} | {}{}({}): {}".format(time_string, (
                self.additional_indent + indent) * "\t", self.module, place, text)
        return whole_text
