from sender import hideFunc
from receiver import revealFunc

def hide(sec_msg,password,cvr_msg):
    result = hideFunc(sec_msg, password, cvr_msg)
    print("Result:", result)


def decode():
        steg_msg = input("Enter steganographic message: ")
        psw_rev = input("Enter password: ")
        result_reveal = revealFunc(steg_msg, psw_rev)
        print("Result:", result_reveal)

hide()