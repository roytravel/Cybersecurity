#include <windows.h>
#pragma comment(lib, "urlmon.lib")

void execute()
{
    
    // 실행을 원하는 파일의 경로
    char fullpath[256];

    // SW_HIDE = Hides the window and activates another window
    // fullpath 이후 NULL은 파라미터를 의미
    ShellExecuteA(NULL, "open", fullpath, NULL, NULL, SW_HIDE);
}


int main()
{
    execute();
    return 0;
}
