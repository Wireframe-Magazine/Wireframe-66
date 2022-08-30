# Excitebike
import pgzrun, time

startTime = time.time()
bike = Actor('bike0',center=(150,350), anchor=('center','bottom'))
bike.speed = 1
bike.frame = bike.direction = 0
bike.laneY = 375
score = trackPos = gametime = lastLap = 0
track = [0,2,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,0,
         0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,1,1,1,0,
         0,0,1,0,0,0,0,1,0,0,0,2,0,0,0,0,0,0,0]
muck = [0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,2,1,
         0,0,4,0,1,0,0,0,0,2,0,0,0,3,0,0,0,0,0,
         3,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0]

def draw():
    screen.blit("background", (0, 0))
    drawTrack()
    bike.draw()
    screen.draw.text("LAP TIME: "+str(int(time.time() - startTime)), (20, 555),color=(255,255,255) , fontsize=50)
    screen.draw.text("LAST LAP: "+str(lastLap), topright = (780, 555),color=(255,255,255) , fontsize=50)

def update():
    global trackPos, gametime, startTime, lastLap
    if keyboard.right and bike.y == bike.laneY: bike.speed = limit(bike.speed+0.1, 1, 5)
    if keyboard.left and bike.y == bike.laneY: bike.speed = limit(bike.speed-0.1, 1, 5)
    trackPos -= bike.speed
    if(trackPos < -4800):
        trackPos = 0
        lastLap = int(time.time() - startTime)
        startTime = time.time()
    if round(bike.y/2) == round(bike.laneY/2):
        bike.y = bike.laneY
        bike.angle = 0
    if bike.direction != 0:
        if bike.y <= 375 or bike.y >= 525 or bike.y == bike.laneY:
            bike.direction = 0
        else: bike.y += bike.direction*2
    if(gametime%(int(8-bike.speed)) == 0): bike.frame = 1 - bike.frame
    a = bike.angle
    bike.image = "bike" + str(bike.frame)
    bike.angle = a
    checkBikeRamp()

def on_key_down(key):
    if key.name == "UP":
        bike.direction = -1
        bike.laneY = limit(bike.laneY-50, 375, 525)
    if key.name == "DOWN":
        bike.direction = 1
        bike.laneY = limit(bike.laneY+50, 375, 525)
    bike.y += bike.direction
        
def drawTrack():
    trackOffset = trackPos%100
    trackBlock = int(-trackPos/100)
    if trackOffset == 0: trackBlock -= 1
    for t in range(0, 9):
        screen.blit("crowd1", ((t*100)+trackOffset-100, 0))
        screen.blit("rock1", ((t*100)+trackOffset-100, 270))
        screen.blit("rock1", ((t*100)+trackOffset-50, 270))
        if track[trackBlock+t] == 0: screen.blit("track1", ((t*100)+trackOffset-100, 300))
        if track[trackBlock+t] == 1: screen.blit("jump1", ((t*100)+trackOffset-100, 300))
        if track[trackBlock+t] == 2: screen.blit("track2", ((t*100)+trackOffset-100, 300))
        if muck[trackBlock+t] > 0: screen.blit("muck1", ((t*100)+trackOffset-100, 295+(muck[trackBlock+t])*50))
        
def checkBikeRamp():
    tp = trackPos + 25
    trackOffset = tp%100
    trackBlock = int((-tp)/100)+2
    trackheight = 0
    if trackOffset == 0: trackBlock -= 1
    if track[trackBlock] == 1:
        trackheight = (100-trackOffset)
        if bike.y >= bike.laneY-trackheight:
            bike.y = bike.laneY-trackheight
            if bike.angle < 45: bike.angle += bike.speed
        if bike.angle < -25:
            bike.speed = 1
            bike.angle = 0
        if bike.angle >= -25 and bike.angle < 0: bike.angle = 0
    else:
        if int(bike.y) == int(bike.laneY) and bike.angle < -25:
            bike.angle = 0
            bike.speed = 1
    if bike.y < bike.laneY-trackheight and bike.direction != 1:
        bike.y += (2-(bike.speed/3))
        if bike.direction == 0: bike.angle -= 1
        if bike.speed > 1: bike.speed -= 0.02
    muckLane = int((bike.laneY-375)/50)+1
    if muck[trackBlock] == muckLane and int(bike.y) == int(bike.laneY) : bike.speed = bike.speed/1.1
    
def limit(n, minn, maxn):
    return max(min(maxn, n), minn)

pgzrun.go()
