import pyautogui
import time
from PIL import ImageGrab
from functools import partial
import cv2 as cv
import numpy as np
from datetime import datetime

def click_screen(i, position):
    '''
    Move o mouse para um local da tela e aplica i clicks sobre ele
    :param i:
    :param position:
    :return:
    '''
    if position:
        pyautogui.moveTo(*position)
        for _ in range(i):
            pyautogui.click()
            time.sleep(1)

def get_position(image, color=False, first=True):
    '''
    Pega a posisação da tela baseado em duas imagens, um screenshot da tela e uma imagem de algum icone clicavel

    :param image: Icone clicavel, os icones estão dentro de images
    :param color:
    :param first:
    :return:
    '''
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    screen_img = ImageGrab.grab()

    if color:
        img = np.array(screen_img.convert('RGB'))
        template = cv.cvtColor(cv.imread(f'./images/green_bar.png'), cv.COLOR_BGR2RGB)
        w, h, _ = template.shape
    else:
        img = cv.cvtColor(np.array(screen_img), cv.COLOR_BGR2GRAY)
        template = cv.imread(f'./images/{image}.png', 0)
        w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.9 if color else 0.8
    loc = np.where(res >= threshold)

    positions = []
    for pt in zip(*loc[::-1]):
        pos = (pt[0] + w / 2, pt[1] + h / 2)
        if positions and abs(pos[0] - positions[-1][0]) < 5 and abs(pos[1] - positions[-1][1]) < 5:
            continue
        positions.append((pt[0] + w / 2, pt[1] + h / 2))
        if first:
            return positions[0]

    return positions

def set_hero_to_work(scroll=False):
    '''
    Coloca os herois com stamina verde para trabalhar

    :return:
    '''
    if scroll:
        position = get_position('work')
        pyautogui.moveTo(*position)
        for i in range(20):
           pyautogui.scroll(-i)
        time.sleep(2)
    green_bar_pos = get_position('green_bar', color=True, first=False)
    if green_bar_pos:
        work_button_pos = get_position('work', first=False)

        for gree_bar in green_bar_pos:
            delta = 1000
            pos = None
            for work_button in work_button_pos:
                value = (gree_bar[-1] - work_button[-1])
                if value < delta and value > 0:
                    delta = (gree_bar[-1] - work_button[-1])
                    pos = work_button
            click_screen(1, pos)

def main():
    i=1
    while True:
        # Verifica se tem mensagem de erro na tela
        position = get_position('ok')
        if position:
            print('erro...')
            click_screen(1, position)
            time.sleep(13)
            click_screen(1, get_position('connect_wallet'))
            time.sleep(5)
            click_screen(1, get_position('sign'))


        # Verifica se está na tela de conexão
        position = get_position('connect_wallet')
        if position:
            print('connectando carteira...')
            click_screen(1, position)
            time.sleep(5)
            delta = 0
            position = None
            while (not position) and (delta < 3):
                position = get_position('sign')
                click_screen(1, position)
                delta += 1
            # atualiza tela
            if delta > 3:
                click_screen(1, get_position('reload'))

        # Coloca os herois para trabalhar
        position = get_position('hunting_game')
        if position:
            print('colocando herois para trabalhar...')
            click_screen(1, get_position('heros'))
            time.sleep(3)
            set_hero_to_work(scroll=False)
            set_hero_to_work(scroll=True)
            time.sleep(3)
            click_screen(1, get_position('close_menu'))
            time.sleep(3)
            click_screen(1, get_position('hunting_game'))
            time.sleep(3)
            print(datetime.now())
            time.sleep(900)
            i += 1

        position = get_position('go_back_arrow')
        time.sleep(3)
        click_screen(1, position)


if __name__ == '__main__':
    main()
