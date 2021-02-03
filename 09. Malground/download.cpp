#include <windows.h>
#pragma comment(lib, "urlmon.lib")

void download()
{
    // 다운로드 받아올 데이터가 위치하는 URL
    char url[256];

    // 다운로드 받아서 데이터를 저장할 로컬 PATH
    char path[256];
    
    // 다운로드 기능(url과 path 지정 필요)
    URLDownloadToFileA(NULL, url, path, 0, NULL);
}


int main()
{
    download();
    return 0;
}
