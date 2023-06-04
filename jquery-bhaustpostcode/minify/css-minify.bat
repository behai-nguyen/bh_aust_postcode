@echo off

REM
REM 02/06/2023.
REM

echo jQuery plugin bhAustPostcode CSS minification: bh-aust-postcode.min.css.

C:\Users\behai\AppData\Roaming\npm\uglifycss ^
    D:\Codes\WebWork\bootstrap\dist\css\bootstrap.css ^
    D:\Codes\WebWork\bootstrap\icons-1.9.1\font\bootstrap-icons.css ^
    D:\Codes\WebWork\jquery-bhaustpostcode\src\bhAustPostcode.css ^
	--output D:\Codes\WebWork\jquery-bhaustpostcode\example\bh-aust-postcode.min.css