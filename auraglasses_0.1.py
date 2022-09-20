# Color Light Removal
#
# This example shows off how to remove bright lights from the image.
# You can do this using the binary() method with the "zero=" argument.
#
# Removing bright lights from the image allows you to now use
# histeq() on the image without outliers from oversaturated
# parts of the image breaking the algorithm...

import sensor, image, time, pyb

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_hmirror(True)
sensor.set_vflip(True)
clock = time.clock() # Tracks FPS.

p = pyb.Pin('P4', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
p2 = pyb.Pin('P5', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)

thresholds = (100, 100, -128, 127, -128, 127)

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot().binary([thresholds], invert=False, zero=True)

    print(clock.fps()) # Note: Your OpenMV Cam runs about half as fast while
    # connected to your computer. The FPS should increase once disconnected.
