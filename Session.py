# defines Session class
# class holds login functionality and methods

class Session:
    def __init__(self):
        self.eid = ""           # populate during login
        self.emp_name = ""      # populate during login
        self.cash_start = 500   # cash at session login
        self.cash_final = 500   # cash at session end
        self.session_start = "" # time of session start
        self.session_end = ""   # time of session end
        self.security_level = -1    # assign based on who is logged in

    def session_start(self):
        pass
        # login window stuff
        # should set eid, emp_name, session_start, security level

    def set_cash_final(self, amount):
        self.cash_final = amount

    def session_end(self):
        pass
        # logout procedures
        # should set cash_final and session_end
