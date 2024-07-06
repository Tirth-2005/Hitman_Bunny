import os

FPS = 100
SCREENSIZE = (640, 480)

IMAGE_PATH = {
    'rabbit':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/dude.png'),
    'rabbit_2':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/dude2.png'),
    'grass':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/grass.png'),
    'castle':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/castle.png'),
    'arrow':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/bullet.png'),
    'badguy':[os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/%d.png' % i) for i in range(1, 5)],
    'healthbar':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/healthbar.png'),
    'health':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/health.png'),
    'gameover':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/gameover.png'),
    'youwin':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/youwin.png'),
    'start':os.path.join(os.getcwd(), 'Hitman Bunny/resources/images/start.png')
}

AUDIO = {
    'hit':os.path.join(os.getcwd(), 'Hitman Bunny/resources/audio/explode.wav'),
    'enemy':os.path.join(os.getcwd(), 'Hitman Bunny/resources/audio/enemy.wav'),
    'moonlight':os.path.join(os.getcwd(), 'Hitman Bunny/resources/audio/moonlight.wav'),
    'shoot':os.path.join(os.getcwd(), 'Hitman Bunny/resources/audio/shoot.wav')
} 