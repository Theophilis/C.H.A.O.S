set files=src\main.c 
set libs=C:\Users\edwar\.vscode\chaos\lib\SDL2main.lib C:\Users\edwar\.vscode\chaos\lib\SDL2.lib Ws2_32.lib 

CL /Zi /I C:\Users\edwar\.vscode\chaos\include %files% /link %libs% /OUT:chaos.exe