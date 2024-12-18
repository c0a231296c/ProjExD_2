import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル(横、縦) 画面内:True, 画面外:False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate
    

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバーした際に表示する画面の処理
    引数：screen
    戻り値：None
    """
    #ブラックアウトの処理
    go_rect = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_rect, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    go_rect.set_alpha(200)
    screen.blit(go_rect, [0, 0])
    #文字の処理
    fonto = pg.font.Font(None, 60)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_locate = txt.get_rect()
    txt_locate.center = WIDTH / 2, HEIGHT / 2
    screen.blit(txt, txt_locate)
    #コウカトン画像の処理
    kk_cry_img = pg.image.load("fig/8.png")   
    kk_cry_rct = kk_cry_img.get_rect()
    kk_cry_rct.center = WIDTH / 2 + 200, HEIGHT / 2
    screen.blit(kk_cry_img, kk_cry_rct)
    kk_cry_rct.center = WIDTH / 2 - 200, HEIGHT / 2
    screen.blit(kk_cry_img, kk_cry_rct)
    pg.display.update()
    time.sleep(5)
    return 


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    時間とともに爆弾が拡大，加速する処理
    引数：なし
    戻り値：サイズの異なる爆弾Surfaceを要素としたリストと加速度リスト
    """
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    pass
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    引数：sum_mv
    戻り値：対応する向きの画像Surface
    """
    # img = pg.image.load("fig/3.png") 
    # dct = {
    #     (0, -5):
    #     (5, -5):
    #     (5, 0): pg.tranform.flip(img, True, False),
    #     (5, 5):
    #     (0, 5):
    #     (-5, 5): 
    #     (-5, 0): img,
    #     (-5, -5):
    # }
    
    # img = pg.transform.rotozoom(img, 10, 1.0) 


def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    orgから見て，dstがどこにあるかを計算し，方向ベクトルをタプルで返す
    引数：org
    戻り値：方向ベクトルをタプル
    """
    pass


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    #kk_img = get_kk_img((0, 0))
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過させる
    bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル(tuple)
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            print("GameOver")
            return  # ゲームオーバー
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        #kk_img = get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
        # こうかとんが画面外なら、元の位置に戻す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]
        bb_img = bb_imgs[min(tmr // 500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx, avy)  # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出る
            vx *= -1
        if not tate:  # 縦にはみ出る
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
