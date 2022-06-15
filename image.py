class image_object:
    def __init__(self, img, name, blur_type, blur_ksize, 
                 use_edge_detection, edge_detection_type,
                 gradient_type, gradient_size, skipping_threshold,
                 max_threshold, min_threshold):
        self.img = img
        self.name = name
        self.blur_type = blur_type
        self.blur_ksize = blur_ksize
        
        self.use_edge_detection = use_edge_detection
        self.edge_detection_type = edge_detection_type
        
        self.gradient_type = gradient_type
        self.gradient_size = gradient_size
        self.skipping_threshold = skipping_threshold

        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
    def show_info(self):
        info = "Image Name: "+ self.name+" \n"
        info += "Blur Type: "+self.blur_type+"\n"
        if self.blur_type != "None":
            info += "Blur Kernel Size: "+str(self.blur_ksize)+"\n\n"
        info += "Use Edge Detection: "+self.use_edge_detection+"\n"
        if self.use_edge_detection != "no":
            info += "Edge Detection Method: "+self.edge_detection_type+"\n"
            if self.edge_detection_type == "Skipping Threshold":
                info += "Type: "+self.gradient_type+"\n"
                if self.gradient_type!="Prewitt":
                    info += "Kernel Size: "+str(self.gradient_size)+"\n"
                info += "Skipping Threshold: "+str(self.skipping_threshold)+"\n"
            else:
                info += "Min Threshold: "+str(self.min_threshold)+"\n"
                info += "Max Threshold: "+str(self.max_threshold)+"\n"
        return info

def init():
    global list_image_obj
    list_image_obj = []