#!/usr/bin/env bash
# Mix VO segments (placed at their start times from audio/tts.py) over the music bed, ducking music under speech.
set -e
cd "$(dirname "$0")"
D=(0.15 3.15 12.2 18.2 24.2 30.1); N=(hook pain step1 step2 step3 cta)
IN=(); F=""
for i in "${!N[@]}"; do IN+=(-i "audio/${N[$i]}.mp3"); ms=$(python3 -c "print(int(${D[$i]}*1000))"); F+="[$((i+1)):a]adelay=${ms}|${ms},aresample=44100[v$i];"; done
F+="[v0][v1][v2][v3][v4][v5]amix=inputs=6:normalize=0,highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,volume=1.6,asplit[vo][sc];"
F+="[0:a]volume=0.55[m];[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
F+="[md][vo]amix=inputs=2:normalize=0,volume=4dB,alimiter=limit=0.95,apad,atrim=0:33[a]"
ffmpeg -y -i audio/music.wav "${IN[@]}" -filter_complex "$F" -map "[a]" -ar 48000 -ac 2 build/mix.wav -loglevel error
ffmpeg -y -i build/video.mp4 -i build/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart bundles-and-kits-ai-agent-reel.mp4 -loglevel error
ffmpeg -i bundles-and-kits-ai-agent-reel.mp4 -af ebur128 -f null - 2>&1 | grep -A1 "Integrated" | tail -2
