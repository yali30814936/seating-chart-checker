import cv2

def load_image(path:str):
    """讀取圖片並回傳 np 格式的照片

    Args:
        path (str): 圖片檔案路徑

    Returns:
        ndarray: numpy 型態的圖片
    """
    img = cv2.imread(path)
    return img
            
def rotate_image(img):
    """順時針旋轉圖片 90 度

    Args:
        img (ndarray): numpy 型態的圖片

    Returns:
        ndarray: numpy 型態轉完90度的圖片
    """
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# if __name__ == "__main__":
#     im = load_image(r"C:\Programing\Python\seating-chart-checker\resource\TestCase\2\1.jpg")
#     print(type(im))
#     cv2.imshow("test", im)
#     cv2.waitKey(0)
#     cv2.imshow("test", rotate_image(im))
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()