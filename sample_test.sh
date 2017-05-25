#!/bin/sh

$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_cpl.cpl
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_jar.jar
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_pdf.pdf
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_php.php --package php
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_python.py
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_vbs.vbs
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_excel.xlsx --timeout 30
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_word.docx --timeout 30
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_ppt.pptx --timeout 30
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_zip.zip -o file=main.exe
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/dll/libtest_dll.dll -o function=dll_entry,arguments="123 32"
$PY cuckoo.py submit $CUCKOO_TEST_SAMPLE_DIR/test_html.html


$PY cuckoo.py submit -u http://192.168.56.1:38080/
