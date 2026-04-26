# 阶段四：音频驱动与口型同步

在针对已有的动态视频进行后期口型同步（Video Dubbing）时，MuseTalk 是目前工业界的绝对标杆。

它的底层逻辑是“局部重绘 (Masked Inpainting)”： 它利用人脸关键点检测（Face Landmarks），精准切割出卡提希娅下半张脸的 Bounding Box，然后只重绘嘴巴这一个局部的像素，完全不破坏我们之前辛苦算出来的头发、衣服和整体光影！
