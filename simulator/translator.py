from PIL import Image, ImageDraw, ImageFont

def draw_triangle(draw, position, size, color):
    x, y = position
    triangle = [(x, y + size), (x + size, y + size // 2), (x, y)]
    draw.polygon(triangle, fill=color)

def add_translations(use_quaternion, use_euler, use_matrix):
    gif_path = "./simulations/airplane_quaternion.gif"
    gif = Image.open(gif_path)

    font = ImageFont.truetype("arial.ttf", size=20)

    frames = []
    for frame in range(0, gif.n_frames):
        gif.seek(frame)
        frame_image = gif.copy().convert("RGBA")

        draw = ImageDraw.Draw(frame_image)

        y_start = 20
        x_text = 40
        x_triangle = 20
        size = 10
        spacing = 25

        if use_quaternion:
            draw_triangle(draw, (x_triangle, y_start + 5), size, "blue")
            draw.text((x_text, y_start), "Кватерніони", font=font, fill="blue")
            y_start += spacing
        if use_euler:
            draw_triangle(draw, (x_triangle, y_start + 5), size, "purple")
            draw.text((x_text, y_start), "Кути Ейлера", font=font, fill="purple")
            y_start += spacing
        if use_matrix:
            draw_triangle(draw, (x_triangle, y_start + 5), size, "green")
            draw.text((x_text, y_start), "Матриці обертання", font=font, fill="green")

        frames.append(frame_image)

    frames[0].save("./simulations/airplane_with_text.gif", save_all=True, append_images=frames[1:], duration=gif.info['duration'], loop=0, disposal=2)

    print("Текст додано.")
