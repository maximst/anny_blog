from PIL import Image


def flip_horizontal(path):
    with open(path, 'rb') as f:
        sim = Image.open(f)
        dim = Image.new("RGB", sim.size)
        for r in range(sim.size[1]):
            for i in range(sim.size[0]):
                dim.putpixel((sim.size[0]-1-i, r), sim.getpixel((i, r)))

    dim.save(path)
