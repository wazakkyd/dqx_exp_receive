import pandas as pd

INIT_JOB = ["戦士", "僧侶", "魔法使い", "武闘家", "旅芸人"]
ADD_JOB = ["バトルマスター", "パラディン", "魔法戦士",
        "スーパースター", "まもの使い", "どうぐ使い",
        "踊り子", "占い師", "天地雷鳴士", "デスマスター",
        "魔剣士",
        ]
GADABOUT_JOB = ["遊び人"]

def received_exp_check(exp_info, user, receiving_exp):
    job, lv, next_exp = user

    if job in INIT_JOB:
        job_group = "init"
    elif job in ADD_JOB:
        job_group = "add"
    elif job in GADABOUT_JOB:
        job_group = "gadabout"
    else:
        print(f"指定された職 \"{job}\" は対応していません。")
        print("下記のいずれかの職を選択してください")
        print(f"{INIT_JOB + ADD_JOB + GADABOUT_JOB}")
        return

    # 次のレベル到達時の累積ポイント
    job_group = job_group + "_cum"

    # Lv上限チェック
    lv_max = exp_info["Lv"].max()
    if lv > lv_max:
        print(f"現在の上限レベルは{lv_max}です。この値より高いLvには対応してません。")
        print(f"入力されたLv: {lv}")
        return

    next_exp_cum = exp_info.loc[exp_info.Lv == lv + 1, job_group]
    next_exp_cum = next_exp_cum.values[0]
    # 現在の累積ポイント
    now_exp_cum = next_exp_cum - next_exp
    # ポイントをうけとったときの累積ポイント
    receiving_cum_exp = now_exp_cum + receiving_exp

    # jobの上限チェック
    job_max = exp_info.loc[:, job_group].max()
    if receiving_cum_exp > job_max:
        over_exp = receiving_cum_exp - job_max
        after_receiving_exp_lv = exp_info.loc[:, "Lv"].max()
        levelup_count = after_receiving_exp_lv - lv
        new_next_exp = -over_exp
        return (job,
                after_receiving_exp_lv,
                levelup_count,
                new_next_exp,
                receiving_cum_exp,
                receiving_exp)

    # ポイント受け取り後のレベル
    after_receiving_exp_lv = exp_info.loc[exp_info.loc[:, job_group] > receiving_cum_exp]
    after_receiving_exp_lv = after_receiving_exp_lv.Lv.min() - 1
    # 上昇するレベル
    levelup_count = after_receiving_exp_lv - lv
    # 次のレベルの到達ポイント
    next_receiving_cum_exp = exp_info.loc[exp_info.Lv == after_receiving_exp_lv + 1, job_group]
    next_receiving_cum_exp = next_receiving_cum_exp.values[0]
    # 次のレベルまでのポイント
    new_next_exp = next_receiving_cum_exp - receiving_cum_exp

    # 受け取り後のレベル、上昇するレベル、次のレベルまでのポイント、受け取り後の累積ポイント
    return (job,
            after_receiving_exp_lv,
            levelup_count,
            new_next_exp,
            receiving_cum_exp,
            receiving_exp)

def print_results(results):
    (job,
     after_receiving_exp_lv,
     levelup_count,
     new_next_exp,
     receiving_cum_exp,
     receiving_exp) = results

    print("*"*30)
    print(f"職業：{job}")
    print(f"受け取り後のレベル:{after_receiving_exp_lv}")
    print(f"レベルの上昇数:{levelup_count}")
    print(f"次のレベルまで:{new_next_exp:,}")
    print(f"受け取り後の累計経験値:{receiving_cum_exp:,}")

    if new_next_exp < 0:
        print()
        print(f"受け取りポイント{receiving_exp:,}のうち{-new_next_exp:,}ポイントが上限をオーバーしています。")

def load_csv(path):
    return pd.read_csv(path)

