class Security(object):
    """description of class"""
    def __init__(self):
        return

    def check(self, handbags):
        if "gun" in handbags or "drugs" in handbags:
            print("Security failed.")
            return False
        print("Security passed.")
        return True