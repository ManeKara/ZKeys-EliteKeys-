import pygame
import random #delete these later if unused 
import copy
import os
import math 
import nltk.corpus
import asyncio
from nltk.corpus import words 



try:
    nltk.data.find('corpora/words.zip')
except LookupError:
    print("Downloading NLTK 'words' corpus...")
    nltk.download('words')
    
wordList = words.words()
lenIndexes = []
length = 1

#wordlist sorting
wordList.sort(key=len)
for i in range (len(wordList)):
    if len(wordList[i]) > length:
        length += 1
        lenIndexes.append(i)
lenIndexes.append(len(wordList))
print(lenIndexes)






#from ZKey import introAnim, Button, logoFlashDir, sparkFlashDir, elecFlashDir, gameScreen, gameTimer, fps
base_dir = os.path.dirname(__file__)
assets_dir = os.path.join(base_dir,"assets")
print("Current Working Directory:", os.getcwd())

pygame.mixer.init()
pygame.mixer.set_num_channels(8)  # Set the number of mixer channels
announcerChannel = pygame.mixer.Channel(0)  # Dedicated to announcer sounds
hitSoundChannel = pygame.mixer.Channel(1) 
typeSoundChannel = pygame.mixer.Channel(3) 


pygame.init()
width = 1920
height = 1080
gameScreen = pygame.display.set_mode([width,height])
pygame.display.set_caption("ZKey 1.0.0") #update constantly
surface = pygame.Surface((0,0), pygame.SRCALPHA)
gameTimer = pygame.time.Clock()
fps = 60
background = (55, 68, 84)

#game stuff
mult = 0
lives = 5
level = 1
activeString = ""
submit = ""
score = 1
highScore = 1
wordObjects= []
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
choices = [False, False, False, True, True, True, False] #word lengths top include, from 2 to 8

#loading stuff in. Music will be made by me, but that will be later 
ZLogo = pygame.image.load(os.path.join(assets_dir, "ZLogoPixel.png"))
scaledZLogo = pygame.transform.scale(ZLogo, (500, 500))
logoFlashDir = os.path.join(assets_dir, "LogoFlash")
sparkFlashDir = os.path.join(assets_dir, "Spark")
elecFlashDir = os.path.join(assets_dir, "Electricity")
startFont = pygame.font.Font(os.path.join(assets_dir, "Fonts", "VCR_OSD_MONO_1.001.ttf"), 50)
titlePng = pygame.image.load(os.path.join(assets_dir, "Keys.png"))
gameFont = pygame.font.Font(os.path.join(assets_dir, "Fonts", "VCR_OSD_MONO_1.001.ttf"), 80)
typeSound = pygame.mixer.Sound(os.path.join(assets_dir, "Sounds", "typesound.wav"))
typeSound.set_volume(0.25)
hitSoundDir = os.path.join(assets_dir, "Sounds", "HitSounds")
superCombo = pygame.mixer.Sound(os.path.join(assets_dir, "Sounds", "Announcer", "supercombo.wav"))

hyperCombo = pygame.mixer.Sound(os.path.join(assets_dir, "Sounds", "Announcer", "hypercombo.wav"))

monsterCombo = pygame.mixer.Sound(os.path.join(assets_dir, "Sounds", "Announcer", "monstercombo.wav"))

ultraCombo = pygame.mixer.Sound(os.path.join(assets_dir, "Sounds", "Announcer", "ultracombo.wav"))

   
class Word:
    def __init__(self, text, color, speed, y_pos, x_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
        self.color = color
        

    def draw(self):
        gameScreen.blit(gameFont.render(self.text, True, self.color), (self.x_pos, self.y_pos))
        activeStringLen = len(activeString)
        if activeString == self.text[:activeStringLen]:
            gameScreen.blit(gameFont.render(activeString, True, "brown1"), (self.x_pos, self.y_pos))
            
    def update(self):
        self.x_pos -= self.speed 
        
    
    
    
    
    
class Button: #reusable for buttons 
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text =  text
        self.clicked = clicked
        self.surf = surf
        
    def draw(self):
        rectangle = pygame.draw.rect(self.surf, (45, 89, 135), (self.x_pos, self.y_pos, 250, 60))
        if rectangle.collidepoint(pygame.mouse.get_pos()):
            pressedButtons = pygame.mouse.get_pressed()
            if pressedButtons[0]:
                pygame.draw.rect(self.surf, "cornsilk", (self.x_pos, self.y_pos, 250, 60))
                self.clicked = True
            else:
                pygame.draw.rect(self.surf, "ivory2", (self.x_pos, self.y_pos, 250, 60)) 
        pygame.draw.rect(self.surf, "white", (self.x_pos-3, self.y_pos-3, 256, 66), 3)
        self.surf.blit(startFont.render(self.text, True, 'white'), (self.x_pos + 10, self.y_pos + 5))        

def playHitSound(soundFolder):
    # Check if the folder exists
    if not os.path.exists(soundFolder):
        print(f"Sound folder '{soundFolder}' not found.")
        return
    
    # Load all sound files into an array
    soundFiles = [os.path.join(soundFolder, file) for file in os.listdir(soundFolder) if file.endswith('.wav')]
    
    # Check if the folder contains sound files
    if not soundFiles:
        print(f"No sound files found in '{soundFolder}'.")
        return
    
    # Randomly pick a sound file
    selectedSound = random.choice(soundFiles)
    
    # Load and play the sound
    try:
        sound = pygame.mixer.Sound(selectedSound)
        sound.set_volume(0.5)  # Adjust volume if needed
        hitSoundChannel.play(sound)
    except pygame.error as e:
        print(f"Error loading sound: {e}")
        

def introAnim(gifFolder, gifFolder2): #cool animation
    images = []
    currentImage = 0
    frameCount = 0
    animSpeed = 2
    animSpeed2 = 2
    animSpeed3 = 5
    pygame.draw.rect(gameScreen, "ivory2", [0, height - 100, width, 100], 0) #load the blue background
    
    #load images into images array
    for file in sorted(os.listdir(gifFolder)):
        filePath = os.path.join(gifFolder, file)
        img = pygame.image.load(filePath)
        scaled_img = pygame.transform.scale(img, (3000, 1688))
        images.append(scaled_img)
    
    while currentImage < len(images):
        gameScreen.fill((0,0,0)) #clear the screen with the background color
        gameScreen.blit(images[currentImage], (-790,-450))
        frameCount += 1
        if frameCount >= animSpeed:
            frameCount = 0
            currentImage += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        pygame.display.flip()
        gameTimer.tick(fps)
    
    flashSurface = pygame.Surface((1920,1080), pygame.SRCALPHA)
    flashSurface.fill((255,255,255,255))  # Fill with white and full alpha
    logo_x = width  # Start position off-screen to the right
    logo_v = -60    # Initial speed (negative to move left)
    deceleration = 0.97  # Deceleration factor
    
    
    while flashSurface.get_alpha() > 0:
        # Update flashSurface alpha
        if flashSurface.get_alpha() > 0:
            flashSurface.set_alpha(max(0, flashSurface.get_alpha() - 3))
        
        # Clear screen and draw elements
        gameScreen.fill(background)
        gameScreen.blit(scaledZLogo, (logo_x, 300))  # Draw the logo at the new position
        gameScreen.blit(flashSurface, (0,0))
        
        # Update logo position and speed
        if logo_v <= 0:
            logo_x += logo_v
            logo_v += deceleration  # Decelerate the logo
        else:
            logo_v = 0  # Stop moving if velocity is very small
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        pygame.display.flip()
        gameTimer.tick(fps)
    
    
    
    for file in sorted(os.listdir(gifFolder2)):
        filePath = os.path.join(gifFolder2, file)
        img = pygame.image.load(filePath)
        scaled_img = pygame.transform.scale(img, (3000, 3000))
        images.append(scaled_img)
    
    while currentImage < len(images):
        gameScreen.fill(background)
        gameScreen.blit(scaledZLogo, (logo_x, 300))
        gameScreen.blit(titlePng, (530,480))
        gameScreen.blit(images[currentImage], (-790,-1200))
        frameCount += 1
        if frameCount >= animSpeed2:
            frameCount = 0
            currentImage += 1
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.flip()
        gameTimer.tick(fps)
    
    waitingForStart = True
    playButton = Button(1500, 540, "Play >>>", False, gameScreen)
    
    while waitingForStart:
    # Clear the screen and redraw everything
        gameScreen.fill(background)
        gameScreen.blit(scaledZLogo, (logo_x, 300))
        gameScreen.blit(titlePng, (530, 480))

        # Draw the Play button
        playButton.draw()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Check if the Play button has been clicked
        if playButton.clicked:
            waitingForStart = False  # Exit the loop

        # Update the display (only once per frame)
        pygame.display.flip()
        gameTimer.tick(fps)

    print("Play button clicked! Exiting intro...")
    return playButton.clicked

def newLevel():
    global lastWordSpawnTime
    wordObj = []
    include = []
    verticalSpacing = (height - 300) // level #making sure words are above bottom border
    if True not in choices: #incase all the lengths of words are off (self error check)
        choices[0] = True #set 2 letter words on by default
    for i in range (len(choices)):
        if choices[i]:
            include.append((lenIndexes[i], lenIndexes[i+1]))
    for i in range(level):
        
        speed = random.uniform(0.1, 0.5)
        color = "ivory2"
        start = 10 + (i * verticalSpacing)
        end = (i + 1) * verticalSpacing
        if start >= end:
            y_pos = start
        else:
            y_pos = random.randint(start, end)
        x_pos = random.randint(width, width + 1000)
        indexSel = random.choice(include) 
        index = random.randint(indexSel[0], indexSel[1])
        text = wordList[index].lower()
        newWord = Word(text, color, speed, y_pos, x_pos)
        wordObj.append(newWord)
    
    
    return wordObj



def actualGame():
    
    dynamicFont = pygame.font.Font(os.path.join(assets_dir, "Fonts", "VCR_OSD_MONO_1.001.ttf"), int(80 + (mult / 2)))
    
    gameScreen.fill(((55 + mult), 68, 84))
    pygame.draw.rect(gameScreen, "ivory2", [0, height - 200, width, 200], 0)
    pygame.draw.rect(gameScreen, background, [600, height - 200, 10, 200], 0)
    gameScreen.blit(gameFont.render(f'Level: {level}', True, "black"), (80, height - 140)) #level text
    gameScreen.blit(gameFont.render(f'{activeString}', True, "black"), (650, height - 140)) #activeString text
    gameScreen.blit(gameFont.render(f'Lives: {lives}', True, "ivory2"), (80, height - 1050)) #lives
    gameScreen.blit(gameFont.render(f'Score: {score}', True, "ivory2"), (580, height - 1050)) #score 
    if 1 < mult < 15:
        gameScreen.blit(dynamicFont.render(f'x{mult}', True, (238, 238, 224)), (1400, height - 1050)) #multi
    elif 15 <= mult < 30:
        gameScreen.blit(dynamicFont.render(f'x{mult}!', True, (242, 206, 195)), (1400, height - 1050))
        if mult == 15:
            announcerChannel.play(superCombo)
    elif 30 <= mult  < 45:
        gameScreen.blit(dynamicFont.render(f'x{mult}!!', True, (229, 129, 99)), (1400, height - 1050))
        if mult == 30:
            announcerChannel.play(hyperCombo)
    if 45 <= mult < 60:
        gameScreen.blit(dynamicFont.render(f'x{mult}!!!', True, (211, 69, 27)), (1400, height - 1050))
        if mult == 45:
            announcerChannel.play(monsterCombo)
    if 60 <= mult:
        gameScreen.blit(dynamicFont.render(f'x{mult}!!!!', True, (162, 37, 0)), (1400, height - 1050))
        if mult == 60:
            announcerChannel.play(ultraCombo)         
        
    return True 
fade_words = []

def checkAnswer(scor):
    global mult
    correct = False
    for word in wordObjects[:]:  # Use a copy to avoid modifying the list during iteration
        if word.text == submit:
            mult += 1
            points = word.speed * len(word.text) + 10 * (len(word.text) / 3) * mult
            scor += int(points)
            word.speed = 0  # Stop the word from moving
            playHitSound(hitSoundDir)
            fade_words.append((word, 255))  # Add word to fade list with full alpha
            wordObjects.remove(word)  # Remove from active words
            correct = True
    if not correct:
        mult = 0
    return scor

def renderFadingWords():
    global fade_words
    updated_fade_words = []  # Temporary list to store updated words
    for word, alpha in fade_words:
        fade_surface = gameFont.render(word.text, True, "black")
        fade_surface.set_alpha(alpha)
        gameScreen.blit(fade_surface, (word.x_pos, word.y_pos))
        alpha -= 1  # Reduce alpha gradually
        if alpha > 0:
            updated_fade_words.append((word, alpha))  # Keep the word if it still needs fading
    fade_words = updated_fade_words  # Update the main fade_words list
    
    
# -------------------------------------------- MAIN GAME LOGIC vvvvvvvvvvvv
running = True #basic variable to tell the code that the game is meant to be running
gameState = "intro"
introShown = False
nextWordTimer = pygame.time.get_ticks()  # Initialize word spawn timer
spawn_interval = 1000
while running:
    
    if introShown == False:
        startGame = introAnim(logoFlashDir, sparkFlashDir)
        introShown = True
        if startGame:
            gameState = "game"
            wordOjects = newLevel() #first level 
        
    if gameState == "game":
        actualGame()
        
    
    
    for word in wordObjects:
        word.draw()
        word.update()
        if word.x_pos < -400:
            wordObjects.remove(word)
            lives -= 1
            mult = 0
    renderFadingWords()

    if len(wordObjects) <= 0:
        level += 1
        wordObjects = newLevel()
        
    if submit != "":
        init = score
        score = checkAnswer(score)
        submit = ""
        if init == score:
            #play wrong entry sound
            pass
    
    
        
    
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #pygame function, I believe it's the same as the red x idk
            running = False
        if event.type == pygame.KEYDOWN:
            if event.unicode.lower() in letters:
                typeSoundChannel.play(typeSound)
                activeString += event.unicode.lower()
            if event.key == pygame.K_BACKSPACE and len(activeString) > 0:
                activeString = activeString[:-1]
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                submit = activeString
                activeString = ""
                
    
    
    pygame.display.flip() #updates the entire screen. idk why it's called "flip" 
pygame.quit()