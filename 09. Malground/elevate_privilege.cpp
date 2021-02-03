#include <Windows.h>
#include <iostream>
using namespace std;

// https://ghostshell.tistory.com/30

void enable_system_priv(void)
{
	HANDLE hToken;
	LUID luidDebug;
	TOKEN_PRIVILEGES tp;

	if (!OpenProcessToken(GetCurrentProcess(),
		TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
		return;

	if (!LookupPrivilegeValue(NULL, SE_DEBUG_NAME, &luidDebug))
	{
		CloseHandle(hToken);
		return;
	}

	tp.PrivilegeCount = 1;
	tp.Privileges[0].Luid = luidDebug;
	tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;


	if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(tp), NULL, NULL))
	{
		cout << "Adjust Error " << GetLastError() << endl;
		CloseHandle(hToken);
	}

	CloseHandle(hToken);

}

int main(void)
{
	enable_system_priv();
	return 0;
}
