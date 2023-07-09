import sys

def error_message(error, detail:sys): 
    _,_,exc_tb = detail.exc_info() #this brings the info about the most recent exception in a tuple (exc_type, exc_value, exc_traceback. the traceback is the only thing we need right now)
    file_name = exc_tb.tb_frame.f_code.co_filename #tb_frame represent the frame at the time of the exception, aand the co_filename gets the name of the file name where the most recent exception occcured
    line_number = exc_tb.tb_lineno

    error_message = f"error occured in the script name [{file_name}] line number [{line_number}] error message [{str(error)}]"

    return error_message


class CustomException(Exception):
    def __init__(self, error_message, detail:sys):
        super.__init__(error_message)
        self.error_message = error_message(error_message, detail = detail)

    def __str__(self):
        return self.error_message