import os

def get_size(path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)

    return total_size


def human_size(size):
    for unit in ['B','KB','MB','GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


ruta = "."  # carpeta actual del proyecto

print("\n📦 PESO DEL PROYECTO POR CARPETAS\n")

for item in os.listdir(ruta):
    path = os.path.join(ruta, item)

    if os.path.isdir(path):
        size = get_size(path)
        print(f"{item:25} -> {human_size(size)}")
    else:
        size = os.path.getsize(path)
        print(f"{item:25} -> {human_size(size)}")

print("\n✅ Listo")