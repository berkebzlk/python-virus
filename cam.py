import cv2

def cams(name):
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite(name, image)
    camera.release()
    cv2.destroyAllWindows()