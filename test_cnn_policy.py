from rl_toolbox import Runner
from rl_toolbox.agent import PPOAgent
from rl_toolbox.policy import CNNPolicy


def main():
        runner = Runner(
            'CarRacing-v0',
            PPOAgent,
            CNNPolicy,
            record_data=False,
            data_path=None,
            save=True,
            load=False,
            weight_path='./weights/')

        runner.run(extra_message='simple')


if __name__ == '__main__':
    main()
