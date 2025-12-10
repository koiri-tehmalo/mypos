*** Settings ***
Resource    common_keywords.robot
Variables   ../../config.ini

*** Keywords ***
Payment Cash
    Click By Name    ${PAYMENT.CASH_TITLE}
    Type Keys    ${PAYMENT.CASH_AMOUNT}{ENTER}
    Click By Id    ${RETAIL_SALES.NEXT_AUTO_ID}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Exact
    Click By Name    ${PAYMENT.PAYMENT_FAST}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment QR
    Click By Name    ${PAYMENT.QR_CODE_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Check
    Click By Name    ${PAYMENT.CHECK_TITLE}
    Type Keys    ${PAYMENT.NUMBER_P}{TAB}
    Type Keys    ${PAYMENT.NUMBER_C}{TAB}
    Type Keys    ${PAYMENT.DATE_C}{TAB}
    Click By Id    ${RETAIL_SALES.NEXT_AUTO_ID}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Credit
    Click By Name    ${PAYMENT.CREDIT_CARD_TITLE}
    Type Keys    ${PAYMENT.CREDIT_CARD_AMOUNT}{ENTER}
    Click By Id    ${RETAIL_SALES.NEXT_AUTO_ID}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Debit
    Click By Name    ${PAYMENT.DEBIT_CARD_TITLE}
    Click By Id    ${RETAIL_SALES.NEXT_AUTO_ID}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Alipay
    Click By Name    ${PAYMENT.ALIPYAY_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment Wechat
    Click By Name    ${PAYMENT.WECHAT_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment THP
    Click By Name    ${PAYMENT.THP_PEYMENT_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment QRCredit
    Click By Name    ${PAYMENT.QR_CREDIT_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}

Payment TrueMoney
    Click By Name    ${PAYMENT.TRUEMANEY_TITLE}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}
