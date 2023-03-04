# Edge Impulse - OpenMV Image Classification
# Antoine Vergnaud & Gaëtan Pusel

import sensor, image, time, os, tf, uos, gc, math

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.
sensor.set_hmirror(True)
sensor.set_vflip(True)


min_confidence = 0.8
net = None
labels = None

try:
    # load the model, alloc the model file on the heap if we have at least 64K free after loading
    net = tf.load("trained.tflite", load_to_fb=uos.stat('trained.tflite')[6] > (gc.mem_free() - (64*1024)))
except Exception as e:
    print(e)
    raise Exception('Failed to load "trained.tflite", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

try:
    labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
    raise Exception('Failed to load "labels.txt", did you copy the .tflite and labels.txt file onto the mass-storage device? (' + str(e) + ')')

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # Crop in the middle (avoids vignetting)
    img.crop((img.width()//2-28//2,
              img.height()//2-28//2,
              28,
              28))

    # Binarize the image
    img.midpoint(2, bias=0.5, threshold=True, offset=5, invert=True)

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?

        print("********** %s **********" % labels[i])

    #print(clock.fps(), "fps", end="\n")