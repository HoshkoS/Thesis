import PySimpleGUI as sg
from .runner import run
from .translator import add_translations

def run_gui():
    sg.theme('LightBlue2')
    sg.set_options(font=('Times New Roman', 14))

    layout = [
        [sg.Text("Кут повороту:")],
        [sg.Text("X:"), sg.InputText("0", key='angle_x', size=(5,1)),
         sg.Text("Y:"), sg.InputText("0", key='angle_y', size=(5,1)),
         sg.Text("Z:"), sg.InputText("0", key='angle_z', size=(5,1))],

        [sg.Text("Швидкість руху:"), sg.InputText("1", key='speed', size=(5,1))],
        [sg.Text("Кількість кроків:"), sg.InputText("10", key='steps', size=(5,1))],

        [sg.Text("Методи обертання:")],
        [sg.Checkbox("Кватерніони", key='quaternion', default=True)],
        [sg.Checkbox("Ейлер", key='euler')],
        [sg.Checkbox("Матриці обертання", key='matrix')],

        [sg.Button("Почати моделювання"), sg.Button("Вийти")]
    ]
    window = sg.Window("Параметри обертання літака", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Вийти':
            break
        elif event == 'Почати моделювання':
                angle_x = float(values['angle_x'])
                angle_y = float(values['angle_y'])
                angle_z = float(values['angle_z'])
                speed = float(values['speed'])
                steps = int(values['steps'])
                use_quaternion = values['quaternion']
                use_euler = values['euler']
                use_matrix = values['matrix']

                if angle_x == 0 and angle_y == 0 and angle_z == 0:
                    sg.popup("❗ Помилка: Хоча б один з кутів повинен бути ненульовим!", title="Помилка вводу")
                    continue

                if speed < 0:
                    sg.popup("❗ Помилка: Швидкість не може бути від'ємною!", title="Помилка вводу")
                    continue

                if not (use_quaternion or use_euler or use_matrix):
                    sg.popup("❗ Помилка: Оберіть хоча б один метод обчислення (кватерніони, Ейлер або матриці)!", title="Помилка вводу")
                    continue

                print(f"Кути: X={angle_x}, Y={angle_y}, Z={angle_z}")
                print(f"Швидкість: {speed}")
                print(f"Методи: Кватерніони={use_quaternion}, Ейлер={use_euler}, Матриці={use_matrix}")

                run(angle_x, angle_y, angle_z, speed, use_quaternion, use_euler, use_matrix, steps)
                add_translations(use_quaternion, use_euler, use_matrix)
                window.close()
                sg.popup("Запис моделювання створено!")
                break

    window.close()
