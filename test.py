import numpy as np
from maraboupy import Marabou
from maraboupy import MarabouCore
import torch
import torchvision
import torchvision.transforms as transforms
import os
import sys

def verify_robustness(model_path, epsilon=0.01):
    # 모델 로드
    print(f"Loading model from {model_path}...")
    network = Marabou.read_onnx(model_path)
    
    # MNIST 테스트 데이터셋에서 첫 번째 이미지를 가져와 입력으로 사용
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
    testset = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    image, label = testset[0] 
    image_np = image.numpy().flatten()
    
    # property
    input_vars = network.inputVars[0][0].flatten()
    for i in range(len(image_np)):
        lb = image_np[i] - epsilon
        ub = image_np[i] + epsilon
        network.setLowerBound(input_vars[i], lb)
        network.setUpperBound(input_vars[i], ub)
    
    output_vars = network.outputVars[0].flatten()
    num_classes = 10
    
    print(f"verifying robustness for class {label}, epsilon {epsilon}")
    
    is_robust = True
    for other_class in range(num_classes):
        if other_class == label:
            continue
        # 부등식 생성: output[other_class] >= output[label]
        eq = Marabou.Equation(MarabouCore.Equation.GE)
        eq.addAddend(1.0, int(output_vars[other_class]))
        eq.addAddend(-1.0, int(output_vars[label]))
        eq.setScalar(0.0)
        network.addEquation(eq)
        
        print(f"Checking if class {label} can be misclassified as {other_class}...")
        exit_code, vals, stats = network.solve()
        
        if exit_code == "sat":
            # adversarial example이 존재함. break
            print(f"Counter-example found for class {other_class}. break.")
            is_robust = False
            break
        
        # 다음 클래스에 대해 검증하기 위해 네트워크 초기화
        network = Marabou.read_onnx(model_path)
        for i in range(len(image_np)):
            network.setLowerBound(input_vars[i], image_np[i] - epsilon)
            network.setUpperBound(input_vars[i], image_np[i] + epsilon)

    if is_robust:
        print(f"Robust: No adversarial examples within epsilon {epsilon}")
    else:
        print(f"Not Robust: Adversarial perturbation exists.")
if __name__ == "__main__":
    ONNX_PATH = "models/mnist_my_cnn.onnx"
    if os.path.exists(ONNX_PATH):
        verify_robustness(ONNX_PATH, epsilon=0.001)
    else:
        print(f"Error: {ONNX_PATH} not found. Please place the ONNX file in this directory.")