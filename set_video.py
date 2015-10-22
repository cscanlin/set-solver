import set_solver as ss
import cv2, util
import numpy as np

# open video feed
# solve for every frame

WINDOW_NAME = 'video'
PREV_FRAME_STACK_SIZE = 3
MOVEMENT_THRESHOLD = 5
def main():
    cv2.namedWindow(WINDOW_NAME)
    vc = cv2.VideoCapture(1)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = false

    prev_frames = []

    while rval:
        # if image has stabilized, solve
        if has_stabilized(prev_frames):
            do_solve(frame)

        # get new frame and add to stack of frames
        rval, frame = vc.read()

        if len(prev_frames) > PREV_FRAME_STACK_SIZE:
            prev_frames.pop(0)
        prev_frames.append(frame)

def has_stabilized(frames):
    if len(frames) < 1:
        return 

    preprocessed = map(lambda x: util.preprocess(x), frames)
    sum_diff = 0

    for i in range(len(preprocessed)):
        if i + 1 > len(preprocessed) - 1:
            break
        diff = cv2.absdiff(preprocessed[i], preprocessed[i + 1])
        sum_diff += np.sum(diff)

    return sum_diff/len(preprocessed)/preprocessed[0].size < MOVEMENT_THRESHOLD

def do_solve(frame):
    # do set stuff
    cards = ss.detect_cards(frame, draw_rects=True)
    cv2.imshow(WINDOW_NAME, frame)
    
    if(len(cards) < 1):
        return 

    # get property of cards and print
    props = ss.get_card_properties(cards)
    print_properties(props)

def print_properties(props):
    if len(props) > 0:
        ss.pretty_print_properties(props)
        print('----')

main()