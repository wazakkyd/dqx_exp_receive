import os
import PySimpleGUI as sg

from utils.received_exp import INIT_JOB, ADD_JOB, GADABOUT_JOB
from utils.received_exp import received_exp_check, print_results, load_csv


exec_directory = os.path.dirname(__file__)

# デザインテーマの設定
sg.theme("LightGreen10")

job_list = INIT_JOB + ADD_JOB + GADABOUT_JOB

# レイアウト
layout = [
    [sg.Text("DQX. 今の職で経験値受け取ったらレベルいくつ上がる？", size=(45, 1))],
    [sg.Text("職業", size=(15, 1)), sg.Combo(job_list, size=(15, 1), key="job")],
    [sg.Text("現在のレベル", size=(15, 1)), sg.InputText("", size=(10, 1), key="lv")],
    [sg.Text("次のレベルまで", size=(15, 1)), sg.InputText("", size=(10, 1), key="next_exp")],
    [sg.Text("受け取るEXP.", size=(15, 1)), sg.InputText("", size=(10, 1), key="receiving_exp")],
    [sg.Button("計算", key="calculate")],
    [sg.Output(size=(60, 20), font=("default", 15))]
]

# ウィンドウ生成
window = sg.Window("DQX. 今の職で経験値受け取ったらレベルいくつ上がる？", layout)

# イベントルール
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "calculate":
        if all(values.values()): 
            user = (values["job"], int(values["lv"]), int(values["next_exp"]))
            csv_path = os.path.join(exec_directory, "csv", "exp_info.csv")
            exp_info = load_csv(csv_path)
            results = received_exp_check(exp_info, user, int(values["receiving_exp"]))
            if results is None:
                continue
            print_results(results)
        else:
            print("職業、現在のレベル、次のレベルまで、受け取るEXP.はすべて入力してください")
            continue

window.close()