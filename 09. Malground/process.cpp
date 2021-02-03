#include <Windows.h>
#include <TlHelp32.h>
#include <iostream>
using namespace std;

class Process
{
	private:
		// 현재 프로세스 전체 목록을 스냅샷
		HANDLE hProcess = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, FALSE);

		// 프로세스 정보 저장 구조체 생성
		PROCESSENTRY32 pe32;
		BOOL bProcessFound;
		
	public:
		void get_process_list()
		{
			pe32.dwSize = sizeof(PROCESSENTRY32);
			bProcessFound = Process32First(hProcess, &pe32);

			while (bProcessFound) 
			{
				cout << "[+] " << pe32.th32ProcessID << " : " << pe32.szExeFile << endl;
				bProcessFound = Process32Next(hProcess, &pe32);
			}

			CloseHandle(hProcess);
		}

		void find_process()
		{
			pe32.dwSize = sizeof(PROCESSENTRY32);
			bProcessFound = Process32First(hProcess, &pe32);

			while (bProcessFound)
			{
				HANDLE handle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pe32.th32ProcessID);

				if (strcmp(pe32.szExeFile, "winlogon.exe") == FALSE)
				{
					cout << "[!] Process ID : " << pe32.th32ProcessID << endl;
					cout << "[!] Process Name : " << pe32.szExeFile << endl;
				}

				bProcessFound = Process32Next(hProcess, &pe32);
			}

			CloseHandle(hProcess);
		}

		void get_process_info(void) {

            pe32.dwSize = sizeof(PROCESSENTRY32);

            if (hProcessSnap == INVALID_HANDLE_VALUE) {
                cout << GetLastError() << endl;
                exit(EXIT_FAILURE);
            }

            // PsActiveProcessHead의 첫 번째 프로세스인 System 함수의 정보 받아오기
            if (!Process32First(hProcessSnap, &pe32)) {
                cout << GetLastError() << endl;
                CloseHandle(hProcessSnap);
                return;
            }

            cout << "\t[Process Name] \t[PID]\t[PPID]\t\n" << endl;

            do {
                printf(("%25s %8d %8d %8d \n"), pe32.szExeFile, pe32.th32ProcessID, pe32.th32ParentProcessID);
            } while (Process32Next(hProcessSnap, &pe32));

            return;
        }


        void kill_process(char* TargetProcess) {
            if (hProcessSnap == INVALID_HANDLE_VALUE) {
                cout << GetLastError() << endl;
                return;
            }

            pe32.dwSize = sizeof(PROCESSENTRY32);

            if (!Process32First(hProcessSnap, &pe32)) {
                cout << GetLastError() << endl;
                CloseHandle(hProcessSnap);
                return;
            }

            HANDLE hProcess = NULL;
            BOOL isKill = FALSE;

            do {
                if (strcmp(pe32.szExeFile, TargetProcess) == 0)
                    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pe32.th32ProcessID);

                if (hProcess != NULL) {

                    // 정상 핸들일 경우 kill
                    TerminateProcess(hProcess, -1);
                    isKill = TRUE;
                    CloseHandle(hProcess);
                    break;
                }

            } while (Process32Next(hProcessSnap, &pe32));

            CloseHandle(hProcessSnap);

            if (isKill == FALSE)
                cout << "Failed to kill process. Try again" << endl;
        }


        void kill_proc_init(void)
        {
            while (TRUE)
            {
                //종료를 원하는 프로세스의 이름을 입력받을 버퍼
                char TargetProcess[BUFSIZ];

                //프로세스 목록을 출력
                get_process_info();
                cout << "[+] Input target process name : ";

                cin >> TargetProcess;

                if (strcmp(TargetProcess, ("x")) == 0)
                    exit(EXIT_SUCCESS);

                kill_process(TargetProcess);
            }
        }
};


int main(int argc, char* argv[])
{
	Process proc;

	proc.find_process();
	//proc.get_process_list();

	return 0;

}

