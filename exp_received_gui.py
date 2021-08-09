import os
import sys
import PySimpleGUI as sg

from utils.received_exp import INIT_JOB, ADD_JOB, GADABOUT_JOB
from utils.received_exp import received_exp_check, print_results, load_csv

# リソースパスの取得（実行ファイル用）
def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(filename)


exec_directory = os.path.dirname(sys.argv[0])

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
    [sg.Text("")],
    [sg.Button("計算", key="calculate"), sg.Button("入力クリア", key="input_clear"),
     sg.Button("出力クリア", key="output_clear"), sg.Button("終了", key="end")],
    [sg.Text("経験値受け取り結果：", size=(20, 1))],
    [sg.Output(size=(60, 20), font=("default", 15), key="output")]
]

# ウィンドウ生成
window = sg.Window("DQX. 今の職で経験値受け取ったらレベルいくつ上がる？", layout)

# イベントルール
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    
    if event == "end":
        break

    if event == "input_clear":
        window["job"].update("")
        window["lv"].update("")
        window["next_exp"].update("")
        window["receiving_exp"].update("")
    
    if event == "output_clear":
        window["output"].update("")

    if event == "calculate":
        if all(values.values()): 
            user = (values["job"], int(values["lv"]), int(values["next_exp"]))
            csv_path = os.path.join(exec_directory, "csv", "exp_info.csv")
            csv_path = resourcePath(csv_path)
            exp_info = load_csv(csv_path)
            results = received_exp_check(exp_info, user, int(values["receiving_exp"]))
            if results is None:
                continue
            print_results(results)
        else:
            print("職業、現在のレベル、次のレベルまで、受け取るEXP.はすべて入力してください")
            continue

window.close()