from PIL import Image

# Ruta de la imagen PNG generada previamente
png_path = "/mnt/data/A_flat_vector_icon_features_a_dark_blue_square_wit.png"
ico_path = "/mnt/data/favicon.ico"

# Abrir la imagen y guardarla como .ico en varias resoluciones típicas
img = Image.open(png_path)
img.save(ico_path, format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64)])

ico_path
