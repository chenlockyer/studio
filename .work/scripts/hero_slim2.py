import io,sys,subprocess,os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
SRC=r"D:\my_media\video\unitree_g1\群控\群控.mp4"
for (w,h,crf,dur,label) in [(1280,720,32,6.0,"720p-crf32-6s"),(1280,720,34,7.0,"720p-crf34-7s"),(1280,720,34,6.0,"720p-crf34-6s")]:
    out=f".work/probe/hero-{label}.mp4"
    vf=f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    r=subprocess.run(["ffmpeg","-y","-v","error","-ss","29.5","-t",str(dur),"-i",SRC,
        "-vf",vf,"-r","30","-c:v","libx264","-profile:v","high","-pix_fmt","yuv420p",
        "-crf",str(crf),"-preset","slow","-an","-movflags","+faststart",out],
        capture_output=True,text=True)
    if r.returncode!=0: print(label,"FAIL"); continue
    print(f"{label:16s} {os.path.getsize(out)/1024:7.1f} KB")
