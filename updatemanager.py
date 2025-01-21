import os
import sys
import requests
import subprocess
import tkinter as tk
from tkinter import messagebox
from packaging import version  # version 비교를 위한 모듈 추가

GITHUB_API_URL = "https://api.github.com/repos/byeonggonkang/Validation_Support_Tool_Xjera/releases/latest"
CURRENT_VERSION = "v1.0.1"

def check_for_updates():
    try:
        # GitHub에서 최신 릴리스 정보 가져오기
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        release_info = response.json()

        latest_version = release_info['tag_name']  # 최신 릴리스 태그 (예: v1.0.2)
        
        # 버전 비교 (v2.0.1과 v2.0.0이 올바르게 비교되도록)
        if version.parse(latest_version.lstrip('v')) > version.parse(CURRENT_VERSION.lstrip('v')):
            # 최신 EXE 파일 URL 가져오기
            for asset in release_info['assets']:
                if asset['name'].endswith(".exe"):
                    download_url = asset['browser_download_url']
                    prompt_update(latest_version, download_url)
                    return
    except Exception as e:
        print(f"Error checking for updates: {e}")

def prompt_update(latest_version, download_url):
    message = f"A new version {latest_version} is available. Do you want to update?"
    response = messagebox.askquestion("Update Available", message)
    if response == 'yes':
        download_and_install_update(download_url, latest_version)

def download_and_install_update(download_url, latest_version):
    try:
        # 태그 이름 기반으로 새 EXE 경로 설정
        exe_filename = f"Validation_Support_Tool_Xjera_{latest_version}.exe"
        new_exe_path = os.path.join(os.path.dirname(sys.executable), exe_filename)

        # EXE 파일 다운로드
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        with open(new_exe_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # 업데이트 완료 메시지 표시
        messagebox.showinfo(
            "Update Complete",
            f"Update has been downloaded successfully.\n"
            f"The new file will now be executed:\n{new_exe_path}",
        )

        # 새 EXE 파일 실행
        subprocess.Popen([new_exe_path], close_fds=True)

        # 현재 프로그램 종료
        sys.exit(0)

    except Exception as e:
        messagebox.showerror("Update Failed", f"An error occurred while updating: {e}")

def main():
    # Tkinter GUI 설정
    root = tk.Tk()
    root.withdraw()  # 기본 Tkinter 창을 숨깁니다.

    # 프로그램 시작 시 1초 후 업데이트 확인
    root.after(1000, check_for_updates)

    root.mainloop()

if __name__ == '__main__':
    main()
