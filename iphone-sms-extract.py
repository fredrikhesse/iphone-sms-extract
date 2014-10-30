import argparse
import os
import sqlite3


def export_messages(backup_directory, sms_file, output_file):
    with sqlite3.connect(os.path.join(os.path.expanduser(backup_directory), sms_file)) as conn:
        with open(output_file, "w") as json:
            json.write("{\n\t\"conversations\":[\n")
            chat_cursor = conn.cursor()
            chat_cursor.execute("SELECT ROWID as chat_id, chat_identifier FROM chat")
            for chat_id, chat_identifier in chat_cursor.fetchall():
                sender = str(chat_identifier)
                print "Exporting conversation with: {0}".format(sender)
                json.write("\t\t{{\n\t\t\t\"sender\":\"{0}\",\n\t\t\t\"messages\":[\n".format(sender))
                first_message = True
                chat_message_cursor = conn.cursor()
                chat_message_cursor.execute(
                    "SELECT chat_id as chat_chat_id, message_id as chat_message_id "
                    "FROM chat_message_join WHERE chat_id = :chat_id",
                    {"chat_id": chat_id})
                for chat_chat_id, chat_message_id in chat_message_cursor.fetchall():
                    if first_message is not True:
                        json.write(",\n")
                    first_message = False
                    message_cursor = conn.cursor()
                    message_cursor.execute(
                        "SELECT text as message_text, service as message_type, is_from_me as message_is_from_me, "
                        "datetime(date + strftime('%s', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') as "
                        "message_sentdate FROM message WHERE ROWID = :message_id",
                        {"message_id": chat_message_id})
                    for message_text, message_type, message_is_from_me, message_sentdate in message_cursor.fetchall():
                        json.write(
                            "\t\t\t\t{{\n\t\t\t\t\t\"text\":\"{0}\",\n\t\t\t\t\t\"fromMe\":\"{1}\",\n\t\t\t\t\t"
                            "\"type\":\"{2}\",\n\t\t\t\t\t\"received\":\"{3}\"\n\t\t\t\t}}".format(
                                str(message_text.encode('utf-8')), bool(message_is_from_me), message_type,
                                message_sentdate))
                json.write("\n\t\t\t]\n\t\t},\n")
            json.write("\t]\n}\n")


parser = argparse.ArgumentParser("Export iPhone text messages from backup.\n(Requires an unencrypted backup).")
parser.add_argument("--backupdirectory",
                    help="The location of your iPhone backup "
                         "(on OS X ~/Library/Application Support/MobileSync/Backup/<backupid>)")
parser.add_argument("--smsfile", default="3d0d7e5fb2ce288813306e4d4636395e047a3d28",
                    help="The name of the file containing the text messages. "
                         "(default: 3d0d7e5fb2ce288813306e4d4636395e047a3d28)")
parser.add_argument("--outputfile", default="messages.json", help="Outputfile (default: messages.json)")
args = parser.parse_args()

export_messages(args.backupdirectory, args.smsfile, args.outputfile)
