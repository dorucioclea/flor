import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

# What if all we did with Doc Dr is document the network (Lines 13-33)
# Basically, just stuff that merits Docstrings... 
# This is exactly the sort of thing that Jupyter does not support
# And this can be a major pain point with debugging in Jupyter.
# E.g. seeing how data changes shape as it moves.

batch_size = 4
num_classes = 10


class Net(nn.Module):
    def __init__(self):
        torch.manual_seed(1217)
        super(Net, self).__init__()
        self.fc1 = nn.Linear(196, 10)
        self.pool = nn.MaxPool2d(2, 2)

    def forward(self, x) -> torch.FloatTensor:
        """DocDr
        x: 
                shape: {x.shape} <->  torch.Size([{batch_size} <-> 4, 1, 28, 28])
                type: {x.type()} <->  'torch.FloatTensor'
        return:
                shape: {ssa.get(x,-1).shape} <->  torch.Size([{batch_size} <-> 4, {num_classes} <-> 10])
                type: {ssa.get(x,-1).type()} <->  'torch.FloatTensor'        
        """
        x = self.pool(x)
        x = x.view(4, -1)
        x = F.relu(self.fc1(x))
        return x


transform = transforms.Compose(
    [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))]
)

trainset = torchvision.datasets.MNIST(
    root="./mnist", train=True, download=True, transform=transform
)
trainloader = torch.utils.data.DataLoader(
    trainset, batch_size=batch_size, num_workers=2)

testset = torchvision.datasets.MNIST(
    root="./mnist", train=False, download=True, transform=transform
)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, num_workers=2)


def eval(net):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    return 100 * correct / total


net = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

EPOCHS = 2

"""DocDr
epochs: ...
lr: ....
batch_size: ....
"""

for epoch in range(EPOCHS):
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000 == 1999:  # print every 2000 mini-batches
            print("[%d, %5d] loss: %.3f" %
                  (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0
    acc = eval(net)

print("Finished Training")
