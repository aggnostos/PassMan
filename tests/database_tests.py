import unittest
from passman import get_urls_and_passwords, get_table_names, parse_config, encrypt_password, connect, add_item, get_item, get_all_items, delete_item, update_url, update_login, update_password, create_vault, delete_vault

settings = parse_config()
db_host, db_name, db_user = settings[::]

master_password = "MyMasterPassword"
salt = b"mysalt"
url = "google.com"
login = "mylogin"
password = "mypassword"

conn = connect(db_host, db_name, db_user, master_password)

table_names = get_table_names(conn)

class DataBaseTest(unittest.TestCase):
    def test_get_and_add_item(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        self.assertEqual(get_item(conn, url, salt, master_password, urls), "URL: google.com, login: mylogin, password: mypassword")
        delete_item(conn, url, urls)

    def test_get_all_items(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        self.assertEqual(get_all_items(conn, salt, master_password), "URL: google.com, login: mylogin, password: mypassword")
        delete_item(conn, url, urls)

    def test_delete_item(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        delete_item(conn, url, urls)
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        self.assertEqual(get_item(conn, url, salt, master_password, urls), "[INFO] No such url in vault")

    def test_update_url(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        update_url(conn, 'gmail.com', url, urls)
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        self.assertEqual(get_item(conn, 'gmail.com', salt, master_password, urls), "URL: gmail.com, login: mylogin, password: mypassword")
        delete_item(conn, 'gmail.com', urls)

    def test_update_login(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        update_login(conn, url, 'mynewlogin', urls)
        self.assertEqual(get_item(conn, url, salt, master_password, urls), "URL: google.com, login: mynewlogin, password: mypassword")
        delete_item(conn, url, urls)

    def test_update_passsword(self):
        add_item(conn, url, login, encrypt_password(salt, password, master_password))
        urls = [url for url in get_urls_and_passwords(conn, salt, master_password).keys()]
        update_password(conn, url, encrypt_password(salt, 'mynewpassword', master_password), urls)
        self.assertEqual(get_item(conn, url, salt, master_password, urls), "URL: google.com, login: mylogin, password: mynewpassword")
        delete_item(conn, url, urls)


if __name__=='__main__':
    unittest.main()