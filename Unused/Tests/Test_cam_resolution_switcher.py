import cv2


def get_frame_size(cap):
    return cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)


def set_frame_size(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)


initial_sizes = []
num_cams = 2
caps = []
frame_sizes = []
indices = []
for i in range(num_cams):
    frame_sizes.append([])
    indices.append(0)

for i in range(num_cams):
    caps.append(cv2.VideoCapture(i, cv2.CAP_DSHOW))

for i in range(num_cams):
    initial_sizes.append(get_frame_size(caps[i]))
    large_size = (4000, 4000)
    step = 100
    set_frame_size(caps[i], large_size[0], large_size[1])
    max_size = get_frame_size(caps[i])
    current_size = initial_sizes[i]

    while current_size[0] <= max_size[0]:
        set_frame_size(caps[i], current_size[0], current_size[1])
        result = get_frame_size(caps[i])
        if result not in frame_sizes[i]:
            frame_sizes[i].append(result)
        new_x = current_size[0] + step
        new_y = current_size[1] + step
        if result[0] > new_x:
            new_x = result[0] + step
        if result[1] > new_y:
            new_y = result[1] + step
        current_size = (new_x, new_y)

    set_frame_size(caps[i], initial_sizes[i][0], initial_sizes[i][1])
    print(frame_sizes[i])

ret = False
frame = None
running = True
while running:
    # Capture frame-by-frame
    if num_cams == 0:
        running = False
    for i in range(num_cams):
        print("Looping for cam:", i)
        ret, frame = caps[i].read()
        if frame is None:
            print("Frame is None for cam:", i)
            caps[i].release()
            del caps[i]
            cv2.destroyWindow('frame' + str(i))
            num_cams -= 1
            break
        if not ret:
            break
        try:
            cv2.imshow('frame' + str(i), frame)
        except:
            print("Cam:", i, "That frame didn't work")
            print(caps[i].isOpened())  # Seems to still be open when it fails.
            set_frame_size(caps[i], initial_sizes[i][0], initial_sizes[i][1])
            continue
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord('q'):
            running = False
        elif keypress == ord('n'):
            indices[i] = (indices[i] + 1) % len(frame_sizes[i])
            set_frame_size(caps[i], frame_sizes[i][indices[i]][0], frame_sizes[i][indices[i]][1])

# When everything done, release the capture
for i in range(num_cams):
    caps[i].release()

cv2.destroyAllWindows()
