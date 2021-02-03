#include <Windows.h>
#include <iostream>
using namespace std;

typedef BOOL (WINAPI *P_GDFSE)(LPCTSTR, PULARGE_INTEGER, PULARGE_INTEGER, PULARGE_INTEGER);

int main(int argc, char* argv[])
{	
	const char* pszDrive = "C:";
	unsigned __int64 i64FreeBytesToCaller, i64TotalBytes, i64FreeBytes;

	P_GDFSE pGetDiskFreeSpaceEx = (P_GDFSE)GetProcAddress(GetModuleHandle("kernel32.dll"), "GetDiskFreeSpaceExA");
	
	BOOL fResult = pGetDiskFreeSpaceEx(pszDrive,
		(PULARGE_INTEGER)&i64FreeBytesToCaller,
		(PULARGE_INTEGER)&i64TotalBytes,
		(PULARGE_INTEGER)&i64FreeBytes);

	if (fResult != TRUE)
	{
		cout << "[!] ERROR : Colud not get free space for " << pszDrive << endl;
		exit(GetLastError());
	}

	unsigned __int64 UsedBytes = i64TotalBytes - i64FreeBytes;

	cout << pszDrive << endl;
	cout << "전체 용량 = " << i64TotalBytes / (1024 * 1024 * 1024) << "GB" << endl;
	cout << "남은 용량 = " << i64FreeBytes / (1024 * 1024 * 1024) << "GB" << endl;
	cout << "사용 용량 = " << UsedBytes / (1024 * 1024 * 1024) << "GB" << endl;

	return 0;
}
