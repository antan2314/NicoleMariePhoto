import getpass
from email_validator import validate_email, EmailNotValidError
from db.session import Session
from db.adminTable import Admin
from db.auditTable import AuditLog, AuditEvent
from security.hashing import hash_password
from sqlalchemy import select

def get_admin_email():
    # Loops until the operator supplies the same valid address twice; any bad
    # or mismatched entry just restarts the prompt rather than aborting.
    while True:
        try:
            username = input("Enter admin email: ")
            result = validate_email(username,
                           check_deliverability=False)  # flag needs to be removed after development, for now having it False allows for testing without adding real domains. Once live, I want it to check for real domains
            username_check = input("Enter admin email again: ")
            result_check = validate_email(username_check, check_deliverability=False)

            # ValidatedEmail defines __eq__, so this compares the parsed
            # results rather than the raw strings - two spellings that
            # normalize to the same address count as a match.
            if result == result_check:
                print("Email matched")
                # Hand back the normalized form so what gets stored is
                # consistent with Admin.validate_email's own normalization.
                return result.normalized
            else:
                print("Email did not match, try again")
                continue

        except EmailNotValidError:
            print("Email not valid, try again")
            continue


def get_admin_pass():
    # Same confirm-twice loop as the email prompt. getpass keeps the typed
    # password off the screen and out of the terminal's history.
    while True:
        admin_pass = getpass.getpass("Enter admin password: ")
        admin_pass_check = getpass.getpass("Enter admin password again: ")

        if admin_pass_check == admin_pass:
            print("Password matched")
            return admin_pass
        else:
            print("Password did not match, try again")
            continue

def main():
    # Collects and confirms the two credentials. Nothing is written to the
    # database yet - the Session/Admin/AuditLog/hash_password imports above
    # are for the persistence step that still has to be added here.
    email = get_admin_email()
    password = get_admin_pass()


if __name__ == "__main__":
    main()
