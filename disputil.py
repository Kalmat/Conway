#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function    # (at top of module)
import os
import sys
import platform
import io
import requests
import pygame
import time
import traceback


####################################################################
def InitDisplay(x=None, y=None, windowed=False, hideMouse=True, clearScreen=False, icon=None, caption=None):
    " Initializes a new pygame screen using the framebuffer "
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679

    archOS = platform.platform()
    print("System Architecture Family:", archOS)
    disp_no = os.getenv("DISPLAY")
    if disp_no:
        print("X Display = {0}".format(disp_no), " - ", end="")
    else:
        print("Display driver: ", end="")

    # Check which frame buffer drivers are available
    if "Linux" in archOS:
        if "arm" in archOS:
            # Raspberry Pi. Start with fbcon since directfb hangs with composite output
            # I added 'x11' because new Raspbian Stretch seems to use it instead of fbcon
            drivers = ['x11', 'fbcon', 'directfb', 'svgalib']
        else:
            drivers = ['x11', 'dga', 'fbcon', 'directfb', 'ggi', 'vgl', 'svgalib', 'aalib']
    elif "Darwin" in archOS:
        drivers = ['foo']  # No driver required (WARNING: not tested on an actual Darwin system)
    elif "Windows" in archOS:
        drivers = ['windib', 'directx']
    else:
        drivers = ['foo', 'x11', 'dga', 'fbcon', 'directfb', 'ggi', 'vgl', 'svgalib', 'aalib', 'windib', 'directx']
    found = False
    for driver in drivers:
        if driver != 'foo':
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
        try:
            pygame.display.init()
        except pygame.error:
            print('Driver: {0} failed.'.format(driver))
            continue
        found = True
        print(driver)
        break

    if not found:
        raise Exception('No suitable video driver found!')

    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print("Framebuffer Size: %d x %d" % (size[0], size[1]))
    print("Display Size: %d x %d" % (x, y))
    interpreter = str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2])
    print("Python interpreter version: %s" % interpreter)

    if x is not None and y is not None:
        if (x == size[0]) and (y == size[1]):
            windowed = False
        else:
            windowed = True
            size = (x, y)
    else:
        windowed = False

    if icon is not None:
        try:
            iconW = pygame.image.load(icon)
            pygame.display.set_icon(iconW)
        except:
            print("Main icon not found. Check Settings!")
            print(traceback.format_exc())

    if caption is not None:
        pygame.display.set_caption(caption, caption[:8]+caption[-7:])

    if windowed:
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
        screen = pygame.display.set_mode(size)
        hideMouse = False
    else:
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    if hideMouse:
        pygame.mouse.set_visible(0)

    if clearScreen:
        screen.fill((0, 0, 0))
        pygame.display.update()

    return screen, size[0], size[1], str(sys.version_info[0])+"."+str(sys.version_info[1]), archOS


####################################################################
def LoadFont(font, fsize, fbold=0):

    # Initialise font support if needed
    if not pygame.font.get_init(): pygame.font.init()

    try:
        # Load custom font
        fontObj = pygame.font.Font(font, fsize)
    except:
        try:
            # Load system installed font
            fontObj = pygame.font.SysFont(font, fsize, fbold)
        except:
            # Default to "freesans" font and list available fonts
            print(font + ": Font not available! Falling back to freesans")
            print("Available Fonts: ", pygame.font.get_fonts())
            try:
                fontObj = pygame.font.SysFont("freesans", fsize)
            except:
                print("ERROR: freesans font not available! Select proper Font!!!")
                fontObj = pygame.font.SysFont(None, fsize)
                print(traceback.format_exc())

    return fontObj


###############################################################################
def loadIcon(code, folder, extension=".png"):

    icon = None

    try:
        icon = pygame.image.load(folder + str(code) + extension).convert_alpha()
    except:
        print("Error loading icon. Loading default icon instead. Code:", folder + code)
        print(traceback.format_exc())

    return icon


###############################################################################
def loadURLImage(url, headers='', timeout=10):

    image = None

    try:
        with requests.get(url, headers=headers, timeout=timeout) as pic:
            image_str = pic.content
            image_file = io.BytesIO(image_str)
            image = pygame.image.load(image_file).convert_alpha()
    except:
        print("Error getting image from URL", url)
        print(traceback.format_exc())

    return image


####################################################################
def DrawText(screen, text, font, fcolor, blit=False, x=0, y=0, outline=None, owidth=0, ocolor=(64, 64, 64), oalpha=64):

    rtext = font.render(text, True, fcolor)
    (rtx, rty) = rtext.get_size()

    if blit:

        if outline == "outline":
            otext = font.render(text, True, ocolor)
            otext.set_alpha(oalpha / 8)  # Worked once, but now it doesn't... don't know why
            if owidth == 0: owidth = int(max(2, rtx / len(text) * 0.03))
            screen.blit(otext, (x - owidth, y - owidth))
            screen.blit(otext, (x - owidth, y + owidth))
            screen.blit(otext, (x + owidth, y - owidth))
            screen.blit(otext, (x + owidth, y + owidth))
            # These next four blits are not strictly necessary, though look better (comment to improve CPU usage)
            screen.blit(otext, (x - owidth, y))
            screen.blit(otext, (x + owidth, y))
            screen.blit(otext, (x, y - owidth))
            screen.blit(otext, (x, y + owidth))

        if outline == "outrect":
            dim(screen, oalpha, ocolor, (x - owidth, y - owidth, rtx + owidth * 2, rty + owidth))

        if outline == "shadow":
            otext = font.render(text, True, ocolor)
            otext.set_alpha(oalpha)                          # Worked once, but now it doesn't... don't know why
            screen.blit(otext, (x + owidth, y + owidth))

        if outline == "FadeIn":
            rect = (x, y, rtx, rty)
            srf = pygame.Surface((rect[2], rect[3]))
            srf.fill(ocolor)
            srf.blit(rtext, (0, 0))
            img = Screenshot(srf, (0, 0, rect[2], rect[3]))
            FadeIn(screen, img, rect, color_filter=(ocolor))

        if outline == "FadeOut":
            rect = (x, y, rtx, rty)
            srf = pygame.Surface((rect[2], rect[3]))
            srf.fill(ocolor)
            srf.blit(rtext, (0, 0))
            img = Screenshot(srf, (0, 0, rect[2], rect[3]))
            FadeOut(screen, img, rect, color_filter=(ocolor))

        if outline != "FadeOut": screen.blit(rtext, (x, y))

    rtx = rtx + owidth * 2
    rty = rty + owidth

    return rtx, rty


####################################################################
def FadeIn(screen, img, rect, time=1.2, color_filter=(0, 0, 0)):

    clock = pygame.time.Clock()
    darken_factor = 255
    darken_step = 25.5
    fadeFps = int((255 / darken_step) / time)

    while darken_factor > 0:
        clock.tick(fadeFps)
        screen.blit(img, (rect[0], rect[1]))
        dim(screen, darken_factor, color_filter, rect, True)
        darken_factor = int(darken_factor - (darken_step / time))
        event_loop()

    screen.blit(img, (rect[0], rect[1]))
    pygame.display.update(rect)

    return


####################################################################
def FadeOut(screen, img, rect, time=1, color_filter=(0, 0, 0)):

    clock = pygame.time.Clock()
    darken_factor = 0
    darken_step = 25.5
    fadeFps = int((255 / darken_step) / time)

    while darken_factor < 255:
        clock.tick(fadeFps)
        screen.blit(img, (rect[0], rect[1]))
        dim(screen, darken_factor, color_filter, rect, True)
        darken_factor = int(darken_factor + (darken_step / time))
        event_loop()

    pygame.draw.rect(screen, color_filter, rect)
    pygame.display.update(rect)

    return


####################################################################
def WrapText(text, font, width):
    # ColdrickSotK
    # https://github.com/ColdrickSotK/yamlui/blob/master/yamlui/util.py#L82-L143
    """Wrap text to fit inside a given width when rendered.
    :param text: The text to be wrapped.
    :param font: The font the text will be rendered in.
    :param width: The width to wrap to."""

    text_lines = text.replace('\t', '    ').split('\n')
    if width is None or width == 0:
        return text_lines

    wrapped_lines = []
    for line in text_lines:
        line = line.rstrip() + ' '
        if line == ' ':
            wrapped_lines.append(line)
            continue

        # Get the leftmost space ignoring leading whitespace
        start = len(line) - len(line.lstrip())
        start = line.index(' ', start)
        while start + 1 < len(line):
            # Get the next potential splitting point
            next = line.index(' ', start + 1)
            if font.size(line[:next])[0] <= width:
                start = next
            else:
                wrapped_lines.append(line[:start])
                line = line[start+1:]
                start = line.index(' ')
        line = line[:-1]
        if line:
            wrapped_lines.append(line)

    return wrapped_lines


####################################################################
def event_loop():

    etype = ekey = 0
    epos = (0,0)

    # Look for and process keyboard events to stop program or return event info
    for event in pygame.event.get():
        etype = event.type
        if event.type == pygame.QUIT:
            # On windowed mode, exit when clicking the "x" (close window)
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_q, pygame.K_ESCAPE):
                # On 'q' or Escape pressed, quit the program.
                pygame.quit()
                exit()
            else:
                ekey = event.key
        elif event.type == pygame.MOUSEBUTTONDOWN:
            epos = event.pos

    return {'Type': etype, 'Key': ekey, 'Pos': epos}


####################################################################
def dim(screen, darken_factor=64, color_filter=(0, 0, 0), rect=None, updateD=False):

    if rect is not None:
        (x, y, w, h) = rect
        w = int(w)
        h = int(h)
        darken = pygame.Surface((w, h))
    else:
        x, y = 0, 0
        darken = pygame.Surface(screen.get_size())
    darken.fill(color_filter)
    darken.set_alpha(darken_factor)
    screen.blit(darken, (x, y))
    if updateD:
        if rect is not None:
            pygame.display.update(rect)
        else:
            pygame.display.update()

    return


####################################################################
def Screenshot(screen, rect):

    pos = (rect[0], rect[1])
    size = (rect[2], rect[3])
    img = pygame.Surface(size)
    img.blit(screen, (0, 0), (pos, size))

    return img


####################################################################
def prepArea(screen, img, rect):

    if not img:
        # Capture "area" background (if not already captured and showBkg)
        img = Screenshot(screen, rect)
    else:
        # ... or blit "area" to erase previous values
        screen.blit(img, rect)

    return img


###############################################################################
def getSunSign():

    # Constellations
    ZD = [119, 218, 320, 419, 520, 620, 722, 822, 922, 1022, 1121, 1221, 1231]
    ZN = ['Capricorn', 'Aquarius', 'Pisces', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpius',
          'Sagittarius', 'Capricorn']

    sunsign = ""

    mdd = int(time.strftime("%m%d"))

    for i in range(0, len(ZD)):
        if mdd <= ZD[i]:
            sunsign = ZN[i]
            break

    return sunsign


####################################################################
def measure_temp(archOS):

    # Will only work on Linux OS
    if "arm" in archOS:
        temp = os.popen("vcgencmd measure_temp").readline()
    elif "Linux" in archOS:
        temp = os.popen("cat /sys/class/thermal/thermal_zone*/temp")
    else:
        temp = "n/a"

    return (temp.replace("temp=", ""))


"""
        # FadeIn/FadeOut EXAMPLE
        # MUST use a different Surface to blit the text/image first, then fade it on main Surface
        srf = pygame.Surface( (rect[2], rect[3]) )
        pygame.draw.rect( srf, nBkg, (0,0,rect[2],rect[3]) )
        font = pygame.font.SysFont( self.fn, size, bold)
        rtext = font.render( "Texto de prueba para FadeIn / FadeOut", True, white )
        srf.blit( rtext, (0,0) )
        img = Screenshot( srf, (0, 0, rect[2], rect[3])
        while True:
            FadeIn( self.screen, img, rect, 2, nBkg )
            sleep(5)
            FadeOut( self.screen, img, rect, 2, nBkg )
"""


####################################################################
def get_input_box_value(screen, rect, back_color=pygame.Color('black'), line_color=pygame.Color('white'), line_thickness=2,
             font="freesans", font_size=32, text='', text_color=pygame.Color('white'), init_text='Enter text',
             init_text_color=pygame.Color('gray55')):

    end_value, event_box, input_box = InputBox(screen=screen, rect=rect, back_color=back_color, line_color=line_color,
                                               line_thickness=line_thickness, font=font, font_size=font_size, text=text,
                                               text_color=text_color, init_text=init_text, init_text_color=init_text_color,
                                               draw=True, capture=False)
    done = False
    draw = False
    capture = True

    final_event = event_box

    while not done:

        if event_box.get("Type") == pygame.KEYDOWN:
            if event_box.get("Key") == pygame.K_RETURN:
                break
            elif event_box.get("Key") == pygame.K_TAB:
                break
            elif event_box.get("Key") == pygame.K_ESCAPE:
                end_value = str(text)
                draw = True
                capture = False
                done = True
        elif event_box.get("Type") == pygame.MOUSEBUTTONDOWN:
            if not input_box.collidepoint(event_box.get("Pos")):
                draw = True
                capture = False
                done = True

        end_value, event_box, input_box = InputBox(screen=screen, rect=rect, back_color=back_color, line_color=line_color,
                                               line_thickness=line_thickness, font=font, font_size=font_size, text=str(end_value),
                                               text_color=text_color, init_text="", init_text_color=init_text_color,
                                               draw=draw, capture=capture)
        if capture:
            final_event = event_box

        if done and (not end_value or end_value.isspace()):
            end_value = str(init_text)

    return str(end_value), final_event, input_box


####################################################################
def InputBox(screen, rect, back_color=pygame.Color('black'), line_color=pygame.Color('white'), line_thickness=2,
             font="freesans", font_size=32, text='', text_color=pygame.Color('white'), init_text='Enter text',
             init_text_color=pygame.Color('gray55'), draw=True, capture=True):
    # Use draw=True to set several InputBox at a time, or re-enter (draw=False); and use capture to focus on one of them
    # Use Enter/TAB to move from one InputBox to another (control must be outside this function, on your program)

    # Enable key held detection (disabled by default in pygame)
    pygame.key.set_repeat(300, 50)

    # Prepare values, font and box (to detect mouse collision)
    firstRun = True
    done = False
    cursor = "|"
    fontObj = LoadFont(font, font_size)
    box = pygame.Rect(rect)
    ekey = etype = 0
    epos = (0, 0)

    # Enter "read-character/draw-text" loop
    while not done:
        if capture:
            for event in pygame.event.get():
                etype = event.type
                if etype == pygame.QUIT:
                    # On windowed mode, exit when clicking the "x" (close window)
                    pygame.quit()
                    exit()
                elif etype == pygame.MOUSEBUTTONDOWN:
                    epos = event.pos
                    if not box.collidepoint(epos):
                        # Exit InputBox if mouse is pressed outside the rect, or else stay
                        done = True
                elif etype == pygame.KEYDOWN:
                    ekey = event.key
                    if ekey == pygame.K_RETURN or ekey == pygame.K_ESCAPE or ekey == pygame.K_TAB:
                        # Exit InputBox if Enter (Finish), Escape (Cancel) or Tab (Next) are pressed
                        done = True
                    elif ekey == pygame.K_BACKSPACE:
                        # Erase last character when Backspace is pressed
                        text = text[:-1]
                    else:
                        # Add entered character to text
                        text = text + event.unicode
                    draw = True
        else:
            done = True

        if firstRun or draw or done:
            # Select text to draw: initial (passed), intermediate (with "cursor") or final (no "cursor")
            if text is None or text == '':
                if init_text is None: init_text = ''
                box_text = init_text
                color = init_text_color
            else:
                if text is None: text = ''
                box_text = text
                color = text_color

            if not done:
                box_text = box_text + cursor

            # Draw rect
            pygame.draw.rect(screen, back_color, rect)
            if line_thickness > 0:
                pygame.draw.rect(screen, line_color, rect, line_thickness)

            # Draw selected text
            rtext = fontObj.render(box_text, True, color)
            tx, ty = rtext.get_size()
            screen.blit(rtext, (rect[0] + line_thickness + font_size*0.3, rect[1] + (rect[3] - ty) / 2))

            # Update display
            pygame.display.update(rect)

            if firstRun:
                firstRun = False
                init_text = ''
            draw = False

        # Save CPU
        time.sleep(0.01)

    return text, {'Type': etype, 'Key': ekey, 'Pos': epos}, box


"""
# EXAMPLE of two InputBox with "re-enter" function

while not done
    
    if first_run:
        input_value1, event_box, input_box = disputil.get_input_box_value(self.screen, rect1, 
                                                                    init_text=str(value1), draw=True, capture=False)
        box1 = pygame.Rect(rect1)

        input_value1, event_box, input_box = disputil.get_input_box_value(self.screen, rect2, 
                                                                    init_text=str(value2), draw=True, capture=False)
        box2 = pygame.Rect(rect2)
        
        button = pygame.Rect(button_rect)
                                                                    
    else:
        if changed1:
            input_value1, event_box, input_box = disputil.get_input_box_value(self.screen, rect1, 
                                                                    init_text=str(value[i]), draw=False, capture=True)
        elif changed2:
            input_value2, event_box, input_box = disputil.get_input_box_value(self.screen, (ix, iy, 300, 50), 
                                                                    init_text=str(value[i]), draw=False, capture=True)
        
        if event_box is not None and event_box.get("Type") == pygame.MOUSEBUTTONDOWN:
            event = event_box
            event_box = None
        else:
            event = event_loop()

        if event.get("Type") == pygame.MOUSEBUTTONDOWN:
            if box1.collidepoint(event.get("Pos")):
                changed1 = True
            elif box2.collidepoint(event.get("Pos")):
                changed2 = True
            elif button.collidepoint(event.get("Pos")):
                done = True
        elif event.get("Type") == pygame.KEYDOWN:
            if event.get("Key") == pygame.K_RETURN:
                done = True
            
    time.sleep(0.05)
"""
