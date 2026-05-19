import schedule
import os
import time
import subprocess
import yaml
import logging
from datetime import datetime, timedelta


def setup_logger(log_path):
    # ログ保存用のディレクトリが存在しない場合は自動で作成する
    os.makedirs(log_path, exist_ok=True)

    log_filename = f"video_recorder_{datetime.now().strftime('%Y%m%d')}.log"
    log_filename = os.path.join(log_path, log_filename)

    logger = logging.getLogger('VideoRecorder')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ===== パスとロガーの初期設定 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")
LOG_PATH = os.path.join(BASE_DIR, "log")

logger = setup_logger(LOG_PATH)

# ===== 設定ファイルの読み込み =====
try:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logger.error(f"設定ファイルが見つかりません。パスを確認してください: {CONFIG_PATH}")
    exit(1)

# 設定値の取得
RTSP_URL = config.get("rtsp_url")
START_TIME = config.get("start_time")
END_TIME = config.get("end_time")
SAVE_PATH = config.get("save_path")


# ===== 録画時間の計算ロジック =====
def calculate_duration(start_str, end_str):
    # "HH:MM" 形式の文字列を datetime オブジェクトとしてパース
    # （日付部分はデフォルトの1900-01-01になります）
    start_dt = datetime.strptime(start_str, "%H:%M")
    end_dt = datetime.strptime(end_str, "%H:%M")

    # 終了時刻が開始時刻以下の場合（例: 23:00開始、01:00終了）は、1日（24時間）足して翌日扱いにする
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    # 差分を秒数(float)で取得し、整数(int)にして返す
    return int((end_dt - start_dt).total_seconds())


def record_video():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"record_{now}.mp4"
    output_file = os.path.join(SAVE_PATH, output_file)

    logger.info(f"録画を開始します: {output_file} (予定録画時間: {RECORD_DURATION}秒)")

    command = [
        "ffmpeg",
        "-i", RTSP_URL,
        "-t", str(RECORD_DURATION),  # 計算した秒数を使用
        "-c", "copy",
        output_file
    ]

    subprocess.run(command)
    logger.info("録画が完了しました。")


# 設定読み込み時に録画時間を計算しておく
RECORD_DURATION = calculate_duration(START_TIME, END_TIME)

if __name__ == "__main__":
    # 毎日設定した時間に record_video 関数を実行
    schedule.every().day.at(START_TIME).do(record_video)

    logger.info(f"設定ファイルを読み込みました: {CONFIG_PATH}")
    logger.info(f"開始時間: {START_TIME}, 終了時間: {END_TIME}")
    logger.info(f"算出された録画時間: {RECORD_DURATION}秒")
    logger.info("スケジューラーを起動し、待機しています...")

    while True:
        schedule.run_pending()
        time.sleep(1)