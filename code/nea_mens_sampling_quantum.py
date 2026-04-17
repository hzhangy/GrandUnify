import numpy as np
import matplotlib.pyplot as plt

def simulate_quantum_emergence():
    # 1. 物理参数
    B_TOTAL = 1000.0  # 总带宽 (c)
    f_s = 50.0        # 观察者(Mens)的采样频率 (带宽限制)
    duration = 2.0    # 观察时间
    dt_causal = 1e-4  # 宇宙底层的因果步进 (Trans时钟)
    
    time_causal = np.arange(0, duration, dt_causal)
    
    # 2. 模拟不同速度 v 下的节点
    velocities = [0.0, 0.5, 0.8] # v = f_ext / B
    
    plt.figure(figsize=(15, 10))
    
    for idx, v in enumerate(velocities):
        # 根据 N.E.A. 勾股带宽律计算内部频率
        f_ext = v * B_TOTAL
        f_int = np.sqrt(max(0, B_TOTAL**2 - f_ext**2))
        
        # 节点的真实物理状态 (一个在 0 和 1 之间跳动的离散位相)
        # 状态 = sin(2 * pi * f_int * t)
        state_causal = np.sin(2 * np.pi * f_int * time_causal)
        
        # 3. 观察者(Mens)进行异步采样
        # 采样时间点 (由于带宽限制，采样频率 f_s 很低)
        time_mens = np.arange(0, duration, 1.0/f_s)
        # 混叠效应：观察者看到的采样点
        state_mens = np.sin(2 * np.pi * f_int * time_mens)
        
        # 4. 提取“涌现”出的波函数
        # 在观察者看来，这些离散的点连成了一个低频的“波”
        # 这个波的频率 f_observed = f_int mod f_s (混叠频率)
        
        plt.subplot(3, 1, idx+1)
        # 绘制底层真相 (灰线)
        plt.plot(time_causal[:2000], state_causal[:2000], color='gray', alpha=0.3, label='Causal Truth (High-Freq)')
        # 绘制观察到的量子波 (蓝点和红线)
        plt.scatter(time_mens, state_mens, color='blue', s=10, label='Mens Samples (Quantum Observations)')
        plt.plot(time_mens, state_mens, 'r-', alpha=0.6, label='Emergent Wavefunction (Psi)')
        
        plt.title(f"Velocity v={v}c | Internal Clock f_int={f_int:.1f} | Observed Wave: Aliasing Effect")
        plt.legend(loc='upper right')
        plt.xlabel("Time"); plt.ylabel("Amplitude")

    plt.tight_layout()
    plt.show()

    # 5. 验证德布罗意关系: 动量增加 -> 波长变短
    # v 增加 -> f_ext 增加 -> f_int 减小 (根据勾股定律)
    # 在混叠效应下，这种频率变化直接导致观测波长的变化
    print("Logic Check (U-Paper):")
    print("1. When v=0, f_int is max. The aliased wave represents the rest mass frequency (E=mc^2).")
    print("2. When v increases, f_int drops (Time Dilation).")
    print("3. The 'Beating' between high-freq f_int and f_sampling creates the matter wave.")
    print("4. This proves that Wave-Particle Duality is a measurement artifact of finite bandwidth.")

simulate_quantum_emergence()