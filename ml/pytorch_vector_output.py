import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import Dataset
from IPython import embed


# Neural net configuration
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_layer_size, num_params):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_layer_size, num_params)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


# Synthetic dataset
class SynData(Dataset):
    def __init__(self, X, Y):
        super(SynData, self).__init__()   
        self.X = X
        self.Y = Y

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, index):
        try:
            val = self.X[index, :], self.Y[index, :]
            return val            
        except IndexError:
            import ipdb; ipdb.set_trace()


def main():
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Hyper parameters
    input_size = 4
    hidden_layer_size = 100
    num_params = 2
    num_epochs = 5
    batch_size = 20
    learning_rate = 0.001

    # Synthetic dataset
    np.random.seed(123)
    N = 10000
    x1 = np.linspace(-1.0, 1.0, N)
    X = np.vstack((x1, x1, x1, x1)).T
    X += np.random.normal(loc=0.1, scale=0.1, size=X.shape)
    gamma = np.array([[0.1, 0.2, -0.3, 0.4]])
    gX = np.dot(X, gamma.T)
    y1 = np.exp(-gX)
    y2 = np.cos(np.pi * gX)
    Y = np.hstack((y1, y2))

    # Convert to torch tensors
    X = torch.from_numpy(X).float()
    Y = torch.from_numpy(Y).float()

    # Create datasets
    train_frac = 0.8
    N_train = int(train_frac * N)
    train_data = SynData(X[:N_train, :], Y[:N_train, :])
    test_data = SynData(X[N_train:, :], Y[N_train:, :])

    # Load data
    train_loader = torch.utils.data.DataLoader(dataset=train_data, 
                                               batch_size=batch_size,
                                               shuffle=False)

    test_loader = torch.utils.data.DataLoader(dataset=test_data, 
                                              batch_size=batch_size,
                                              shuffle=False)

    # Instantiate model
    model = NeuralNet(input_size, hidden_layer_size, num_params).to(device)

    # Loss and optim
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (vx, vy) in enumerate(train_loader):            
            vx = vx.to(device)
            vy = vy.to(device)

            outputs = model(vx)              
            loss = criterion(outputs, vy)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))


    # Test
    with torch.no_grad():
        mse_test = 0.0
        mse_bench = 0.0
        y_mean = Y.mean((0, ))
        for vx, vy in test_loader:
            vx = vx.to(device)
            vy = vy.to(device)            
            outputs = model(vx)
            mse_test += ((vy - outputs) ** 2).sum().item()
            mse_bench += ((vy - y_mean) ** 2).sum()

    print('mse_test -> {}, mse_bench -> {}'.format(mse_test, mse_bench))


if __name__ == '__main__':
    # Main training and eval loop
    main()
