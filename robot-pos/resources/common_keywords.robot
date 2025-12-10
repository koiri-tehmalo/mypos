*** Settings ***
Library    RPA.Windows

*** Keywords ***
Load App Window
    [Arguments]    ${title}
    Wait For Window    ${title}    timeout=10
    ${win}=    Get Window    ${title}
    Set Global Variable    ${APP}    ${win}

Click By Id
    [Arguments]    ${id}
    Click Element    id:${id}

Click By Name
    [Arguments]    ${name}
    Click Element    name:${name}

Type Keys
    [Arguments]    ${text}
    Send Keys    ${APP}    ${text}
