import numpy as np
import onnxruntime
from mlagents_envs.environment import UnityEnvironment as UE
import cv2
import torchvision.transforms as transforms

env_path = "C:/Users/User/Desktop/Unity/MLAgent_v3/build_circle/DuckieBotProject.exe"
model = "C:/Users/User/Desktop/Unity/MLAgent_v3/Assets/Duckie-999972.onnx"
order = (0, 3, 1, 2) # 모델 input으로 넣기 위한 transpose 순서

env = UE(file_name=env_path, seed=1, side_channels=[]) # 현재 생성된 환경 불러오기
env.reset()
sess = onnxruntime.InferenceSession(model)
to_tensor = transforms.ToTensor()

behavior_name = list(env.behavior_specs)[0]
spec = env.behavior_specs[behavior_name]

for episode in range(3):
    env.reset()
    # decision_steps : 다음 스텝이 있을 경우에 해당하는 스텝
    # terminal_steps : 다음 스텝이 없어서 초기화하는 스텝
    decision_steps, terminal_steps = env.get_steps(behavior_name)
    tracked_agent = -1 # -1 indicates not yet tracking
    done = False # For the tracked_agent
    episode_rewards = 0 # For the

    while not done:
        ###### OpenCV -> ROI #######
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
        for index, obs_spec in enumerate(spec.observation_specs):
            frame = cv2.cvtColor(decision_steps.obs[index][0, :, :, :], cv2.COLOR_RGB2BGR)

            ### 이미지 자르기 ###
            height, width, channel = frame.shape
            crop = frame[int(height/2):, :, :]
            #  image = cv2.resize(image, (200,66)) # input image size (200,66) Nvidia model
            crop_resize = cv2.resize(crop, (width, height))
            img = to_tensor(crop_resize)
            Input_crop = np.expand_dims(img,axis=0)
            cv2.imshow('crop',crop_resize)

            ### ROI ###
            '''
            height, width, channel = frame.shape
            mask = np.zeros_like(frame)
            polygon_bottom = np.array([[
                (0, height * 1/2), ## 1/2
                (width, height * 1/2), ##1/2
                (width, 0),
                (0, 0),
            ]], np.int32)
            cv2.fillPoly(mask, polygon_bottom, (255, 255, 255))
            masked_img = cv2.add(frame, mask)

            # ROI
            img = to_tensor(masked_img)
            Input_mask = np.expand_dims(img, axis=0)
            cv2.imshow('frame', masked_img)
            '''

            '''
            #orgin
            img = to_tensor(frame)
            Input_orig = np.expand_dims(img, axis=0)
            cv2.imshow('frame', frame)
            '''

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                message = "exit"
                break
            # cv2.waitKey()
            # cv2.destroyAllWindows()

        # Track the first agent we see if not tracking
        # Note : len(decision_steps) = [number of agents that requested a decision]
        if tracked_agent == -1 and len(decision_steps) >= 1:
            tracked_agent = decision_steps.agent_id[0]

        # Generate an action for all agents
        # action = spec.action_spec.random_action(len(decision_steps))

        # unity 환경
        #output = sess.run(["discrete_actions"], {"obs_0": np.array(decision_steps.obs[0]).transpose(order),"action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

        # opencv 환경 (Origin)
        #output = sess.run(["discrete_actions"], {"obs_0": np.array(Input_orig), "action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

        # opencv 환경 (ROI)
        #output = sess.run(["discrete_actions"], {"obs_0": np.array(Input_mask), "action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

        # opencv 환경 (crop)
        output = sess.run(["discrete_actions"], {"obs_0": np.array(Input_crop), "action_masks": np.array([[1., 1., 1., 1., 1.]]).astype(np.float32)})

        # print(output) output으로 얻어내는 결과는 list -> 0번째가 얻어낸 정보 1번째가 타입이다.
        action = spec.action_spec.empty_action(len(decision_steps))
        action.add_discrete(output[0])
        # action.add_discrete(np.array([[1]]))
        # action.add_discrete(np.array([[2]])) 알아낸 성질 add_discrete는 덮어 씌워진다.

        # 출력값 확인하는 곳
        #print(action.discrete)
        print(f'유니티:{np.array(decision_steps.obs[0]).transpose(order).shape}')
        #print(f'OpenCV_orig:{np.array(Input_orig).shape}')
        #print(f'OpenCV_mask:{np.array(Input_mask).shape}')
        print(f'OpenCV_crop:{np.array(Input_crop).shape}')

        # Set the actions
        env.set_actions(behavior_name, action)

        # Move the simulation forward
        env.step()

        # Get the new simulation results
        decision_steps, terminal_steps = env.get_steps(behavior_name)
        if tracked_agent in decision_steps: # The agent requested a decision
            episode_rewards += decision_steps[tracked_agent].reward
        if tracked_agent in terminal_steps: # The agent terminated its episode
            episode_rewards += terminal_steps[tracked_agent].reward
            done = True
    print(f"Total rewards for episode {episode} is {episode_rewards}")

env.close()
cv2.waitKey()
cv2.destroyAllWindows()
print("Closed environment")