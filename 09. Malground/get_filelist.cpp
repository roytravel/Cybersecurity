#include <iostream>
#include <io.h>
#include <string>
using namespace std;

/*
struct _finddata_t {
	unsigned    attrib;
	time_t      time_create;    // -1 for FAT file systems
	time_t      time_access;    // -1 for FAT file systems 
	time_t      time_write;
	_fsize_t    size;
	char        name[260];
};
*/


int main(int argc, char* argv[])
{
	// 디렉터리 지정
	string path = "*.*";

	// 파일 정보 관리를 위한 자료형 _finddata_t 선언
	struct _finddata_t fd;

	// 정수형 포인터를 저장하기 위한 handle 변수 할당
	intptr_t handle;

	// 파일 검색에 사용되는 첫 번째 함수 사용 : _findfirst
	// c_str : 문자열 배열의 시작 주소 값 반환
	handle = _findfirst(path.c_str(), &fd);

	// 
	if (handle == -1)
		exit(0);

	do{
		cout << fd.name << endl;

	// 파일 검색에 사용되는 두 번째 함수 사용 : _findnext
	} while (_findnext(handle, &fd) == 0);

	// 파일 검색에 사용되는 세 번째 함수 사용 : _findclose
	_findclose(handle);
}

