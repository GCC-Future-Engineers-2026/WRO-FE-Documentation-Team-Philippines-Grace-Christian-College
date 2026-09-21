import sensor
import time
from pupremote import PUPRemoteSensor
from pyb import Pin, Timer

# ===========================================================================
# Tunables
# ===========================================================================
DEBUG = True             # prints FPS to the OpenMV IDE; does NOT touch PUP data.[cite: 3]
FPS_PRINT_EVERY = 30     # print fps once every N frames when DEBUG is on.[cite: 3]

LED_DUTY = 100
# LED brightness %.[cite: 3]

# Lock exposure / gain to fixed values to fight MOTION BLUR.[cite: 3]
EXPOSURE_US = None
GAIN_DB = None

# --- IMAGE PROCESSING LAYER ---[cite: 3]
USE_CLAHE = True         # Normalizes local lighting spots caused by your LEDs.[cite: 3]
CLAHE_CLIP_LIMIT = 3     # High numbers = more contrast, lower numbers = less noise.[cite: 3]

AREA_THRESHOLD = 50     #minimum number of pixels needed to detect block.[cite: 3]

# Gamma / contrast applied to the analysis frame before find_blobs.[cite: 3]
GAMMA = 1.9
CONTRAST = 1.1
BRIGHTNESS = -0.1

# ===========================================================================
# Colour thresholds (LAB) -- BLOCK AND CORNER DETECTION
# ===========================================================================
threshold_pink  = (45, 89, 20, 53, -14, -4) # bright magenta / pink
threshold_red   = (0, 100, 30, 87, 26, 127)
threshold_red2 = (0, 100, 27, 82, 12, 127)
threshold_green = (0, 100, -58, -26, 20, 55)
threshold_black = (0, 42, -86, -3, -3, 2) # current best

# ===========================================================================
# ROIs FOR CORNER AND BLOCK DETECTION
# ===========================================================================
img_center = (160, 120)
img_roi = (45, 115, 230, 80)
roi_rect = (img_roi[0], img_roi[1], img_roi[2], img_roi[3])
roi_left_bottom = (5, 201, 70, 35)
roi_right_bottom = (245, 201, 70, 35)
img_roi_corner = (155, 175, 10, 48)


# ===========================================================================
# PUPRemote Command Callback
# ===========================================================================
def msg(txt):
    # Callback handler for PUPRemote 'msg' command received from the Hub.[cite: 3]
    # PUPRemote requires a return value matching the 'repr' format.[cite: 3]
    print(txt)
    return txt + txt


# ===========================================================================
# LED Control
# ===========================================================================
light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
light.pulse_width_percent(LED_DUTY)

# ===========================================================================
# Camera Sensor Initialization
# ===========================================================================
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_hmirror(False)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False)
sensor.skip_frames(time=2000)
# sensor.set_hmirror(True)[cite: 3]
# sensor.set_vflip(True)[cite: 3]

# Optional explicit locks, applied AFTER skip_frames so they actually stick.[cite: 3]
if GAIN_DB is not None:
    sensor.set_auto_gain(False, gain_db=GAIN_DB)
if EXPOSURE_US is not None:
    sensor.set_auto_exposure(False, exposure_us=EXPOSURE_US)

# ===========================================================================
# PUPRemote Communication
# ===========================================================================
p = PUPRemoteSensor(power=True)
p.add_command('msg', "repr", "repr")
p.add_channel('cam', to_hub_fmt='bhhb')


def _bbox_center(b):
    return (b.x() + (b.w() // 2), b.y() + (b.h() // 2))

def find_block(img_proc, img_debug):
    # Detect the nearest red / green / pink block.[cite: 3]

    # img_proc  : Shared gamma-corrected and CLAHE analysis frame.[cite: 3]
    # img_debug : Raw overlay frame displayed in OpenMV IDE.[cite: 3]

    nearestRed = None
    nearestGreen = None
    nearestPink = None
    red_val = 0
    green_val = 0
    pink_val = 0

    img_debug.draw_rectangle(img_roi, color=(0, 0, 255))

    red = img_proc.find_blobs([threshold_red, threshold_red2], area_threshold=50,pixel_threshold=550, roi=img_roi, merge=True)
    green = img_proc.find_blobs([threshold_green], area_threshold=50, pixel_threshold=600, roi=img_roi, merge=True)
    pink = img_proc.find_blobs([threshold_pink], area_threshold=AREA_THRESHOLD, roi=img_roi, merge=True)

    if red:
        for b in red:
            # Red block: Draw debug cross at RIGHTMOST edge
            cx = b.x() + b.w()
            cy = b.y() + b.h()
            img_debug.draw_rectangle(b.rect(), color=(255, 0, 0))
            img_debug.draw_cross(cx, cy, color=(255, 0, 0))

            # Proximity calculation: Y + H equals the bottom edge of the blob.[cite: 3]
            # Higher pixel value = lower down in the frame = closer to the robot camera.[cite: 3]
            val = b.y() + b.h()
            if val > red_val:
                red_val = val
                nearestRed = b

    if green:
        for b in green:
            # Green block: Draw debug cross at LEFTMOST edge
            cx = b.x()
            cy = b.y() + b.h()
            img_debug.draw_rectangle(b.rect(), color=(0, 255, 0))
            img_debug.draw_cross(cx, cy, color=(0, 255, 0))

            # Proximity calculation: Higher pixel value = closer to the robot camera.[cite: 3]
            val = b.y() + b.h()
            if val > green_val:
                green_val = val
                nearestGreen = b

    if pink:
        for b in pink:
            cx, cy = _bbox_center(b)
            img_debug.draw_rectangle(b.rect(), color=(255, 0, 255))
            img_debug.draw_cross(cx, cy, color=(255, 0, 255))

            # Pink is actively tracked to isolate it from red, preventing false red positives.[cite: 3]
            val = b.y() + b.h()
            if val > pink_val:
                pink_val = val
                nearestPink = b

    # Pick dominant colour based on closest block (lowest in frame)[cite: 3]
    # COLOR MAPPING KEY FOR HUB: 0 = None, 1 = Green, 2 = Red[cite: 3]
    if nearestRed and nearestGreen:
        color = 2 if red_val >= green_val else 1
    elif nearestRed:
        color = 2
    elif nearestGreen:
        color = 1
    else:
        color = 0

    if color == 2:  # Red block -> Rightmost X coordinate
        center_x = nearestRed.x() + nearestRed.w()
        center_y = nearestRed.y() + (nearestRed.h() // 2)
    elif color == 1:  # Green block -> Leftmost X coordinate
        center_x = nearestGreen.x()
        center_y = nearestGreen.y() + (nearestGreen.h() // 2)
    else:
        center_x, center_y = 0, 0

    if nearestPink is not None:
        p_center_x, p_center_y = _bbox_center(nearestPink)
    else:
        p_center_x, p_center_y = 0, 0

    return {
        "center_x": center_x,
        "center_y": center_y,
        "color": color,
        "p_center_x": p_center_x,
        "p_center_y": p_center_y,
    }


def check_corner_roi(img_proc, img_debug):
    img_debug.draw_rectangle(img_roi_corner, color=(255, 255, 0))
    black = img_proc.find_blobs([threshold_black], area_threshold= 20, roi=img_roi_corner, merge=True)
    return {"black": 1 if black else 0}


# ===========================================================================
# Main Execution Loop
# ===========================================================================
clock = time.clock()
_frame = 0

while True:
    clock.tick()
    img_debug = sensor.snapshot()

    # Image preparation layer[cite: 3]
    img_proc = img_debug.copy()
    img_proc.gamma_corr(gamma=GAMMA, contrast=CONTRAST, brightness=BRIGHTNESS)

    if USE_CLAHE:
        img_proc.histeq(adaptive=True, clip_limit=CLAHE_CLIP_LIMIT)

    img_debug.draw_cross(160, 120, color=(0, 0, 0)) # place cross on the center of the camera[cite: 3]

    block = find_block(img_proc, img_debug)
    corner = check_corner_roi(img_proc, img_debug)

    # NOTE: Pink block data is purposely omitted from 'data' tuple because the[cite: 3]
    # 'cam' PUPRemote channel format ('bhhb') is only configured to send 4 values.[cite: 3]
    data = (block["color"], block["center_x"], block["center_y"], corner["black"])
    # print(data)[cite: 3]
    p.update_channel('cam', *data)
    p.process()

    # print(corner["black"])[cite: 3]
    if DEBUG:
        _frame += 1
        if _frame >= FPS_PRINT_EVERY:
            print("fps:", clock.fps())
            _frame = 0

    # Give the hardware background handler a tiny window to service the USB link[cite: 3]
    time.sleep_ms(1)
