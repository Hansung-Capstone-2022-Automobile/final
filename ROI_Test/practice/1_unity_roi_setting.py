import numpy as np
import onnxruntime
from mlagents_envs.environment import UnityEnvironment as UE
import cv2

_SHOW_IMAGE = True

def region_of_interest(img):
    height, width, channel = img.shape
    mask = np.zeros_like(img)

    # only focus bottom half of the screen

    polygon_bottom = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, 0),
        (0, 0),
    ]], np.int32)

    cv2.fillPoly(mask, polygon_bottom, (255,255,255))
    show_image("mask", mask)

    masked_image = cv2.add(img,mask)
    show_image("mask_img", masked_image)
    return masked_image

def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)

env_path = "C:/Users/User/Desktop/Unity/MLAgent_v3/build/DuckieBotProject.exe"
model = "C:/Users/User/Desktop/Unity/MLAgent_v3/Assets/Duckie-999972.onnx"

env = UE(file_name=env_path, seed=1, side_channels=[]) # 현재 생성된 환경 불러오기
env.reset()
sess = onnxruntime.InferenceSession(model)

order = (0, 3, 1, 2)

behavior_name = list(env.behavior_specs)[0] # 행동 이름 받아오기
spec = env.behavior_specs[behavior_name] # 얻은 이름을 바탕으로 관측치
vis_obs = any(len(spec.shape) == 3 for spec in spec.observation_specs)
decision_steps, terminal_steps = env.get_steps(behavior_name)

for index, obs_spec in enumerate(spec.observation_specs):
    env.reset()
    print(len(obs_spec.shape))
    if len(obs_spec.shape) == 3:
        vision = cv2.cvtColor(decision_steps.obs[index][0,:,:,:], cv2.COLOR_RGB2BGR)
        height, width, channel = vision.shape
        #region_of_interest(vision)

        mask = np.zeros_like(vision)

        polygon_bottom = np.array([[
            (0, height * 1 / 2),
            (width, height * 1 / 2),
            (width, 0),
            (0, 0),
        ]], np.int32)

        cv2.fillPoly(mask, polygon_bottom,(255,255,255))
        masked_img = cv2.add(vision, mask)

        cv2.imshow('orig', vision)
        cv2.imshow('mask', mask)
        cv2.imshow('masked',masked_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
