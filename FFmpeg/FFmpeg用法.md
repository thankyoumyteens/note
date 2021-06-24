# 语法

```
ffmpeg [全局参数] [输入文件参数] -i [输入文件] [输出文件参数] [输出文件]
```

## 例子

将 mp4 文件转成 webm 文件

- 输入的 mp4 文件的音频编码格式是 aac，视频编码格式是 H.264
- 输出的 webm 文件的视频编码格式是 VP9，音频格式是 Vorbis
- 如果不指明编码格式，FFmpeg 会自己判断输入文件的编码

```
ffmpeg \
-y \
-c:a libfdk_aac -c:v libx264 \
-i input.mp4 \
-c:v libvpx-vp9 -c:a libvorbis \
output.webm
```

# 常用命令行参数

- `-c`：指定编码器
- `-c copy`：直接复制，不经过重新编码（这样比较快）
- `-c:v`：指定视频编码器
- `-c:a`：指定音频编码器
- `-i`：指定输入文件
- `-an`：去除音频流
- `-vn`： 去除视频流
- `-preset`：指定输出的视频质量，会影响文件的生成速度，有以下几个可用的值 ultrafast, superfast, veryfast, faster,fast, medium, slow, slower, veryslow。
- `-y`：不经过确认，输出时直接覆盖同名文件。
