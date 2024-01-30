import cv2
import socket
import base64

def connect_to_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('58.237.187.59', 8000))

    print("서버에 연결됨")
    cam = cv2.VideoCapture(0)
    # 이미지 속성 변경 3 = width, 4 = height
    cam.set(3, 640)
    cam.set(4, 480)
    cam.set(cv2.CAP_PROP_FPS, 60)
    # 0~100에서 90의 이미지 품질로 설정 (default = 95)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    print("전송시작")

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame, encode_param)
        if not ret:
            continue
        data = base64.b64encode(buffer)
        s.sendall(data + bytes("끝", 'utf-8'))
    s.close()

if __name__ == '__main__':
    connect_to_server()
