// Example showing how to read and write images
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/video/video.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>

using namespace cv;

int main(int argc, char** argv)
{   
    // Load an image from file - change this based on your image name
    Mat img = imread("apple.jpg");

    if(img.empty())
    {
        fprintf(stderr, "failed to load input image\n");
        return -1;
    }

    // this is just to show, that you won't have to pre-alloc
    // result-images with c++ any more..
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);

    // Write the image to a file with a different name,
    // using a different image format -- .png instead of .jpg
    if( ! imwrite("my_image_copy.png", gray) )
    {
        fprintf(stderr, "failed to write image file\n");
    }

    // no need to release anything with c++ !   
    return 0;
}