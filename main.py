from os import system
from glob import glob
from sys import argv
from sys import platform
from pathlib import PureWindowsPath, Path

def check_ffmpeg_win(FFMPEG):
    if not Path(FFMPEG).is_file():
        print(f"Binary file {FFMPEG} doesn't exist. Download it, please, from https://www.ffmpeg.org/download.html")
        ans = input("Press any key to exit or 'Y' if you downloaded ffmpeg and want to continue: ")
        if ans != "Y" and ans !="y":
            exit(0)
    print(f"For encoding wil be used {FFMPEG}")



def main(DIR, OUTDIR, LOGO, FFMPEG):
    mxfs = glob(f"{DIR}/*.*")
    for mxf in mxfs:
        video_name = Path(mxf).stem.split('.')[0]
        null_device = "/dev/null" if not platform.startswith('win') else "NUL"
        cmd_pass1 = f'{FFMPEG} -y -i {mxf} -c:v libx264 -b:v 7500k -pass 1 -an -f null {null_device}'
        cmd_pass2 = f'{FFMPEG} -y -i {mxf}  -i  {LOGO} -map 0:a  -filter_complex "overlay=0:0" -c:v libx264  -b:v 7500k -pass 2  -c:a aac -ar 48000 -b:a 128k  -f mpegts {OUTDIR}/{video_name}.ts'

        system(cmd_pass1)
        system(cmd_pass2)


if __name__ == "__main__":
    print("Help : main.exe input_video_folder_path  output_video_folder_path  logo_file_path ffmpeg_path")
    DIR = argv[1] if len(argv) > 2 else "./video_input"
    OUTDIR = argv[2] if len(argv) > 3 else "./video_output"
    LOGO = argv[3] if len(argv) > 4 else "./logo/LOGO_KvTV.png"
    FFMPEG = argv[4] if len(argv) > 5 else "ffmpeg"

    if platform.startswith('win'):
        FFMPEG = "./ffmpeg/bin/ffmpeg.exe"
        check_ffmpeg_win(FFMPEG)
        [DIR, OUTDIR, LOGO, FFMPEG] = map(lambda pth: str(PureWindowsPath(pth)), [DIR, OUTDIR, LOGO, FFMPEG])

    main(DIR, OUTDIR, LOGO, FFMPEG)

