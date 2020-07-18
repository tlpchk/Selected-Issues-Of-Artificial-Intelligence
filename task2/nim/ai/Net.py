import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch import optim, tanh
from torch.autograd import Variable
from torch.nn.functional import relu
from torch.utils.data import Dataset
from torch.utils.data.sampler import SubsetRandomSampler


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(5, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 1)

        self.lossFunction = nn.MSELoss()  # nn.NLLLoss()

    def forward(self, x):
        x = relu(self.fc1(x))
        x = relu(self.fc2(x))
        x = 2 * tanh(self.fc3(x))
        return x

    def train_network(self, loader, epochs=2, lr=3e-3, momentum=0.9, log_interval=10):
        optimizer = optim.SGD(self.parameters(), lr=lr, momentum=momentum)

        for epoch in range(epochs):
            for batch_idx, (data, target) in enumerate(loader):
                data, target = Variable(data), Variable(target)
                optimizer.zero_grad()
                pred = self(data).squeeze()
                loss = self.lossFunction(pred, target)
                loss.backward()
                optimizer.step()

                if batch_idx % log_interval == 0:
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                        epoch, batch_idx * len(data), len(data) * len(loader), 100. * batch_idx / len(loader),
                        loss.item()))
            net.valid(loader=valid_ldr)

    def valid(self, loader):
        valid_loss = 0
        for batch_idx, (data, target) in enumerate(loader):
            data, target = Variable(data), Variable(target)
            pred = self(data).squeeze()
            valid_loss += self.lossFunction(pred, target).item()

        valid_loss /= len(loader)
        print('\nTest set: Average loss: {:.4f}'.format(valid_loss))


class Net1row(Net):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3, 64)


class CustomDatasetFromCSV(Dataset):
    def __init__(self, csv_path):
        data_frame = pd.read_csv(csv_path, delimiter=';', header=None).astype('float32')
        self.data = torch.tensor(data_frame.values)

    def __getitem__(self, index):
        return self.data[index, :-1], self.data[index, -1]

    def __len__(self):
        return self.data.shape[0]


def get_loaders(batch_size=200, validation_split=.2, shuffle_dataset=True, random_seed=42):
    dataset = CustomDatasetFromCSV(DATASET_PATH)

    # Indices for train and valid
    dataset_size = len(dataset)
    indices = list(range(dataset_size))
    split = int(np.floor(validation_split * dataset_size))
    train_indices, val_indices = indices[split:], indices[:split]

    # shuffle data
    if shuffle_dataset:
        np.random.seed(random_seed)
        np.random.shuffle(indices)

    # samplers and loaders
    train_sampler = SubsetRandomSampler(train_indices)
    valid_sampler = SubsetRandomSampler(val_indices)

    train_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, sampler=train_sampler)
    validation_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, sampler=valid_sampler)

    return train_loader, validation_loader


OUTPUT_PATH = '../data/model3row_standard.pth'
DATASET_PATH = '../data/history3row.csv'
# train = True
train = False

if __name__ == "__main__":
    net = Net()
    train_ldr, valid_ldr = get_loaders(batch_size=256)

    if train:
        net.train_network(loader=train_ldr, log_interval=1000)
        torch.save(net.state_dict(), OUTPUT_PATH)
        # net.valid(loader=valid_ldr)
    else:
        net.load_state_dict(torch.load(OUTPUT_PATH))
        # net.valid(loader=valid_ldr)
        print(net(torch.tensor([10., 10., 10., 2., 10.])))
