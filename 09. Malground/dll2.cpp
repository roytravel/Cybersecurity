#include <Windows.h>
#include <iostream>
#include <conio.h>

#define DEF_DLL_NAME	"test.dll"
#define DEF_HOOKSTART	"HookStart"
#define DEF_HOOKSTOP	"HookStop"

typedef void(*PFN_HOOKSTART)();
typedef void(*PFN_HOOKSTOP)();
using namespace std;

void main(void)
{
	HMODULE hDll = NULL;
	PFN_HOOKSTART HookStart = NULL;
	PFN_HOOKSTOP HookStop = NULL;

	hDll = LoadLibraryA(DEF_DLL_NAME);
	if (hDll == NULL)
	{
		cout << GetLastError() << endl;
		return;
	}

	HookStart = (PFN_HOOKSTART)GetProcAddress(hDll, DEF_HOOKSTART);
	HookStop = (PFN_HOOKSTOP)GetProcAddress(hDll, DEF_HOOKSTOP);

	HookStart();

	cout << "Input 'q' if you want to quit" << endl;
	while (_getch() != 'q');

	HookStop();
	FreeLibrary(hDll);
}
