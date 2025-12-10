*** Settings ***
Resource    common_keywords.robot
Variables   ../../config.ini

*** Keywords ***
Open Retail
    Load App Window    ${GLOBAL.WINDOW_TITLE}

Retail Hotkey R
    Click By Id    ${RETAIL_SALES.HOTKEY_R_AUTO_ID}

Search Product Text
    Click By Id    ${TEST_1_SEARCH_BY_TEXT.SEARCH_AUTO_ID}
    Type Keys    ${TEST_1_SEARCH_BY_TEXT.SEARCH_KEYWORD}{ENTER}

Select Product
    Click By Id    ${RETAIL_SALES.PRODUCT_DETAIL_TITLE}

Retail Next
    Click By Id    ${RETAIL_SALES.NEXT_AUTO_ID}

Receive Payment
    Click By Name    ${RETAIL_SALES.RECEIVE_PAYMENT_TITLE}
