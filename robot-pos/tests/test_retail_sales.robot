*** Settings ***
Resource    ../resources/retail_sales_keywords.robot

*** Test Cases ***
Retail Sales Basic
    Open Retail
    Retail Hotkey R
    Search Product Text
    Select Product
    Retail Next
    Receive Payment
