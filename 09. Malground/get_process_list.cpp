#include <Windows.h>
#include <TlHelp32.h> //CreateToolSnapshot32
#include <iostream>
using namespace std;

void get_process_list()
{
	HANDLE hProcess = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	PROCESSENTRY32 pe32;
	BOOL bProcessFound;
	pe32.dwSize = sizeof(PROCESSENTRY32);
	bProcessFound = Process32First(hProcess, &pe32);

	while (bProcessFound){
		cout << "[+] " << pe32.th32ProcessID << " : " << pe32.szExeFile << endl;
		bProcessFound = Process32Next(hProcess, &pe32);
	}

	CloseHandle(hProcess);

}


int main(int argc, char* argv[])
{
	get_process_list();
	return 0;
}
