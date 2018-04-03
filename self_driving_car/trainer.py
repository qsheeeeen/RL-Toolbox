import h5py
import numpy as np
import torch
from torch.autograd import Variable
from torch.nn import SmoothL1Loss
from torch.optim import Adam
from torch.utils.data import TensorDataset, DataLoader
from torch.utils.data.dataset import random_split
from visualdl import LogWriter


class Trainer(object):
    def __init__(self, model, input_shape, output_shape, data_path='./data.hdf5', lr=3e-4):
        self.model = model(input_shape, output_shape)

        self.model_optimizer = Adam(self.model.parameters(), lr=lr)
        self.model_criterion = SmoothL1Loss().cuda()

        self.file = h5py.File(data_path, 'r')

        self.state_dataset = self.file['state']
        self.action_dataset = self.file['action']
        self.reward_dataset = self.file['reward']

        self.logger = LogWriter('./logdir', sync_cycle=100)

        with self.logger.mode('train'):
            self.train_loss = self.logger.scalar('loss/')

        with self.logger.mode('test'):
            self.test_loss = self.logger.scalar('loss/')

    def fit(self, batch_size=32, epochs=100):
        states_array = np.array(self.state_dataset)
        actions_array = np.array(self.action_dataset)

        states_t = self._processing_state(states_array_train)
        actions_t = actions_t = torch.from_numpy(actions_array_train).cuda()

        # TODO
        (states_array_train,
         states_array_test,
         actions_array_train,
         actions_array_test) = random_split(states_array, actions_array)

        del states_array, actions_array

        states_train = self._processing_state(states_array_train)
        actions_train = torch.from_numpy(actions_array_train).cuda()

        training_dataset = TensorDataset(states_train, actions_train)
        training_data_loader = DataLoader(training_dataset, batch_size, shuffle=True)

        states_test = self._processing_state(states_array_test)
        actions_test = torch.from_numpy(actions_array_test).cuda()

        testing_dataset = TensorDataset(states_test, actions_test)
        testing_data_loader = DataLoader(testing_dataset, batch_size, shuffle=True)

        training_step = 0
        testing_step = 0

        train_loader = torch.utils.data.DataLoader(
            datasets.MNIST('../data',
                           train=True,
                           download=True,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])),
            batch_size=args.batch_size,
            shuffle=True, **kwargs)

        test_loader = torch.utils.data.DataLoader(
            datasets.MNIST('../data',
                           train=False,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])),
            batch_size=args.test_batch_size,
            shuffle=True, **kwargs)

        for _ in range(epochs):
            for states, actions in training_data_loader:
                states_var = Variable(states)
                actions_var = Variable(actions)

                means_var, stds_var, values_var = self.model(states_var)

                total_loss = self.model_criterion(means_var, actions_var)

                self.model_optimizer.zero_grad()
                total_loss.backward()
                self.model_optimizer.step()

                self.train_loss.add_record(training_step, float(total_loss))
                training_step += 1

            for states, actions in testing_data_loader:
                states_var = Variable(states)
                actions_var = Variable(actions)

                means_var, stds_var, values_var = self.model(states_var)

                total_loss = self.model_criterion(means_var, actions_var)

                self.test_loss.add_record(testing_step, float(total_loss))
                testing_step += 1

    def save(self, weight_path='./ppo_weights.pth'):
        torch.save(self.model.state_dict(), weight_path)

    @staticmethod
    def _processing_state(x):
        x = torch.from_numpy(x).cuda()
        x = x.permute(0, 3, 1, 2)
        x = x / 128 - 1
        return x
