import image
from sys import argv


def calc_dist(c1, c2):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)


def edging(fname_in, fname_out, n_iter):
    img = image.load(fname_in)
    width, height = len(img[0]), len(img)
    img_out = image.create(width, height, (0, 0, 0))
    pix_hood = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
    for _ in range(n_iter):
        for row in range(height):
            for col in range(width):
                color = img[row][col]
                max_distance = 0
                max_color = color
                for x, y in pix_hood:
                    row_hood = y + row
                    col_hood = x + col
                    if not (0 <= col_hood < width and 0 <= row_hood < height):
                        continue
                    color_hood = img[row_hood][col_hood]
                    distance = calc_dist(color, color_hood)
                    if distance > max_distance:
                        max_distance = distance
                        max_color = color_hood
                img_out[row][col] = max_color
        img, img_out = img_out, img
    image.save(fname_out, img)


def draw_quad(img, x, y, w, h, c):
    """Disegna su img un rettangolo con lo spigolo
    in alto a sinistra in (x, y), larghezza w,
    altezza h e di colore c."""
    for i in range(y,y+h):
        for j in range(x,x+w):
            # Disegna il pixel solo se è dentro
            if 0 <= i < len(img) and 0 <= j < len(img[0]):
                img[i][j] = c


def inside(img, i, j):
    """Ritorna True se il pixel (i, j) e' dentro l'immagine img, False
    altrimenti"""
    iw, ih = len(img[0]), len(img)
    return 0 <= i < iw and 0 <= j < ih


def mosaic_nearest(fname_in, fname_out, s):
    """Ritorna una nuova immagine ottenuta dividendo
    l'immagine img in quadrati di lato s e riempendo
    ogni quadrato con il colore del suo angolo in
    alto a sinistra"""
    img = image.load(fname_in)
    w, h = len(img[0]), len(img)
    ret = image.create(w, h, (0,0,0))
    # itera sui possibili quadrati
    for jj in range(h//s):
        for ii in range(w//s):
            # colore dell'angolo in alto-sinistra
            c = img[jj*s][ii*s]
            draw_quad(ret, ii*s, jj*s, s, s, c)
    image.save(fname_out, ret)


def average(img, i, j, w, h):
    '''Calcola la media dei valori dell'area
    [i,w-1]x[j,h-1].'''
    c = [0,0,0]
    for jj in range(j,j+h):
        for ii in range(i,i+w):
            for k in range(3):
                c[k] += img[jj][ii][k]
    for k in range(3):
        c[k] //= w*h
    return tuple(c)


def mosaic_average(fname_in, fname_out, s):
    '''Ritorna una nuova immagine ottenuta dividendo
    l'immagine img in quadrati di lato s e riempendo
    ogni quadratino con la media dei suoi colori.'''
    img = image.load(fname_in)
    w, h = len(img[0]), len(img)
    ret = image.create(w, h, (0,0,0))
    # itera sui possibili quadrati
    for jj in range(h//s):
        for ii in range(w//s):
            # colore medio dell'immagine
            c = average(img,ii*s,jj*s,s,s)
            draw_quad(ret, ii*s, jj*s, s, s, c)
    image.save(fname_out, ret)


def mosaic_size(fname_in, fname_out, s):
    '''Ritorna una nuova immagine ottenuta dividendo
    l'immagine img in quadratini di lato s e
    disegnando all'interno di ognuno di essi,
    su sfondo nero, un quadratino centrale bianco di
    lato proporzionale alla luminosità media del
    corrispondente quadratino'''
    img = image.load(fname_in)
    w, h = len(img[0]), len(img)
    ret = image.create(w, h, (0,0,0))
    # itera sui possibili quadrati
    for jj in range(h//s):
        for ii in range(w//s):
            # colore medio dell'immagine
            c = average(img,ii*s,jj*s,s,s)
            # lato del quadratino bianco
            r = round(s*(c[0]+c[1]+c[2])/(3*255))
            draw_quad(ret, ii*s+(s-r)//2,
                jj*s+(s-r)//2, r, r, (255,255,255))
    image.save(fname_out, ret)


def main():
    if not (len(argv) == 5 ):
        print("Devi passare 4 argomenti.")
        print("1. Quale tipo di modifica applicare:")
        print("Edging: 1.")
        print("Mosaic: 2.")
        print("Mosaic average: 3.")
        print("Mosaic black white: 4.")
        print("2. Quale è l'immagine da modificare. (Stringa)")
        print("3. Con che nome salvare l'immagine modificata. (Stringa)")
        print("4. Quante volte applicare Edging oppure la grandezza dei quadrati di Mosaic. (Intero > 0)")
        return
    else:
        print(argv[0], "avviato con:")
        mode, fname_in, fname_out, n = int(argv[1]), argv[2], argv[3], int(argv[4])
        print("Modifier scelto:", mode)
        print("Immagine in input:", fname_in)
        print("Immagine in output sara':", fname_out)
        if mode == 1:
            print("Numero applicazioni modifica:", n)
        elif mode == 2:
            print("Grandezza dei quadrati:", n)
        if n <= 0:
            return
        if mode == 1:
            edging(fname_in, fname_out, n)
        elif mode == 2:
            mosaic_nearest(fname_in, fname_out, n)
        elif mode == 3:
            mosaic_average(fname_in, fname_out, n)
        elif mode == 4:
            mosaic_size(fname_in, fname_out, n)
    print("Fatto!")


if __name__ == "__main__":
    main()
