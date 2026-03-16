import numpy as np
import cv2 as cv

video = cv.VideoCapture('rtsp://210.99.70.120:1935/live/cctv001.stream')
record = False
fps = 20

if not video.isOpened():
    print("fail to open video")
    exit()

elif video.isOpened():
    valid, img = video.read()
    h, w, *_ = img.shape
    writer = cv.VideoWriter('record.avi', cv.VideoWriter_fourcc(*'XVID'), fps, (w, h))
    while True:
        valid, img = video.read()

        if not valid:
            break

        # 영상에 record 뜨는거 방지(녹화 될 영상과 같은 이미지인 frame을 하나 더 추가)
        frame = img.copy()

        # Record 글자 표시
        if record:
            # 글자와 원은 화면에 띄울 frame에만 삽입
            cv.circle(frame, (30, 30), 10, (0,0,255), -1)
            cv.putText(frame, "REC", (50,35), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            
            # 녹화(녹화는 record 글자가 들어간 frame이 아닌 원본 img로 저장)
            writer.write(img)

        # 화면 출력(화면에 띄우는건 복사된 frame)
        cv.imshow('Simple Video Recorder', frame)
        key = cv.waitKey(fps)

        # 키 입력 event 대응
        # ESC
        if key == 27: 
            break

        # Space(Record)
        elif key == 32:
            record = not record
            print("Record:", record)

    video.release()
    writer.release()
    cv.destroyAllWindows()


