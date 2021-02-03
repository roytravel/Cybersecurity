#include <Windows.h>
#include <iostream>
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"

using namespace std;
using namespace cv;

class hWnd2Mat
{
    public:
        hWnd2Mat(HWND hWindow, float scale = 1);

        // 함수 명 앞에 ~는 소멸자를 의미
        // 소멸자는 개체가 범위를 벗어나거나 delete 호출에 의해 명시적으로 제거 될 때 자동으로 호출 되는 멤버 함수
        virtual ~hWnd2Mat();
        virtual void Read();
        Mat capture;

    private:
        HWND hWnd;
        HDC hWindowDC, hWindowCompatibleDC;
        int height, width, srcHeight, srcWidth;
        HBITMAP hBitmap;
        BITMAPINFOHEADER bi;
};

hWnd2Mat::hWnd2Mat(HWND hWindow, float scale)
{
    hWnd = hWindow;
    hWindowDC = GetDC(hWnd); //DC = Device Context
    hWindowCompatibleDC = CreateCompatibleDC(hWindowDC);
    SetStretchBltMode(hWindowCompatibleDC, COLORONCOLOR);

    RECT windowsize;    // 스크린의 높이와 너비 GET
    GetClientRect(hWnd, &windowsize);

    srcHeight = windowsize.bottom;
    srcWidth = windowsize.right;
    height = (int)(windowsize.bottom * scale);
    width = (int)(windowsize.right * scale);

    capture.create(height, width, CV_8UC4);

    // 비트맵 생성
    hBitmap = CreateCompatibleBitmap(hWindowDC, width, height);
    bi.biSize = sizeof(BITMAPINFOHEADER);    // http://msdn.microsoft.com/en-us/library/windows/window/dd183402%28v=vs.85%29.aspx
    bi.biWidth = width;
    bi.biHeight = -height;  //this is the line that makes it draw upside down or not
    bi.biPlanes = 1;
    bi.biBitCount = 32;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;
    bi.biXPelsPerMeter = 0;
    bi.biYPelsPerMeter = 0;
    bi.biClrUsed = 0;
    bi.biClrImportant = 0;

    // use the previously created device context with the bitmap
    SelectObject(hWindowCompatibleDC, hBitmap);
};


void hWnd2Mat::Read()
{
    // copy from the window device context to the bitmap device context
    StretchBlt(hWindowCompatibleDC, 0, 0, width, height, hWindowDC, 0, 0, srcWidth, srcHeight, SRCCOPY);
    //change SRCCOPY to NOTSRCCOPY for wacky colors!
    GetDIBits(hWindowCompatibleDC, hBitmap, 0, height, capture.data, (BITMAPINFO*)&bi, DIB_RGB_COLORS);
    //copy from hWindowCompatibleDC to hBitmap
};


hWnd2Mat::~hWnd2Mat()
{
    DeleteObject(hBitmap);
    DeleteDC(hWindowCompatibleDC);
    ReleaseDC(hWnd, hWindowDC);
};


int main(int argc, char **argv)
{
    HWND hWndDesktop = GetDesktopWindow();
    hWnd2Mat desktop(hWndDesktop, 1);    // scale = 1

    // 시간이 아니라 다른 동작으로 변형 가능
    //cout << "Screen capure in 3 seconds." << endl;

    /*for (int i = 3; i > 0; i--)
    {
        cout << i << ".." << endl;
        Sleep(1000);
    }*/

    desktop.Read();
    imshow("Capture", desktop.capture);

    waitKey();

    return 0;
}

