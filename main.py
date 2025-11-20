import cv2
import numpy as np
import car_rl

image_height = 900
image_width = 1600

scene = 0 # 0:lobby, 1:desc, 2:play

# 글로벌 변수들
drawing = False  # 드래그 상태를 추적하는 변수
start_point = None  # 드래그 시작 점
end_point = None  # 드래그 끝 점
circles = []  # 저장된 원들의 리스트

# 마우스 콜백 함수 정의
def draw_circle(event, x, y, flags, param):
    global drawing, start_point, end_point, circles

    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼을 누를 때
        drawing = True
        start_point = [x, y]
        end_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스를 움직일 때
        if drawing:
            end_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:  # 마우스 왼쪽 버튼을 뗄 때
        drawing = False
        end_point = (x, y)
        # 반지름 계산
        radius = 60 + int(np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2))
        # 원 정보 저장
        circles.append((start_point + [radius]))

def lobby_mouse(event,x,y,flags,param):
    if event ==cv2.EVENT_LBUTTONUP:
        print("test")

# 빈 이미지 생성
image = np.full((image_height, image_width, 3), 255,dtype=np.uint8)

#로비 화면 생성
lobby_image = np.full((image_height, image_width, 3), 255,dtype=np.uint8)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 5
thickness = 10
textsize, baseline = cv2.getTextSize("AutoRL", font, font_scale, thickness)
cv2.putText(lobby_image, "AutoRL",((1600 - textsize[0])//2, 300), font, font_scale, (0,0,0), thickness)

button_size = (600, 150)
button_y_pos = 450
cv2.rectangle(lobby_image, (800 - button_size[0]//2, button_y_pos),(800 + button_size[0]//2, button_y_pos+button_size[1]), (0,0,0), 5, )

button_y_pos = 650
cv2.rectangle(lobby_image, (800 - button_size[0]//2, button_y_pos),(800 + button_size[0]//2, button_y_pos+button_size[1]), (0,0,0), 5, )

# 윈도우 생성 및 콜백 함수 등록
cv2.namedWindow('car-rl')
cv2.setMouseCallback('car-rl', draw_circle)
cv2.setMouseCallback('car-rl', lobby_mouse)

while True:
    # 이미지 복사본 생성
    if scene==0:
        img_copy = lobby_image.copy()
    elif scene ==2:
        img_copy = image.copy()

    # 저장된 모든 동그라미 그리기
    for circle in circles:
        cv2.circle(img_copy, circle[:2], circle[2], (0, 0, 0), 2)
    
    # 경로를 잇는 선 그리기    
    for line_start, line_end in zip(circles[:-1], circles[1:]):
        cv2.line(img_copy, line_start[:2], line_end[:2], (255,0,0), 1)

    # 현재 드래그 중인 동그라미 그리기
    if drawing and start_point and end_point:
        temp_radius = 60 + int(np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2))
        cv2.circle(img_copy, start_point, temp_radius, (0, 0, 0), 2)

    # 이미지 표시
    cv2.imshow('car-rl', img_copy)

    # 키 입력 대기
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == ord('s'):  # s키를 누르면 시작
        env = car_rl.enviroment(20, circles)  #circles == roads
        env.train(100)
        break

# 윈도우 종료
cv2.destroyAllWindows()
