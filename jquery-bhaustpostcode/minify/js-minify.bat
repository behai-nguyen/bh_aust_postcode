@echo off

REM
REM 02/06/2023.
REM

echo jQuery plugin bhAustPostcode JS minification: bh-aust-postcode.min.js.

C:\Users\behai\AppData\Roaming\npm\uglifyjs ^
    D:\Codes\WebWork\jquery\js\jquery-3.6.0.js ^
    D:\Codes\WebWork\bootstrap\dist\js\bootstrap.bundle.js ^
    D:\Codes\WebWork\js\delay_callback_func.js ^
    D:\Codes\WebWork\js\css_funcs.js ^
    D:\Codes\WebWork\js\content_types.js ^
    D:\Codes\WebWork\js\http_status.js ^
    D:\Codes\WebWork\js\ajax_funcs.js ^
    D:\Codes\WebWork\js\elem_height_funcs.js ^
    D:\Codes\WebWork\js\bootstrap_funcs.js ^
    D:\Codes\WebWork\js\drags.js ^
    D:\Codes\WebWork\js\bootstrap_dialogs.js ^
    D:\Codes\WebWork\jquery-bhaustpostcode\src\bhAustPostcode.js ^
    --output D:\Codes\WebWork\jquery-bhaustpostcode\example\bh-aust-postcode.min.js	