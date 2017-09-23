import png


def create(iwidth, iheight, color):
    """Crea e ritorna un'immagine (cioè un array 2D) di larghezza width, altezza height e con
        tutti i pixels di colore color"""
    img = []
    for _r in range(iheight):
        row = []
        for _c in range(iwidth):
            row.append(color)
        img.append(row)
    return img


def save(filename_out, img):
    """Salva un'immagine in formato PNG con nome filename"""
    png_img = png.from_array(img, 'RGB')
    png_img.save(filename_out)


def load(filename):
    """Carica l'immagine in formato PNG dal file filename, la converte nel
    formato a matrice di tuple e la ritorna"""
    with open(filename, 'rb') as file_img:
        iwidth, iheight, png_img, _ = png.Reader(file=file_img).asRGB8()
        png_img = [[v for v in png_row] for png_row in png_img]
    img = []
    for png_row in png_img:
        row = []
        for i in range(0, len(png_row), 3):
            row.append((png_row[i + 0],
                        png_row[i + 1],
                        png_row[i + 2]))
        img.append(row)
    return img



