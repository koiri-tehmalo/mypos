*** Settings ***
Resource    common_keywords.robot
Variables   ../../config.ini

*** Keywords ***
Return Product Full
    Load App Window    ${GLOBAL.WINDOW_TITLE}
    Click By Name    ${RETURN_PRODUCT.HOTKEY_E_TITLE}
    Type Keys    ${RETURN_PRODUCT.PRODUCT_CODE}{ENTER}
    Click By Name    ${RETURN_PRODUCT.REFUND_BUTTON_TITLE}
    Click By Id    ${RETURN_PRODUCT.REASON_COMBO_AUTO_ID}
    Type Keys    ${RETURN_PRODUCT.REASON_ITEM_TITLE}{ENTER}
    Click By Id    ${RETURN_PRODUCT.CONDITION_COMBO_AUTO_ID}
    Type Keys    ${RETURN_PRODUCT.CONDITION_ITEM_TITLE}{ENTER}
    Click By Id    ${RETURN_PRODUCT.SUBMIT_AUTO_ID}
    Click By Name    ${RETURN_PRODUCT.PAY_BUTTON_TITLE}
    Click By Name    ${RETURN_PRODUCT.CASH_BUTTON_TITLE}
    Click By Id    ${RETURN_PRODUCT.CONFIRM_OK_AUTO_ID}
    Click By Id    ${RETURN_PRODUCT.NEXT_AUTO_ID}
    Click By Id    ${GLOBAL.ABORT_PRINT_AUTO_ID}
