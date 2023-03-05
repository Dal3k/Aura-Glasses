import sensor, image, time, pyb

tresholds = [240, 255]
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(30)
sensor.set_vflip(True)
sensor.set_hmirror(True)
clock = time.clock()

p = pyb.Pin('P4', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
p2 = pyb.Pin('P5', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
print(p.value())

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([tresholds], merge = True):
        if ((blob.cx() >= 100 and blob.cx() <= 440) or (blob.cy() >= 120 and blob.cy() <= 360)):
            p.value(1)
            p2.value(1)
        else:
            p.value(0)
            p2.value(0)
        NewImage = img.draw_rectangle(blob.rect())
