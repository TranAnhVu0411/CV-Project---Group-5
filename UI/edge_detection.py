import cv2
import numpy as np


def blur(gray, blur_type, blur_ksize):
    """
    img: gray image
    blur_type: mean or gaussian
    blur_ksize: size of blur kernel; it must be 1, 3, 5, or 7.
    """
    # blur image
    if blur_type == "Mean filter":
        return cv2.blur(gray, (blur_ksize, blur_ksize))
    elif blur_type == "Gaussian filter":
        return cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    else:
        return gray

def sobel_edge_detection(img_blur, sobel_ksize, skipping_threshold):
    """
    img_blur: image that is blur
    sobel_ksize: size of the extended Sobel kernel; it must be 1, 3, 5, or 7.
    skipping_threshold: ignore weakly edge
    """
    
    # sobel algorthm use cv2.CV_64F
    sobelx64f = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=sobel_ksize)
    abs_sobel64f = np.absolute(sobelx64f)
    img_sobelx = np.uint8(abs_sobel64f)

    sobely64f = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=sobel_ksize)
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
    return img_sobel

def prewitt_edge_detection(img_blur, skipping_threshold):
    """
    img_blur: image that is blur
    skipping_threshold: ignore weakly edge
    """

    kernelX=np.array([[1,1,1], [0,0,0], [-1, -1, -1]])
    kernelY=np.array([[-1,0,1], [-1,0,1], [-1,0,1]])
    
    # algorithm
    img_prewitt_x = cv2.filter2D(img_blur, -1, kernelX)
    img_prewitt_y = cv2.filter2D(img_blur, -1, kernelY)

    
    # calculate magnitude
    img_prewitt = (img_prewitt_x + img_prewitt_y)/2
    
    # ignore weakly pixel
    for i in range(img_prewitt.shape[0]):
        for j in range(img_prewitt.shape[1]):
            if img_prewitt[i][j] < skipping_threshold:
                img_prewitt[i][j] = 0
            else:
                img_prewitt[i][j] = 255
    return img_prewitt

def laplacian_edge_detection(img_blur, laplacian_ksize, skipping_threshold):
    """
    img_blur: image that is blur
    laplacian_ksize: size of the extended Laplacian kernel; it must be 1, 3, 5, or 7.
    skipping_threshold: ignore weakly edge
    """
    
    # calculate magnitude
    img_laplacian = cv2.Laplacian(img_blur, cv2.CV_64F, ksize=laplacian_ksize) 
    #convert to uint8 array
    img_laplacian = cv2.convertScaleAbs(img_laplacian) 
    # ignore weakly pixel
    for i in range(img_laplacian.shape[0]):
        for j in range(img_laplacian.shape[1]):
            if img_laplacian[i][j] < skipping_threshold:
                img_laplacian[i][j] = 0
            else:
                img_laplacian[i][j] = 255
    return img_laplacian

def canny_edge_detection(img_blur, threshold1=100, threshold2=200):
    """
    img_blur: image that is blur
    threshold1: min threshold 
    threshold2: max threshold
    """

    img_canny = cv2.Canny(img_blur,threshold1,threshold2)

    return img_canny

def edge_detection(img, blur_type, blur_ksize, 
                   use_edge_detection, edge_detection_type,
                   gradient_type, gradient_size, skipping_threshold,
                   max_threshold, min_threshold):
    if use_edge_detection=="no":
        return blur(img, blur_type, blur_ksize)
    else:
        blur_image = blur(img, blur_type, blur_ksize)
        if edge_detection_type=="Skipping Threshold":
            if gradient_type == "Prewitt":
                return prewitt_edge_detection(blur_image, skipping_threshold)
            elif gradient_type == "Sobel":
                return sobel_edge_detection(blur_image, gradient_size, skipping_threshold)
            else:
                return laplacian_edge_detection(blur_image, gradient_size, skipping_threshold)
        else:
            return canny_edge_detection(blur_image, min_threshold, max_threshold)
