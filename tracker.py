import cv2

tracker = cv2.legacy.TrackerCSRT_create()
v = cv2.VideoCapture('mot.mp4')
ret, frame = v.read()
cv2.imshow('Frame', frame)
bb = cv2.selectROI('Frame', frame)
cv2.waitKey(0)
#v.release()
cv2.destroyAllWindows()

tracker.init(frame, bb)

frame_width = 480
frame_height = 360
size = (frame_height, frame_width)
i = 0
while True:
    ret, frame = v.read()
    if not ret:
        break
    (success, box) = tracker.update(frame)
    if success:
        (x, y, w, h) = [int(a) for a in box]
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        xc = int((x+x+w)/2)
        yc = int((y+y+h)/2)
        new_h = h+10
        new_w = int((3/4)*new_h)
        new_frame = frame[yc-new_h:yc+new_h, xc-new_w:xc+new_w]
        new_frame = cv2.resize(new_frame, size)
        if i == 0:
            result = cv2.VideoWriter('cropped.mp4',
                                     cv2.VideoWriter_fourcc(*'MP4V'), 25, size)
        i = 1
    cv2.imshow('Frame', new_frame)
    result.write(new_frame)
    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
result.release()
v.release()
cv2.destroyAllWindows()
