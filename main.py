import pygame, sys, os, math, random
import Menu, Mountain, Pool, Fish, Alien, Bird, Player, Bullet

#copy some existing player

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("?")
fullscreen = False

background = pygame.Surface((640, 480))
background.fill((0,255,0))

f = pygame.font.Font("freesansbold.ttf", 32)
clock = pygame.time.Clock()
start = 0
level = 0

up_down = False
down_down = False
left_down = False
right_down = False

up_key = pygame.K_w
down_key = pygame.K_s
left_key = pygame.K_a
right_key = pygame.K_d

#sounds
#pygame.mixer.music.load(os.path.join("sounds", "music.mid"))
sfx_slap = pygame.mixer.Sound(os.path.join("sounds", "slap.wav"))


images = {
	'f': pygame.image.load(os.path.join("images", "fish.png")).convert_alpha(),
	'm': pygame.image.load(os.path.join("images", "mountain.png")).convert_alpha(),
	'a': pygame.image.load(os.path.join("images", "alien.png")).convert_alpha(),
	'b': pygame.image.load(os.path.join("images", "bird.png")).convert_alpha(),
}

Fish.getstuff((images['f'], None), sfx_slap)
Mountain.getstuff((images['m'], None))#,sounds)
Alien.getstuff((images['a'], None))
Bird.getstuff((images['b'], None))

Player.getstuff((images['b'], None))
Bullet.getstuff((images['f'], None), sfx_slap)

player = Player.Player()
fish = Fish.Fish((0,0))
mountains = pygame.sprite.Group()
aliens = pygame.sprite.Group()
pools = pygame.sprite.Group()
birds = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def newlevel(level):
	fish.active = False
	mountains.empty()
	aliens.empty()
	pools.empty()
	birds.empty()

	for x in xrange(level):
		pools.add(Pool.Pool((random.randint(100,540), random.randint(100,380))))


def newlevel2(level):
	global player

	mountains.empty()
	aliens.empty()
	bullets.empty()

	mountains.add(Mountain.Mountain((0,0)))
	for m in mountains:
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.slap()
		m.rect.center = (320,240)
		m.drop()

	player = Player.Player()



menus = (
		Menu.Menu(0, ("Start", "Options", "Play Other Game"), (10, 1, 20), f, (100,100), 20, (255,255,255), 0, (255,0,0)),
		Menu.Menu(1, ("Fullscreen", "BACK"), (2, 0), f, (150,100), 30, (255,255,255), 0, (255,0,0))
)
activemenu = menus[0]

while 1:
	mouse = pygame.mouse.get_pos()
	delta = clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEMOTION:
			activemenu.checkmouse(mouse)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			activemenu.checkmouse(mouse)
		elif event.type == pygame.MOUSEBUTTONUP:
			if activemenu.checkmouse(mouse):
				if activemenu.highlight != 0:
					start = activemenu.nodes[activemenu.highlight-1]
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				activemenu.movehighlight(-1)
			elif event.key == pygame.K_DOWN:
				activemenu.movehighlight(1)
			elif event.key == pygame.K_RETURN:
				if activemenu.highlight != 0:
					start = activemenu.nodes[activemenu.highlight-1]
			elif event.key == pygame.K_ESCAPE:
				if activemenu.id == 0:
					sys.exit()
				else:
					for n in activemenu.nodes:
						if n < activemenu.id:
							start = n
							break
	if start != activemenu.id:

		if start == 2 and activemenu.highlight == 1:
			fullscreen = not fullscreen
			if fullscreen:
				screen = pygame.display.set_mode((640,480), pygame.FULLSCREEN)
			else:
				screen = pygame.display.set_mode((640,480))
			start = 1

		for menu in menus:
			if menu.id == start:
				activemenu = menu
				break

	screen.blit(background, (0,0))
	#if activemenu.id == 0: show title thing, else 1: show stuff, etc
	activemenu.draw(screen)
	pygame.display.flip()

	while start == 10:
		delta = clock.tick()
		endgame = 0
		pause = False
		endgame = False
		nextlevel = False
		level = 1
		newlevel(level)
		pygame.event.set_grab(1)

		while not endgame:
			while pause:
				delta = clock.tick(60)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							pygame.event.set_grab(1)
							pause = False
							delta = clock.tick()
						elif event.key == pygame.K_ESCAPE:
							pause = False
							endgame = True
							start = 0
			if not endgame:
				delta = clock.tick(60)
				#print float(1000)/delta

				mouse1 = pygame.mouse.get_pos()
				fish.update(mouse1)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if event.button == 1:
							fish.slap(mountains, aliens, birds, pools)
						elif event.button == 3:
							fish.active = False
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
							pause = True
							pygame.event.set_grab(0)

				if len(pools) > len(mountains) + len(birds) and len(birds) < 5:
					birds.add(Bird.Bird(birds))

				mountains.update(mouse1, aliens)
				birds.update()
				pools.update(mountains)
				aliens.update()

#win/lose:
				brk = False
				for p in pools:
					if p.active:
						brk = True
						break
				if not brk:
					nextlevel = True

				if not nextlevel:
					w = 0
					for p in pools:
						if p.active:
							w += p.radius**2 * math.pi
					if w > 150000:
						endgame = True
						nextlevel = True

#draw
				screen.blit(background, (0,0))

				for p in pools:
					p.draw(screen)
				for m in mountains:
					m.draw(screen)
				for a in aliens:
					a.draw(screen)
				for b in birds:
					b.draw(screen)
				fish.draw(screen)

				pygame.display.flip()

			if nextlevel:
				windowtimer = 0
				while windowtimer < 2000 and start != 0:
					windowtimer += clock.tick(60)
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()

				if not endgame:
					level += 1
				newlevel(level)

				nextlevel = False


	while start == 20:
		delta = clock.tick()
		endgame = 0
		pause = False
		endgame = False
		nextlevel = False
		newlevel2(level)
		pygame.event.set_grab(1)

		while not endgame:
			while pause:
				delta = clock.tick(60)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE:
							pygame.event.set_grab(1)
							pause = False
							delta = clock.tick()
						elif event.key == pygame.K_ESCAPE:
							pause = False
							endgame = True
							start = 0
			if not endgame:
				delta = clock.tick(60)
				#print float(1000)/delta

				mouse1 = pygame.mouse.get_pos()
				fish.update(mouse1)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if event.button == 1:
							player.shoot(mouse1, bullets)
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
							pause = True
							pygame.event.set_grab(0)
						elif event.key == up_key:
							up_down = True
							if down_down:
								player.stopmove(0,1)
							else:
								player.move(0,-1)
						elif event.key == down_key:
							down_down = True
							if up_down:
								player.stopmove(0,-1)
							else:
								player.move(0,1)
						elif event.key == left_key:
							left_down = True
							if right_down:
								player.stopmove(1,0)
							else:
								player.move(-1,0)
						elif event.key == right_key:
							right_down = True
							if left_down:
								player.stopmove(-1,0)
							else:
								player.move(1,0)
					elif event.type == pygame.KEYUP:
						if event.key == up_key:
							up_down = False
							if down_down:
								player.move(0,1)
							else:
								player.stopmove(0,-1)
						elif event.key == down_key:
							down_down = False
							if up_down:
								player.move(0,-1)
							else:
								player.stopmove(0,1)
						elif event.key == left_key:
							left_down = False
							if right_down:
								player.move(1,0)
							else:
								player.stopmove(-1,0)
						elif event.key == right_key:
							right_down = False
							if left_down:
								player.move(-1,0)
							else:
								player.stopmove(1,0)

				for m in mountains:
					if random.randint(0,9) == 0:
						aliens.add(Alien.Alien((0,0), m, True))

				mountains.update(mouse1, aliens)
				birds.update()
				pools.update(mountains)
				aliens.update()
				bullets.update(aliens)
				player.update()

#lose
				for m in mountains:
					if m.rect.top < 0 and m.rect.left < 0:
						nextlevel = True

#draw
				screen.blit(background, (0,0))

				for m in mountains:
					m.draw(screen)
				for a in aliens:
					a.draw(screen)
				for b in bullets:
					b.draw(screen)
				player.draw(screen)

				pygame.display.flip()

			if nextlevel:
				windowtimer = 0
				while windowtimer < 2000 and start != 0:
					windowtimer += clock.tick(60)
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()

				newlevel2(level)

				nextlevel = False
