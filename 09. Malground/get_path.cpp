#include <windows.h>
#include <iostream>
using namespace std;


// 현재 실행중인 파일의 디렉터리 경로 확인
void get_current_dir_path()
{
	char fullpath[MAX_PATH];
	GetCurrentDirectory(MAX_PATH, fullpath);
	cout << fullpath << endl;
}


// 현재 실행중인 파일의 전체 경로 확인
void get_fullpath()
{
	char fullpath[MAX_PATH];
	GetModuleFileName(NULL, fullpath, MAX_PATH);
	cout << fullpath << endl;
}


int main(int argc, char **argv)
{
	get_current_dir_path();
	get_fullpath();
	return 0;
}
