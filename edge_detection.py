import cv2
import numpy as np

def sobel_edge_detection(image_path, blur_ksize, sobel_ksize, skipping_threshold):
    """
    image_path: link to image
    blur_ksize: kernel size parameter for Gaussian Blurry
    sobel_ksize: size of the extended Sobel kernel; it must be 1, 3, 5, or 7.
    skipping_threshold: ignore weakly edge
    """
    # read image
    img = cv2.imread(image_path)
    
    # convert BGR to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    
    # sobel algorthm use cv2.CV_64F
    sobelx64f = cv2.Sobel(img_gaussian, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    abs_sobel64f = np.absolute(sobelx64f)
    img_sobelx = np.uint8(abs_sobel64f)

    sobely64f = cv2.Sobel(img_gaussian, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    abs_sobel64f = np.absolute(sobely64f)
    img_sobely = np.uint8(abs_sobel64f)
    
    # calculate magnitude
    img_sobel = (img_sobelx + img_sobely)/2
    
    # ignore weakly pixel
    for i in range(img_sobel.shape[0]):
        for j in range(img_sobel.shape[1]):
            if img_sobel[i][j] < skipping_threshold:
                img_sobel[i][j] = 0
            else:
                img_sobel[i][j] = 255
    return img_sobelx, img_sobely, img_sobel

def prewitt_edge_detection(image_path, blur_ksize, skipping_threshold):
    """
    image_path: link to image
    blur_ksize: kernel size parameter for Gaussian Blurry
    skipping_threshold: ignore weakly edge
    """
    # read image
    img = cv2.imread(image_path)
    # convert BGR to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

    kernelX=np.array([[1,1,1], [0,0,0], [-1, -1, -1]])
    kernelY=np.array([[-1,0,1], [-1,0,1], [-1,0,1]])
    
    # algorithm
    img_prewitt_x = cv2.filter2D(img_gaussian, -1, kernelX)
    img_prewitt_y = cv2.filter2D(img_gaussian, -1, kernelY)

    
    # calculate magnitude
    img_prewitt = (img_prewitt_x + img_prewitt_y)/2
    
    # ignore weakly pixel
    for i in range(img_prewitt.shape[0]):
        for j in range(img_prewitt.shape[1]):
            if img_prewitt[i][j] < skipping_threshold:
                img_prewitt[i][j] = 0
            else:
                img_prewitt[i][j] = 255
    return img_prewitt_x, img_prewitt_y, img_prewitt

def laplacian_edge_detection(image_path, blur_ksize, laplacian_ksize, skipping_threshold):
    """
    image_path: link to image
    blur_ksize: kernel size parameter for Gaussian Blurry
    laplacian_ksize: size of the extended Laplacian kernel; it must be 1, 3, 5, or 7.
    skipping_threshold: ignore weakly edge
    """
    # read image
    img = cv2.imread(image_path)
    
    # convert BGR to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    
    # calculate magnitude
    img_laplacian = cv2.Laplacian(img_gaussian, cv2.CV_64F, ksize=laplacian_ksize) 
    
    # ignore weakly pixel
    for i in range(img_laplacian.shape[0]):
        for j in range(img_laplacian.shape[1]):
            if img_laplacian[i][j] < skipping_threshold:
                img_laplacian[i][j] = 0
            else:
                img_laplacian[i][j] = 255
    return img_laplacian

def canny_edge_detection(image_path, blur_ksize=5, threshold1=100, threshold2=200):
    """
    image_path: link to image
    blur_ksize: Gaussian kernel size
    threshold1: min threshold 
    threshold2: max threshold
    """
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(gray,(blur_ksize,blur_ksize),0)

    img_canny = cv2.Canny(img_gaussian,threshold1,threshold2)

    return img_canny