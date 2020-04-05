import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from IPython import embed


def download_data():    
    mnist_train = datasets.MNIST(root='./data', 
                                 train=True, 
                                 download=True, 
                                 transform=None)


# Neural net configuration
class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_layer_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_layer_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_layer_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out


def main():
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Hyper parameters
    input_size = 784
    hidden_layer_size = 500
    num_classes = 10
    num_epochs = 5
    batch_size = 100
    learning_rate = 0.001

    # MNIST dataset
    train_data = torchvision.datasets.MNIST(root='./data', train=True,
                                            transform=transforms.ToTensor(),
                                            download=False)


    test_data = torchvision.datasets.MNIST(root='./data', train=False,
                                           transform=transforms.ToTensor(),
                                           download=False)

    # Load data
    train_loader = torch.utils.data.DataLoader(dataset=train_data, 
                                               batch_size=batch_size,
                                               shuffle=True)

    test_loader = torch.utils.data.DataLoader(dataset=test_data, 
                                              batch_size=batch_size,
                                              shuffle=False)



    # Instantiate model
    model = NeuralNet(input_size, hidden_layer_size, num_classes).to(device)

    # Loss and optim
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Train the model
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (images, labels) in enumerate(train_loader):            
            # Move tensors to device
            images = images.reshape(-1, input_size).to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 100 == 0:
                print ('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}' 
                       .format(epoch + 1, num_epochs, i + 1, total_step, loss.item()))


    # Test
    with torch.no_grad():
        correct = total = 0
        for images, labels in test_loader:
            images = images.reshape(-1, input_size).to(device)
            labels = labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100.0 * float(correct) / float(total)
    print('Accuracy of the network on the 10000 test images: {} %'.format(accuracy))


if __name__ == '__main__':
    # One time download  of data. Activate if you delete the data for some reason
    # download_data()

    # Main training and eval loop
    main()
