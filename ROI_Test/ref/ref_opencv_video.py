from mlagents_envs.environment import UnityEnvironment as UE

env = UE(file_name='../DuckieBotProject.exe', seed=1, side_channels=[]) # 현재 생성된 환경 불러오기

env.reset()

behavior_name = list(env.behavior_specs)[0] # 행동 이름 받아오기
print(behavior_name) # 출력
spec = env.behavior_specs[behavior_name] # 얻은 이름을 바탕으로 관측치

print("Number of observations : ", len(spec.observation_specs)) # 관측치의 종류

vis_obs = any(len(spec.shape) == 3 for spec in spec.observation_specs)
print("Is there a visual observation ?", vis_obs) # 영상 정보인지 확인

if spec.action_spec.continuous_size > 0:
  print(f"There are {spec.action_spec.continuous_size} continuous actions")
  # 유니티 continuous action -> 물리엔진 사용시
if spec.action_spec.is_discrete():
  print(f"There are {spec.action_spec.discrete_size} discrete actions")
  # 유니티 discrete action -> 끊어진 액션(현재 사용중인 것)/전후진,좌우회전

# For discrete actions only : How many different options does each action has ?
if spec.action_spec.discrete_size > 0:
  for action, branch_size in enumerate(spec.action_spec.discrete_branches):
    print(f"Action number {action} has {branch_size} different options") # 0,1번째 action의 옵션

decision_steps, terminal_steps = env.get_steps(behavior_name)
# decision_steps 다음 스탭이 있을경우 사용되는 스탭, terminal_steps 다음에 할게없어 초기화 할때 사용하는 스탭

# print(spec.action_spec.empty_action(len(decision_steps)))
env.set_actions(behavior_name, spec.action_spec.empty_action(len(decision_steps)))
env.step()

import matplotlib.pyplot as plt
for index, obs_spec in enumerate(spec.observation_specs):
  if len(obs_spec.shape) == 3:
    print("Here is the first visual observation")
    plt.imshow(decision_steps.obs[index][0,:,:,:])
    plt.show()
    # vision = cv2.cvtColor(decision_steps.obs[index][0,:,:,:], cv2.COLOR_RGB2BGR)
    # cv2.imshow('a', vision)
    # cv2.waitKey()
    # cv2.destroyAllWindows()


for index, obs_spec in enumerate(spec.observation_specs):
  if len(obs_spec.shape) == 1:
    print("First vector observations : ", decision_steps.obs[index][0,:])

for episode in range(3):
  env.reset()
  decision_steps, terminal_steps = env.get_steps(behavior_name)
  tracked_agent = -1 # -1 indicates not yet tracking
  done = False # For the tracked_agent
  episode_rewards = 0 # For the tracked_agent
  while not done:
    # Track the first agent we see if not tracking
    # Note : len(decision_steps) = [number of agents that requested a decision]
    if tracked_agent == -1 and len(decision_steps) >= 1:
      tracked_agent = decision_steps.agent_id[0]

    # Generate an action for all agents
    action = spec.action_spec.random_action(len(decision_steps))

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
print("Closed environment")