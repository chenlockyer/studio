import io,sys,subprocess,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
SRC=r"D:\my_media\video\unitree_g1\群控\群控.mp4"
# 首屏视频源信息：group-sync 起点 29.5s（此前用灰度相关匹配定位的）
for (w,h,crf,label) in [(1280,720,33,"720p-crf33"),(960,540,32,"540p-crf32"),(960,540,35,"540p-crf35")]:
    out=f".work/probe/hero-{label}.mp4"
    vf=f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    r=subprocess.run(["ffmpeg","-y","-v","error","-ss","29.5","-t","9.0","-i",SRC,
        "-vf",vf,"-r","30","-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
        "-crf",str(crf),"-preset","slow","-an","-movflags","+faststart",out],
        capture_output=True,text=True)
    if r.returncode!=0: print(label,"FAIL",r.stderr[-200:]); continue
    print(f"{label:12s} {w}x{h} crf{crf}  {os.path.getsize(out)/1024:7.1f} KB")
print(f"{'当前线上':12s} 1280x720        {os.path.getsize('assets/video/group-sync.mp4')/1024:7.1f} KB")
