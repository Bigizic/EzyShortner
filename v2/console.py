#!/usr/bin/env python3
"""Admin Console using cmd
"""

import bcrypt
import cmd
import pyotp


def console_pwd(pwd: str) -> bool:
    """Confirms if entered password matches console pwd
    """
    hashed = b'$2b$12$OHXRZbf5.2WsSeEUFQmQLuG71EYNufwJDd2521eNA5Y/88S/b8Q7u'
    return bcrypt.checkpw(pwd.encode(), hashed)


class AdminCommand(cmd.Cmd):
    """Representation of admin console
    """
    prompt = "(Admin): "

    def do_quit(self, arg: str) -> bool:
        """Quit is command to exit the program"""
        print("BYE")
        return True

    def do_EOF(self, arg: str) -> bool:
        """EOF is command to exit the program"""
        return True

    def emptyline(self):
        """shouldn't execute anything"""
        pass

    def do_create(self, arg: str):
        """Usage:
        Create ADMIN {full_name} {password} {username}
        """
        args = arg.split(' ')
        if args[0].lower() == 'admin':
            cpwd = input("Enter password, click anything to skip: ")
            check_pwd = console_pwd(cpwd)

            from admin.model.admin_model import Admin
            from models import storage_type as st

            if len(args) == 4:
                admin_exists = st.check_admin(args[3])
                if not admin_exists:
                    ad = Admin()
                    ad.username = args[3]
                    ad.password = args[2]
                    ad.full_name = args[1]
                    ad.two_factor = pyotp.random_base32()
                    ad.login_time = 'NULL'
                    if check_pwd:
                        ad.rights = 'GET DELETE EDIT CREATE'
                    ad.save()
                    print(f"\nYour two factor code is: {ad.two_factor} Save it\nCreated!!")
                    return self.do_quit(None)
                else:
                    print("ADMIN EXISTS TRY AGAIN!!")
                    return self.do_quit(None)
            else:
                print("Usage: {create} {ADMIN} {full_name} {password} {username}")
        else:
            print("Usage {CREATE} {ADMIN}")
            return self.do_quit(None)


if __name__ == '__main__':
    AdminCommand().cmdloop()
