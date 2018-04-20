from rl_toolbox import Runner
from rl_toolbox.agent import PPOAgent
from rl_toolbox.policy import MLPPolicy


def main():
    runner = Runner(
        'LunarLanderContinuous-v2',
        PPOAgent,
        MLPPolicy,
        record_data=False,
        data_path=None,
        save=True,
        load=False,
        weight_path='./weights/')

    runner.run(num_episode=500, num_worker=2, train=True)


if __name__ == '__main__':
    main()