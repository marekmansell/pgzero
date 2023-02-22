import serial

TITLE = "PyGame Zero battle"
WIDTH = 640
HEIGHT = 480

GAME_OVER = 0
PLAYING = 1
GAME_WON = 2

port = "COM4"
microbit_serial = serial.Serial(port, baudrate=115200)

ball = Actor("ball")
ball.x = WIDTH / 2
ball.y = HEIGHT / 2
ball.dx = 1
ball.dy = -1
ball.speed = 3

serial_msg = "N"

hearts = []
for i in range(3):
    heart = Actor("heart")
    heart.y = HEIGHT - 30
    heart.x = WIDTH - 30 - 40 * i
    hearts.append(heart)

bricks = []
for col in range(10):
    for row in range(4):
        brick = Actor("brick.red")
        brick.left = brick.width * col
        brick.top = brick.height * row
        bricks.append(brick)

paddle = Actor("paddle")
paddle.x = WIDTH / 2
paddle.bottom = HEIGHT
paddle.speed = 7

game_status = PLAYING


def update():
    global game_status, hearts, serial_msg

    ball.x += ball.dx * ball.speed
    ball.y += ball.dy * ball.speed

    if ball.top <= 0:
        ball.dy = 1

    if ball.right >= WIDTH:
        ball.dx = -1

    if ball.left <= 0:
        ball.dx = 1

    if ball.bottom >= HEIGHT:
        # ball.dy = -1
        # game_status = GAME_OVER

        if not len(hearts):
            game_status = GAME_OVER
        else:
            hearts.pop()
            ball.dy = -1

    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball.dy *= -1
            sounds.hit01.play()
            break

    if ball.colliderect(paddle):
        ball.dy *= -1
        sounds.hit02.play()

    if microbit_serial.inWaiting() > 0:
        serial_msg = microbit_serial.read().decode()

    if keyboard.right == True or serial_msg == "B":
        paddle.x = paddle.x + paddle.speed
        if paddle.right >= WIDTH:
            paddle.right = WIDTH

    if keyboard.left == True or serial_msg == "A":
        paddle.x = paddle.x - paddle.speed
        if paddle.left <= 0:
            paddle.left = 0

    if len(bricks) == 0:
        game_status = GAME_WON




def draw():
    if game_status == GAME_OVER:
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2), color="white")
        return

    if game_status == GAME_WON:
        screen.draw.text("You Win!", center=(WIDTH / 2, HEIGHT / 2), color="white")
        return

    screen.clear()
    screen.blit("background", (0, 0))

    for b in bricks:
        b.draw()

    ball.draw()
    paddle.draw()

    for heart in hearts:
        heart.draw()

    screen.draw.text(
        str(40 - len(bricks)), topright=(WIDTH - 20, 10), color="white", fontsize=48
    )
