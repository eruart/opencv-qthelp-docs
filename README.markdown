#### OpenCV documentation for Qt Creator

Instructions:

``` bash
$ cd "/path/to/opencv/svn/"
$ patch -p0 < "/path/to/opencv-doc.patch"
$ mkdir build && cd build
$ cmake ..
$ make qthelp_docs
$ qcollectiongenerator doc/_qthelp/OpenCV.qhcp
# you will find your .qch file in doc/_qthelp/
```
