import numpy as np
import cv2 as cv

video = cv.VideoCapture('rtsp://210.99.70.120:1935/live/cctv001.stream')
record = False
delay_ms = 20
fps = int(1000/delay_ms)
ab = 0 # additional brightness
snc = 0 # snapshot number counting

if not video.isOpened():
    print("fail to open video")
    exit()


valid, img = video.read()
if not valid:
    print("fail to read video")
    exit()
h, w, *_ = img.shape
writer = cv.VideoWriter('record.avi', cv.VideoWriter_fourcc(*'XVID'), fps, (w, h))

while True:
    valid, img = video.read()

    if not valid:
        break

    # 밝기 값 보정 및 상한(255), 하한(0) 벗어나지 않게 조절
    img = img.astype(np.int32) + ab
    img[img < 0] = 0
    img[img > 255] = 255
    img = img.astype(np.uint8)

    # 영상에 record 뜨는거 방지(녹화 될 영상과 같은 이미지인 frame을 하나 더 추가)
    frame = img.copy()

    # Record 글자 표시
    if record:
        # 글자와 원은 화면에 띄울 frame에만 삽입
        cv.circle(frame, (35, 28), 10, (180,180,225), 2)
        cv.circle(frame, (35, 28), 10, (0,0,255), -1)
        cv.putText(frame, "REC", (50,35), cv.FONT_HERSHEY_SIMPLEX, 0.7, (180,180,225), thickness=3)
        cv.putText(frame, "REC", (50,35), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        
        # 녹화(녹화는 record 글자가 들어간 frame이 아닌 원본 img로 저장)
        writer.write(img)

    # 화면 출력(화면에 띄우는건 복사된 frame)
    cv.imshow('Simple Video Recorder', frame)
    key = cv.waitKey(delay_ms)

    # 키 입력 event 대응
    # ESC
    if key == 27: 
        break
    # Space(Record)
    elif key == 32:
        record = not record
        print("Record : ", record)
    # 밝기 조절(i(+), o(-))
    elif key == ord('i') or key == ord('I'):
        ab += 5
        if ab > 255 :
            ab = 255
        print(f'brightness ++ / now addtional brightness : {ab}')
    elif key == ord('o') or key == ord('O'):
        ab -= 5
        if ab < -255 :
            ab = -255
        print(f'brightness -- / now addtional brightness : {ab}')
    # 스냅샷 저장(p)
    elif key == ord('p') or key == ord('P'):
        cv.imwrite(f'snapshot_{snc}.png', img)
        print(f"saved snapshot_{snc}.png")
        snc += 1
    
    
video.release()
writer.release()
cv.destroyAllWindows()


