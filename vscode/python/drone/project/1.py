import cv2
import mediapipe as mp

# 初始化 MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# 開啟電腦攝像頭
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access the camera.")
    exit()

print("Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # 將圖像轉為 RGB 格式
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 偵測臉部關鍵點
    results = face_mesh.process(rgb_frame)

    # 設置畫面中心座標
    screen_height, screen_width, _ = frame.shape
    center_x, center_y = screen_width // 2, screen_height // 2

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 獲取鼻尖座標
            nose = face_landmarks.landmark[1]
            head_x = int(nose.x * screen_width)
            head_y = int(nose.y * screen_height)

            # 計算頭部位置與畫面中心的偏移量
            offset_x = head_x - center_x
            offset_y = head_y - center_y

            # 印出數據到終端
            print(f"Nose Position: (X: {head_x}, Y: {head_y}), Offset: (X: {offset_x}, Y: {offset_y})")

            # 在畫面上顯示數據
            cv2.putText(frame, f'Nose: ({head_x}, {head_y})', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f'Offset: ({offset_x}, {offset_y})', (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 標記鼻尖位置和畫面中心
            cv2.circle(frame, (head_x, head_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # 顯示畫面
    cv2.imshow('Head Tracking', frame)

    # 按 'q' 鍵退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()
