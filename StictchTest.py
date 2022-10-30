import cv2

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()


    try:
        stitcher = cv2.Stitcher.create()
        (status, res) = stitcher.stitch([cv2.resize(frame1, (0,0), None, 0.5, 0.5), cv2.resize(frame2, (0,0), None, 0.5, 0.5)])   
        # (status, res) = stitcher.stitch([frame1, frame2])   
    except:
        print("Error stitching")
        continue

    if (status == cv2.STITCHER_OK):
        print("Stitching successful")
        cv2.imshow("Stitched", res)
    else: 
        print("Stitching failed")

    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2)

    key = cv2.waitKey(1) & 0xFF == ord('q')

