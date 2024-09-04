import time
from email.header import decode_header
from email import message_from_bytes
import imaplib
import os


def ready_mail():
    with open('emails_check/emails.txt', 'r', encoding="utf-8") as file:
        return file.read().split("\n")


def get_first_message(email, email_password):
    print(email, email_password)
    time.sleep(2)
    path_delete = 'emails_check/emails.txt'
    path_add = 'txt/ready_emails.txt'
    try:
        imap_server = 'imap.rambler.ru'

        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email, email_password)

        inbox = imap.select("inbox")  # ('OK', [b'3'])
        search = imap.search(None, 'ALL')  # ('OK', [b'1 2 3'])
        # print("search: ", search)
        string = search[1][0].decode("utf-8")
        list_ids_inbox = [int(x) for x in string.split()]
        last_mess = list_ids_inbox[len(list_ids_inbox) - 1]
        iteration = bytes(str(last_mess), encoding="utf-8")

        res, msg = imap.fetch(iteration, '(RFC822)')

        msg = message_from_bytes(msg[0][1])
        decoded_subj = decode_header(msg["Subject"])[0][0].decode()  # получение первого месседжа
        print(f"✅ Сообщение получено! {decoded_subj}")
        pochta = True
        editted = open(path_add, 'a')
        editted.writelines(email + ':' + email_password + '\n')
        editted.close()
        return str(decoded_subj)
    except AttributeError:
        try:
            msg = message_from_bytes(msg[0][1])
            print(f"✅ Сообщение получено! {msg}")
            pochta = True
            editted = open(path_add, 'a')
            editted.write(email + ':' + email_password)
            editted.close()
        except Exception as err:
            print(f"Не удалось получить сообщение: {err}")
            pochta = False
            orig = open(path_delete, 'r')
            L = orig.readlines()
            k = 0
            while k < len(L) - 1:
                L[k] = L[k + 1]
                k = k + 1
            L = L[:-1]  # убираем почту
            orig.close()
        time.sleep(3)
    finally:
        if pochta:
            orig = open(path_delete, 'r')
            L = orig.readlines()
            k = 0
            while k < len(L) - 1:
                L[k] = L[k + 1]
                k = k + 1
            L = L[:-1]  # убираем почту
            orig.close()
        else:
            orig = open(path_delete, 'r')
            L = orig.readlines()
            k = 0
            while k < len(L) - 1:
                L[k] = L[k + 1]
                k = k + 1
            L = L[:-1]  # убираем почту
            orig.close()
        path = 'emails_check/emails.txt'
        new = open('txt/cut_tmp.txt', 'w')
        for line in L:
            new.write(line)
        new.close()
        os.remove(path)
        os.rename('txt/cut_tmp.txt', path)


emails = ready_mail()

for j in range(len(emails)):
    get_first_message(email=emails[j].split(':')[0], email_password=emails[j].split(':')[1])
