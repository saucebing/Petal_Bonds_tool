import torch

from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video

import cv2
import os, time

def resize_video(input_path, output_path, size):
    # 创建一个VideoCapture对象来读取视频
    cap = cv2.VideoCapture(input_path)
    
    # 获取视频的帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # 获取视频的宽度和高度
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 创建一个VideoWriter对象来写入新的视频
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 根据需要的格式选择编解码器
    out = cv2.VideoWriter(output_path, fourcc, fps, size)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 调整帧的尺寸
        resized_frame = cv2.resize(frame, size)
        
        # 写入新的帧
        out.write(resized_frame)
    
    # 释放资源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def load_model():
    pipe = StableVideoDiffusionPipeline.from_pretrained("/mnt/afs/data/model/open_source_data/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16")
    #pipe.enable_model_cpu_offload()
    pipe.to("cuda")
    #pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)
    return pipe

def generate_video(pipe, image_filename):
    # Load the conditioning image
    #image = load_image("../images/rocket.png")
    #image = load_image("../images/0000000001_000005_0_Light\'s_Guidance_Mia.png")
    image_filepath = "../images/%s" % image_filename

    # resize image to 1024x576 for video generation
    #image = load_image(image_filepath)
    image = load_image('input.png')
    image = image.resize((1024, 576))

    generator = torch.manual_seed(42)
    frames = pipe(image, decode_chunk_size=8, generator=generator).frames[0]
    export_to_video(frames, "generated.mp4", fps=7)

    # resize video
    input_video_filename = 'generated.mp4'
    output_video_filename = '../videos/%s' % image_filename.replace('.png', '.mp4')
    sizes = [(856, 1200), (856, 836)]
    shape_ind = int(get_flag('shape_ind'))
    resize_video(input_video_filename, output_video_filename, sizes[shape_ind])

def get_flag(fname):
    if os.path.exists(fname):
        f = open(fname, 'r')
        flag = f.read().strip()
        f.close()
        return flag
    else:
        return 'None'

def set_flag(fname, flag):
    f = open(fname, 'w')
    f.write(flag.strip())
    f.close()

if __name__ == '__main__':
    pipe = load_model()
    print('service up')
    while True:
        flag = get_flag('flag')
        if flag == 'start':
            set_flag('flag', 'Doing')
            image_filepath = get_flag('fname')
            print('Begin process %s' % image_filepath)
            generate_video(pipe, image_filepath)
            print('Done process %s' % image_filepath)
            set_flag('flag', 'Done')
        else:
            time.sleep(0.1)
