iphone-sms-extract
==================

A simple python script that extracts text messages from an iPhone backup database.

Backup your iPhone using iTunes (make sure that the backup is not encrypted).

Then run the script, specifying the location of the backup database:
python iphone-sms-extract.py --backupdirectory <directory>

On OS/X the backups are located in:
~/Library/Application Support/MobileSyc/Backup
while on Windows the directory is:
%APPDATA%\Apple Computer\MobileSync\Backup

The result will be a json-file, sorted by conversations, formatted like:
{
	"conversations":[
		{
			"sender":"<sender phone>",
			"messages":[
				{
					"text":"<message>",
					"fromMe":"<True/False>",
					"type":"<SMS/iMessage>",
					"received":"<date>"
				}
			]
		}
	]
}
