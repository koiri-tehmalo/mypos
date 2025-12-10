*** Settings ***
Resource    ../resources/payment_keywords.robot

*** Test Cases ***
Test Payment Cash
    Payment Cash

Test Payment Exact
    Payment Exact

Test Payment QR
    Payment QR

Test Payment Check
    Payment Check

Test Payment Credit
    Payment Credit

Test Payment Debit
    Payment Debit

Test Payment Alipay
    Payment Alipay

Test Payment Wechat
    Payment Wechat

Test Payment THP
    Payment THP

Test Payment QR Credit
    Payment QRCredit

Test Payment TrueMoney
    Payment TrueMoney
