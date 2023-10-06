from robot.libraries.BuiltIn import BuiltIn


def beni_cagir(mesaj):
    msg = '\nBeni çağırdığına sevindim\n'
    print(msg+mesaj)
    BuiltIn().log_to_console(msg+mesaj)
    return "Oldu mu?"
