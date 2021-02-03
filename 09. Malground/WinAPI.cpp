#define _CRT_SECURE_NO_WARNINGS //strcpy 보안 경고로 인한 컴파일 에러 방지
#include <tchar.h>
#include <Windows.h>
#include <stdio.h>
#include <WinBase.h>
#include <WinInet.h>
#include <iostream>
#include <string>
#include <stdlib.h> //malloc, free 함수가 선언 되어 있음
#include <wchar.h>

#pragma comment(lib, "urlmon.lib")

void getComName()
{
	char comName[100];
	DWORD size = sizeof(comName);
	if (GetComputerName(comName, &size))
		printf("ComputerName : %s\n", comName);
}

void getCpuInfo()
{
	char cpuName[100];
	HKEY hKey;
	DWORD c_size = sizeof(cpuName);
	RegOpenKeyEx(HKEY_LOCAL_MACHINE, "Hardware\\Description\\System\\CentralProcessor\\0", 0, KEY_QUERY_VALUE, &hKey);
	RegQueryValueEx(hKey, "ProcessorNameString", NULL, NULL, (LPBYTE)cpuName, &c_size);
	RegCloseKey(hKey);

	printf("CPU Info : %s\n", cpuName);
}

void getOSinfo()
{
	char ProductName[100];
	DWORD c_size = 100;
	HKEY hKey;
	RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\", 0, KEY_QUERY_VALUE, &hKey);
	RegQueryValueEx(hKey, "ProductName", NULL, NULL, (LPBYTE)ProductName, &c_size);
	RegCloseKey(hKey);
	printf("OS Info : %s\n", ProductName);
}


char *getUserN()
{
	char userName[100];
	char *s1 = (char*)malloc(sizeof(char) * 64);
	unsigned long dwLength = 100;
	GetUserName(userName, &dwLength);
	strcpy(s1, userName);
	printf("User Name : %s\n", userName);
	system("C:\\Users\\RoyTravel\\Desktop\\test.txt");
	return s1;
}

void getSysInfo()
{
	SYSTEM_INFO *GetInfo;
	GetInfo = (SYSTEM_INFO*)malloc(sizeof(SYSTEM_INFO));
	GetSystemInfo(GetInfo);
	printf("CPU Core : %x개\n", GetInfo->dwNumberOfProcessors);
	free(GetInfo);
}

void getTime()
{
	SYSTEMTIME st;
	SYSTEMTIME lt;
	GetLocalTime(&st);
	GetSystemTime(&lt);
	printf("local Time : %d/%d/%d %d:%d:%d %d\n", lt.wYear, lt.wMonth, lt.wDay, lt.wHour, lt.wMinute, lt.wSecond, lt.wMilliseconds);
	printf("System Time : %d/%d/%d %d:%d:%d %d\n", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond, st.wMilliseconds);
}

void Download()
{
	char url[256];
	char name[256];
	char path[256];
	
	char userName[100];
	unsigned long dwLength = 100;
	GetUserName(userName, &dwLength);

	printf("URL : ");
	scanf_s("%s",url,sizeof(url));
	printf("FILENAME : ");
	scanf_s("%s", name, sizeof(name));
	sprintf(path, "C:\\Users\\%s\\Desktop\\%s",userName,name);
	URLDownloadToFile(NULL, url, path, 0, NULL);
}

BOOL SetStartProgram(LPCSTR lpPosition);


BOOL SetStartProgram(LPCSTR lpPosition)
{
	HKEY hKey;
	long error;

	error = RegOpenKeyEx(HKEY_LOCAL_MACHINE, TEXT("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"), 0L, KEY_WRITE, &hKey);

	if (error == ERROR_SUCCESS)
	{
		error = RegSetValueEx(hKey, TEXT("HELLO"), 0, REG_SZ, (BYTE*)lpPosition, lstrlen(lpPosition));
		RegCloseKey(hKey);
		printf("Hello");
		return true;
	}
	else if (error == ERROR_ACCESS_DENIED)
		printf("ERROR_ACCESS_DENIED\n");
	else
		printf("ERRORCODE : %ld\n", error);

	return false;
}

void alert()
{
	char message[256];
	scanf_s("%[^\n]", message, sizeof(message));
	HWND hWndConsole = GetConsoleWindow();
	ShowWindow(hWndConsole, SW_HIDE);
	MessageBox(NULL, message, "Alert", MB_OK);
}


int main(int argc, char** argv)
{

	//alert();
	getUserN();
	//SetStartProgram(argv[0]);
	//Download();
	//getComName();
	//getCpuInfo();
	//getSysInfo();
	//getTime();
	//getOSinfo();
	
	
}
