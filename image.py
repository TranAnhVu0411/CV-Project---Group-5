class image_object:
    def __init__(self, img, blur_type, blur_ksize, 
                 use_edge_detection, edge_detection_type,
                 gradient_type, gradient_size, skipping_threshold,
                 max_threshold, min_threshold):
        self.img = img
        self.blur_type = blur_type
        self.blur_ksize = blur_ksize
        
        self.use_edge_detection = use_edge_detection
        self.edge_detection_type = edge_detection_type
        
        self.gradient_type = gradient_type
        self.gradient_size = gradient_size
        self.skipping_threshold = skipping_threshold

        self.min_threshold = min_threshold
        self.max_threshold = max_threshold        

def init():
    global list_image_obj
    list_image_obj = []