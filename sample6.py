import pygame
from numpy.random import rand

import math
import numpy as np
import string

def unicodetoascii(text):

    uni2ascii = {
            ord('\xe2\x80\x99'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9d'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9e'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x9f'.decode('utf-8')): ord('"'),
            ord('\xc3\xa9'.decode('utf-8')): ord('e'),
            ord('\xe2\x80\x9c'.decode('utf-8')): ord('"'),
            ord('\xe2\x80\x93'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x92'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x94'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x98'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\x9b'.decode('utf-8')): ord("'"),

            ord('\xe2\x80\x90'.decode('utf-8')): ord('-'),
            ord('\xe2\x80\x91'.decode('utf-8')): ord('-'),

            ord('\xe2\x80\xb2'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb3'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb4'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb5'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb6'.decode('utf-8')): ord("'"),
            ord('\xe2\x80\xb7'.decode('utf-8')): ord("'"),

            ord('\xe2\x81\xba'.decode('utf-8')): ord("+"),
            ord('\xe2\x81\xbb'.decode('utf-8')): ord("-"),
            ord('\xe2\x81\xbc'.decode('utf-8')): ord("="),
            ord('\xe2\x81\xbd'.decode('utf-8')): ord("("),
            ord('\xe2\x81\xbe'.decode('utf-8')): ord(")"),

                            }
    return text.decode('utf-8').translate(uni2ascii).encode('ascii')

#Reading a story
f = open('story.txt', 'r')

listStory = []
listSubs = []
listVerbs = []
listObjs = []
listSub = {}
listVerb = {}
listObj = {}
listSubr = {}
listVerbr = {}
listObjr = {}

line = f.readline()
ks = 0
ko = 0
kv = 0
while line:
    #prepare a line
    line = unicodetoascii(line)
    
    line = line.translate(None, '\n')
    
    
    line = line.upper()

    k = 0
    while k < len(line) and (line[k] == ' '):
        k += 1
    line = line[k:]
    #saving
    if len(line) > 0:
        k = len(line)-1
        while k >=0 and (line[k] == ' '):
            k -= 1
        line = line[0:k+1]
        if line[0].isdigit():
            k = 0
            while k < len(line) and (line[k].isdigit() or line[k] == '.' or line[k] == ' '):
                k += 1
            line = line[k:]
            listStory.append(line)
            
        elif line[-1] == 'S' or line[-1] == 's':
            line = line.translate(None, ' ')
            line = line[:-2]
            ls = []
            for i in line.split(","):
                i = i.translate(None, ' ')
                if i in listSub:
                    ls.append(listSub[i])
                else:
                    listSub[i] = ks
                    listSubr[ks] = i
                    ls.append(ks)
                    ks += 1
            listSubs.append(ls)
        elif line[-1] == 'V' or line[-1] == 'v':
            line = line.translate(None, ' ')
            line = line[:-2]
            lv = []
            for i in line.split(","):
                i = i.translate(None, ' ')
                if i in listVerb:
                    lv.append(listVerb[i])
                else:
                    listVerb[i] = kv
                    listVerbr[kv] = i
                    lv.append(kv)
                    kv += 1
            listVerbs.append(lv)
        elif line[-1] == 'O' or line[-1] == 'o':
            line = line.translate(None, ' ')
            line = line[:-2]
            lo = []
            for i in line.split(","):
                if i in listObj:
                    lo.append(listObj[i])
                else:
                    listObj[i] = ko
                    listObjr[ko] = i
                    lo.append(ko)
                    ko += 1
            listObjs.append(lo)
    line = f.readline()

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Alpha')

gameExit = False

render_x = 80
render_y = 540
renderLength = 700
renderHeight = 500

storyVis = True
personVis = False
eventVis = False
story_n = len(listSub)
story = []
storyLength = len(listStory)
storyBegin = 0
storyPrev = 0
numVerbs = len(listVerb)
numObjs = len(listObj)
newLength = storyLength

zoom = 1
zoomRatio = 5
zoomMax = 100

focusPos = pygame.mouse.get_pos()
focusWidth = 200
fh = 20

bw = 100
bHomeFlag = 0
bSubFlag = 0
subFlag = 0
bVerbFlag = False
verbFlag = 0
bObjFlag = False
objFlag = 0
homeR = [render_x,render_y - renderHeight- 2*fh, render_x + bw ,render_y - renderHeight- 1*fh]
subR  = [render_x+1*bw, render_y - renderHeight- 2*fh, render_x + 2*bw , render_y - renderHeight- 1*fh]
verbR = [render_x+2*bw, render_y - renderHeight- 2*fh, render_x + 3*bw , render_y - renderHeight- 1*fh]
objR  = [render_x+3*bw, render_y - renderHeight- 2*fh, render_x + 4*bw , render_y - renderHeight- 1*fh]

detailLimit = 20

clock = pygame.time.Clock()


viss = {}
viso = {}
visv = {}

mx = 0

visso = np.zeros((story_n+1, numObjs+1))
vissv = np.zeros((story_n+1, numVerbs+1))
vissvo = np.zeros((story_n+1, numVerbs+1, numObjs + 1))
mxo = 0
mxs = 0
mxv = 0
mxv1 = 0


for i in range(storyLength):
	sub = listSubs[i]
	verb = listVerbs[i]
	obj = listObjs[i]
	
	#if len(obj) > 1:
	#	print i
	
	for s in sub:	
		if s in viss:
			viss[s] += 1
		else:
			viss[s] = 1
	for o in obj:
		if o in viso:
			viso[o] += 1
		else:
			viso[o] = 1
		mx = max(mx,viso[o])

	for v in verb:
		if v in visv:
			visv[v] += 1
		else:
			visv[v] = 1
		mxv = max(mxv,visv[v])

	story.append((sub,verb,obj))
	
	for s in sub:
		for o in obj:
			visso[s][o] += len(verb)
			mxo = max(mxo, visso[s][o])
			
			vissvo[s][verb[0]][o] = 1
	for s in sub:
		for v in verb:	
			vissv[s][v] += len(obj)
			mxv1 = max(mxv1, vissv[s][v])	

while not gameExit:
	#Parameters	
	w = 1.0*renderLength/newLength
	h = renderHeight/story_n

	focusPos = pygame.mouse.get_pos()
		
	fx = max(focusPos[0] - focusWidth/2,render_x)
	fx = min(fx, render_x+renderLength-focusWidth)
	fy = render_y - renderHeight - fh
	
	cx = int((focusPos[0] - render_x)/w)
	cy = int((render_y - focusPos[1])/h)

	focusR = [fx, fy, fx + focusWidth, fy+fh]

	if w > detailLimit:
		bSubFlag = True
		bVerbFlag = True
		bObjFlag = True
	else:
		bSubFlag = False
		bVerbFlag = False
		bObjFlag = False
		if storyVis:
			subFlag = False
			verbFlag = False
			objFlag = False
	if personVis:
		bVerbFlag = True
		bObjFlag = True
	
	#Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    gameExit = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			if focusPos[0] >= homeR[0] and focusPos[0] <= homeR[2] and focusPos[1] >= homeR[1] and focusPos[1] <= homeR[3]:
				storyBegin = 0
				storyPrev = 0
				newLength = storyLength
				storyVis = True
				personVis = False
				eventVis = False
			elif focusPos[0] >= focusR[0] and focusPos[0] <= focusR[2] and focusPos[1] >= focusR[1] and focusPos[1] <= focusR[3]:
				storyBegin = int(max((focusPos[0]-render_x-focusWidth/2)/w,0) + storyPrev)
				newLength = int(focusWidth/w+1)
				storyPrev = storyBegin
			elif focusPos[0] >= subR[0] and focusPos[0] <= subR[2] and focusPos[1] >= subR[1] and focusPos[1] <= subR[3]:
				if bSubFlag:
					subFlag = not subFlag
			elif focusPos[0] >= verbR[0] and focusPos[0] <= verbR[2] and focusPos[1] >= verbR[1] and focusPos[1] <= verbR[3]:
				if bVerbFlag:
					verbFlag = not verbFlag
			elif focusPos[0] >= objR[0] and focusPos[0] <= objR[2] and focusPos[1] >= objR[1] and focusPos[1] <= objR[3]:
				if bObjFlag:
					objFlag = not objFlag
			elif storyVis and focusPos[0] < render_x and focusPos[1] <= render_y and focusPos[1] >= render_y-renderHeight:
				storyVis = False
				personVis = True
				objFlag = True
				newLength = numObjs
				storyBegin = 0
				storyPrev = 0
				person = max(0,story_n - int((focusPos[1]-render_y+renderHeight)/h))
			elif storyVis and focusPos[0] > render_x and focusPos[1] <= render_y and focusPos[1] >= render_y-renderHeight:
				storyVis = False
				eventVis = True
				newLength = story_n
				currentEvent = storyBegin + int((focusPos[0]-render_x)/w)
				fo = 0
				storyBegin = 0
				storyPrev = 0
			elif eventVis:
				fo = min(max(int(render_y - focusPos[1])/20,0),len(story[currentEvent][2])-1)

	# New screen
	screen.fill(white)
	#Buttons
	#home
	pygame.draw.rect(screen, black, [render_x,render_y - renderHeight- 2*fh, bw ,fh], bHomeFlag)
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("HOME", 1, white)
	screen.blit(label, (render_x + bw/3, render_y - renderHeight- 1.8*fh))
	#Subject	
	pygame.draw.rect(screen, black, [render_x+bw, render_y - renderHeight- 2*fh, bw ,fh], not bSubFlag)
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("SUBJECT", 1, white)
	screen.blit(label, (render_x + bw + bw/3, render_y - renderHeight- 1.8*fh))
	#verb	
	pygame.draw.rect(screen, black, [render_x+2*bw, render_y - renderHeight- 2*fh, bw ,fh], not bVerbFlag)
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("VERB", 1, white)
	screen.blit(label, (render_x + 2*bw + bw/3, render_y - renderHeight- 1.8*fh))
	#object	
	pygame.draw.rect(screen, black, [render_x+3*bw, render_y - renderHeight- 2*fh, bw ,fh], not bObjFlag)
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("OBJECT", 1, white)
	screen.blit(label, (render_x + 3*bw + bw/3, render_y - renderHeight- 1.8*fh))

	#Grid
	pygame.draw.line(screen, black, [render_x,render_y],[render_x+renderLength,render_y])
	pygame.draw.line(screen, black, [render_x,render_y],[render_x,render_y-renderHeight])
	pygame.draw.line(screen, black, [render_x+renderLength,render_y],[render_x+renderLength,render_y-renderHeight])
	pygame.draw.rect(screen, black, [render_x,render_y - renderHeight- fh, renderLength,fh],1)

	if storyVis:
		#time
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("Time", 1, black)
		screen.blit(label, (render_x + 0.45*renderLength, render_y + 10))
		
		#focus range
		pygame.draw.rect(screen, blue, [fx, fy, focusWidth,fh],0)
		label = myfont.render("ZOOM", 1, white)
		screen.blit(label, (fx + focusWidth/3, fy+0.2*fh))
		fcx = min(max(focusPos[0], render_x), render_x + renderLength)
		fcy = max(min(focusPos[1], render_y), render_y-renderHeight)
		pygame.draw.line(screen, black, [render_x,fcy],[render_x+renderLength,fcy])
		pygame.draw.line(screen, black, [fcx, render_y],[fcx, render_y-renderHeight])
		#pygame.draw.rect(screen, blue, [fx, render_y - renderHeight, focusWidth,renderHeight],1)
		
		#labels
		myfont = pygame.font.SysFont("monospace", 8)
		for i in range(story_n):
			label = myfont.render("%s" %(listSubr[i]), 1, black)
			screen.blit(label, (render_x - 70, render_y-(i+1)*h + h/2))
		#time
		myfont = pygame.font.SysFont("monospace", 12)
		m = max(newLength/20,1)
		for i in range(newLength):
			if i%m == 0:
				label = myfont.render("%d" %(i+storyBegin), 1, black)
				screen.blit(label, (render_x+i*w, render_y+1))

		# story
		for i in range(newLength):
			#print i+storyBegin, storyLength
			if i+storyBegin < storyLength:
				event = story[i+storyBegin]
				for evs in event[0]:
					if evs < story_n:
						x = render_x + i*w
						y = render_y - (evs+1)*h
			
						#need to fix
						c = int(visv[event[1][0]]*255/mxv)
						pygame.draw.rect(screen, (255-c, c, 0), [x,y,w,h],0)
						if newLength < 200:
							pygame.draw.rect(screen, black, [x,y,w,h],1)
						if verbFlag:
							myfont = pygame.font.SysFont("monospace", 15)
							label = myfont.render("%s" %(listVerbr[event[1][0]]), 1, blue)
							screen.blit(label, (x + 0.01, y + 0.001*h))
						if objFlag:
							myfont = pygame.font.SysFont("monospace", 15)
							label = myfont.render("%s" %(listObjr[event[2][0]]), 1, blue)
							screen.blit(label, (x + 0.01, y + 0.85*h))
		#show the event		
		cx = min(max(0,cx+storyBegin),storyLength-1)
		cy = min(max(0,cy),story_n-1)
		stringEvent = listSubr[cy] + " | " + listVerbr[listVerbs[cx][0]]
		for i in listObjs[cx]:
			stringEvent += " | " + listObjr[i]
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(stringEvent, 1, black)
		screen.blit(label, (render_x, render_y + 20))
		#original event
		stringEvent = "#%d | " %(cx) + listStory[cx]
		myfont = pygame.font.SysFont("monospace", 10)
		label = myfont.render(stringEvent, 1, black)
		screen.blit(label, (10, render_y + 4*h))
	
	elif personVis:
		#label
		myfont = pygame.font.SysFont("monospace", 15)
		if objFlag:
			label = myfont.render("Objects", 1, black)
		else:
			label = myfont.render("Verbs", 1, black)
		screen.blit(label, (render_x + 0.45*renderLength, render_y + 10))
		
		
		#focus range
		pygame.draw.rect(screen, blue, [fx, fy, focusWidth,fh],0)
		label = myfont.render("ZOOM", 1, white)
		screen.blit(label, (fx + focusWidth/3, fy+0.2*fh))
		fcx = min(max(focusPos[0], render_x), render_x + renderLength)
		fcy = max(min(focusPos[1], render_y), render_y-renderHeight)
		pygame.draw.line(screen, black, [render_x,fcy],[render_x+renderLength,fcy])
		pygame.draw.line(screen, black, [fcx, render_y],[fcx, render_y-renderHeight])
		#pygame.draw.rect(screen, blue, [fx, render_y - renderHeight, focusWidth,renderHeight],1)

		#labels
		"""
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(listSubr[person], 1, black)
		screen.blit(label, (render_x - 70, render_y + 3*h))
		"""
		#time
		myfont = pygame.font.SysFont("monospace", 12)
		m = max(newLength/20,1)
		for i in range(newLength):
			if i%m == 0:
				label = myfont.render("%d" %(i+storyBegin), 1, black)
				screen.blit(label, (render_x+i*w, render_y+1))

		#quantity
		if objFlag:
			mxx = mxo
		else:
			mxx = mxv1
			
		myfont = pygame.font.SysFont("monospace", 12)
		for i in range(int(mxx)+1):
			label = myfont.render("%d" %(i), 1, black)
			screen.blit(label, (render_x - 15, render_y - (i*renderHeight/(mxx+1))))
		
		# story
		for i in range(newLength):
			event = i + storyBegin
			if objFlag and event <= numObjs:
				h1 = renderHeight/(mxo+1)*visso[person][event]
				x = render_x + i*w
				y = render_y

				pygame.draw.rect(screen, green, [x,y-h1,w,h1],0)
				if newLength < 200:
					pygame.draw.rect(screen, black, [x,y-h1,w,h1],1)
				if objFlag and h1 > 0 and w > detailLimit:
					myfont = pygame.font.SysFont("monospace", 15)
					label = myfont.render("%s" %(listObjr[event]), 1, blue)
					screen.blit(label, (x, y - h1-15))

			elif verbFlag and event <= numVerbs:
				h1 = renderHeight/(mxv1+1)*vissv[person][event]
				x = render_x + i*w
				y = render_y

				pygame.draw.rect(screen, green, [x,y-h1,w,h1],0)
				if newLength < 200:
					pygame.draw.rect(screen, black, [x,y-h1,w,h1],1)
				if verbFlag and h1 > 0 and w > detailLimit:
					myfont = pygame.font.SysFont("monospace", 15)
					label = myfont.render("%s" %(listVerbr[event]), 1, blue)
					screen.blit(label, (x, y - h1-15))
		
		#show the event		
		stringEvent = listSubr[person]
		stringDetail = ""
		
		
		if objFlag:
			stringDetail = "VERBS:"
			cx = min(max(0,cx + storyBegin),numObjs-1)
			stringEvent += " | " + listObjr[cx]
			for i in range(numVerbs):
				if vissvo[person][i][cx] == 1:
					stringDetail += " >" + listVerbr[i]
		elif verbFlag:
			stringDetail = "OBJECTS: "
			cx = min(max(0,cx + storyBegin),numVerbs-1)
			stringEvent += " | " + listVerbr[cx]
			for i in range(numObjs):
				if vissvo[person][cx][i] == 1:
					stringDetail += " >" + listObjr[i]
		
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(stringEvent, 1, black)
		screen.blit(label, (render_x, render_y + 20))
		#details
		myfont = pygame.font.SysFont("monospace", 10)
		label = myfont.render(stringDetail, 1, black)
		screen.blit(label, (render_x, render_y + 40))
		
		
	elif eventVis:
		objs = story[currentEvent][2]		#need to fix
		#subject
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("Subjects", 1, black)
		screen.blit(label, (render_x + 0.45*renderLength, render_y + 10))
		
		#focus range
		pygame.draw.rect(screen, blue, [fx, fy, focusWidth,fh],0)
		label = myfont.render("ZOOM", 1, white)
		screen.blit(label, (fx + focusWidth/3, fy+0.2*fh))
		fcx = min(max(focusPos[0], render_x), render_x + renderLength)
		fcy = max(min(focusPos[1], render_y), render_y-renderHeight)
		pygame.draw.line(screen, black, [render_x,fcy],[render_x+renderLength,fcy])
		pygame.draw.line(screen, black, [fcx, render_y],[fcx, render_y-renderHeight])
		#pygame.draw.rect(screen, blue, [fx, render_y - renderHeight, focusWidth,renderHeight],1)

		#labels
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("#%d" %(currentEvent), 1, black)
		screen.blit(label, (render_x - 70, render_y + 3*h))
		#several objects
		myfont = pygame.font.SysFont("monospace", 10)
		for i in range(len(objs)):
			label = myfont.render(listObjr[objs[i]], 1, black)
			screen.blit(label, (3, render_y - (i+1)*20))
		
		label = myfont.render("CHOOSE:", 1, black)
		screen.blit(label, (3, render_y - (len(objs)+1)*20))
		#time
		myfont = pygame.font.SysFont("monospace", 12)
		m = max(newLength/20,1)
		for i in range(newLength):
			if i%m == 0:
				label = myfont.render("%d" %(i+storyBegin), 1, black)
				screen.blit(label, (render_x+i*w, render_y+1))
		
		#quantity
		myfont = pygame.font.SysFont("monospace", 12)
		for i in range(int(mxo)+1):
			label = myfont.render("%d" %(i), 1, black)
			screen.blit(label, (render_x - 15, render_y - (i*renderHeight/(mxo+1))))

		# story
		obj = objs[fo]
		for i in range(newLength):
			person = i + storyBegin
			if person <= story_n:
				h1 = renderHeight/(mxo+1)*visso[person][obj]
				x = render_x + i*w
				y = render_y

				pygame.draw.rect(screen, green, [x,y-h1,w,h1],0)
				if newLength < 200:
					pygame.draw.rect(screen, black, [x,y-h1,w,h1],1)
					if subFlag and h1 > 0:
						myfont = pygame.font.SysFont("monospace", 15)
						label = myfont.render("%s" %(listSubr[person]), 1, blue)
						screen.blit(label, (x, y - h1-15))
	
		cx = min(max(0,cx + storyBegin),story_n-1)
		#todo
		stringEvent = listSubr[cx] + " | " + listObjr[obj]
		
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(stringEvent, 1, black)
		screen.blit(label, (render_x, render_y + 20))
		
		#show details
		stringDetail = ""
		
		stringDetail = "VERBS:"
		cx = min(max(0,cx + storyBegin),story_n-1)
		for i in range(numVerbs):
			if vissvo[cx][i][obj] == 1:
				stringDetail += " >" + listVerbr[i]
		#details
		myfont = pygame.font.SysFont("monospace", 10)
		label = myfont.render(stringDetail, 1, black)
		screen.blit(label, (render_x, render_y + 40))
		
	pygame.display.update()

	clock.tick(30)
    

pygame.quit()
quit()





