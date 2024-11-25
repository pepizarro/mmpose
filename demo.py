#!/usr/bin/python3 
from mmpose.apis import MMPoseInferencer

# img_path = 'tests/data/coco/000000000785.jpg'   # replace this with your own image path

federer = 'resources/federer480.mp4'
webcam = "webcam"
# instantiate the inferencer using the model alias
# inferencer = MMPoseInferencer(pose3d="human3d")

inferencer = MMPoseInferencer(
    pose3d='configs/body_3d_keypoint/motionbert/h36m/'
           'test_config.py',
    pose3d_weights='https://download.openmmlab.com/mmpose/v1/body_3d_keypoint/'
                   'pose_lift/h36m/motionbert_ft_h36m-d80af323_20230531.pth',
    device="cuda",
    # show_progress=True
)


result_generator = inferencer(
    webcam,
    show=False,
    return_vis=False,
    pred_out_dir='vis_results/human3d',

    batch_size=2048
)

# Convert to list to get the length
results = list(result_generator)
# length = len(results)
#
#
# results = [result for result in result_generator]
# results = [result for index, result in enumerate(result_generator) if index % 2 == 0]

