import pytesseract
import cv2
from PIL import Image, ImageFont, ImageDraw

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def videoToFrames():
    vidcap = cv2.VideoCapture('montage.mp4')
    success, image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("frame%d.png" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1

def readImage(imageName):
    img = cv2.imread(imageName)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binarized = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contents = pytesseract.image_to_string(binarized)

    return contents.split()
def readVideoFrames():
    try:
        gtList = []  # This will now be a list of tuples
        frameName = "frame1073.png"
        count = 1073
        while True:
            arrTxt = readImage(frameName)
            if len(arrTxt) > 0:
                if "You" in arrTxt:
                    youIndex = arrTxt.index("You") + 1
                    if arrTxt[youIndex] == "killed" or arrTxt[youIndex] == "sniped" or arrTxt[youIndex] == "lasered":
                        index = arrTxt.index("You")
                        gt = arrTxt[index + 2]
                        # Check if the gamertag is already in the list, considering the frame name
                        if not any(gt == existing_gt for existing_gt, _ in gtList):
                            gtList.append((gt, frameName))  # Append the tuple

            frameName = frameName.replace(str(count), str(count + 1))
            count += 1
            print(frameName)
            print(gtList)
    except:
        print("End of Frames: The gamertags in the montage killed by the montager are:")
        for gt, frame in gtList:
            print(f"Gamertag: {gt}, Frame: {frame}")

readVideoFrames()
