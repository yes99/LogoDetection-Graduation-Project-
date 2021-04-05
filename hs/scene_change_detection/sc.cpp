// http://docs.opencv.org/3.0.0/d5/dc4/tutorial_video_input_psnr_ssim.html
// Base Examples : Video Input with OpenCV and similarity measurement
 
#include <cv.hpp>
#include <string>
#include <iostream>
 
using namespace std;
using namespace cv;
 
double getPSNR(const Mat& I1, const Mat& I2)
{
    Mat s1;
    absdiff(I1, I2, s1);       // |I1 - I2|
    s1.convertTo(s1, CV_32F);  // cannot make a square on 8 bits
    s1 = s1.mul(s1);           // |I1 - I2|^2
    Scalar s = sum(s1);        // sum elements per channel
    double sse = s.val[0] + s.val[1] + s.val[2]; // sum channels
 
    if (sse <= 1e-10) // for small values return zero
        return 0;
    
    double mse = sse / (double)(I1.channels() * I1.total());
    double psnr = 10.0*log10((255 * 255) / mse);
    return psnr;
}
 
void merge(const Mat &m1, const Mat &m2, Mat &result)
{
    resize(result, result, Size(m1.cols + m2.cols, m1.rows));
    
    m1.copyTo(result(Rect(0, 0, m1.cols, m1.rows)));
    m2.copyTo(result(Rect(m1.cols, 0, m2.cols, m2.rows)));
 
    putText(result, "Normal Video", cvPoint(30, 30),
        FONT_HERSHEY_COMPLEX_SMALL, 1.0, cvScalar(200, 200, 250), 1, CV_AA);
 
    putText(result, "Scene Change Detection", cvPoint(m1.cols + 30, 30),
        FONT_HERSHEY_COMPLEX_SMALL, 1.0, cvScalar(200, 200, 250), 1, CV_AA);
}
 
int main()
{
    stringstream conv;
    char c;
    int frameNum = -1; // Frame counter
    double psnrV, CHANGE_DETECT_RATIO = 15.0;
    string videoPath = "testvideo.mp4";
 
    VideoCapture cap(videoPath);
        
    // file open
    if (!cap.isOpened()) {
        cout << "Could not open video - " << videoPath << endl;
        return -1;
    }
    Size s = Size((int)cap.get(CAP_PROP_FRAME_WIDTH), (int)cap.get(CAP_PROP_FRAME_HEIGHT));
    Mat prevFrame, currFrame, changeFrame, result(s, CV_8UC3);
    
    namedWindow("Scene Change Detection");
    resizeWindow("Scene Change Detection", s.width * 2, s.height);
    
    while (1)
    {
        ++frameNum;
        cap >> currFrame;
 
        if (frameNum < 1) {
            prevFrame = currFrame.clone();
            changeFrame = currFrame.clone();
            continue;
        }
        
        if (currFrame.rows == 0 && currFrame.cols == 0)
            break;
 
        psnrV = getPSNR(prevFrame, currFrame);
        
        if (psnrV < CHANGE_DETECT_RATIO)
            changeFrame = currFrame.clone();
        
        merge(currFrame, changeFrame, result);
        imshow("Scene Change Detection", result);
 
        if (frameNum % 2 == 0)
            prevFrame = currFrame.clone();
 
        c = (char)waitKey(10);
        
        if (c == 27)
            break;
    }
 
    return 0;
}