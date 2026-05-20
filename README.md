# Reliable-and-Trustworthy-AI_Assignment_3

## Start Using Docker
Docker를 통해 즉시 검증을 수행할 수 있습니다.

```bash
# 빌드
docker build -t marabou-verify .

# 검증 실행
docker run marabou-verify
```

📊 Verification Result
- Target Model: 2-layer CNN (98.8% Accuracy)
- Test Image: MNIST Test Set Index 0 (Label: 7)
- Property: $L_\infty$-norm distance $\epsilon = 0.001$
- Status: PROVEN ROBUST (All 9 target classes returned UNSAT)
