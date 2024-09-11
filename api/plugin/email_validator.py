class EmailValidator:
    def run(self, email):
        if '@' not in email:
            raise ValueError("Invalid email address.")
        return email

# Ensure that this is the module's entry point
def get_plugin():
    return EmailValidator()
