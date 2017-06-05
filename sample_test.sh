#!/bin/sh

if [ "$1" != "" ]; then
	echo "Positional parameter 1 contains something"
	exit
fi

python cuckoo.py submit $1/test_cpl.cpl
python cuckoo.py submit $1/test_jar.jar
python cuckoo.py submit $1/test_pdf.pdf
python cuckoo.py submit $1/test_php.php --package php
python cuckoo.py submit $1/test_python.py
python cuckoo.py submit $1/test_vbs.vbs
python cuckoo.py submit $1/test_excel.xlsx --timeout 30
python cuckoo.py submit $1/test_word.docx --timeout 30
python cuckoo.py submit $1/test_ppt.pptx --timeout 30
python cuckoo.py submit $1/test_zip.zip -o file=main.exe
python cuckoo.py submit $1/dll/libtest_dll.dll -o function=dll_entry,arguments="123 32"
python cuckoo.py submit $1/test_html.html

python cuckoo.py submit $1/DANGER/StuxNet_infected.zip -o password=infected,file=malware.exe
python cuckoo.py submit $1/DANGER/VirusShare_84c82835a5d21bbcf75a61706d8ab549_Wanncry_infected.zip -o password=infected

python cuckoo.py submit -u http://192.168.56.1:38080/
