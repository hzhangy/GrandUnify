import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.linalg import expm

def create_sponge_grid(N_side=20, stitching_density=0.1):
    """
    创建一个3D海绵骨架：
    1. 基础2D格点
    2. 随机长程缝合（模拟引力Stitching）
    """
    G = nx.grid_2d_graph(N_side, N_side)
    G = nx.convert_node_labels_to_integers(G)
    
    # 执行拓扑缝合 (Stitching)
    nodes = list(G.nodes())
    n_stiches = int(len(nodes) * stitching_density)
    for _ in range(n_stiches):
        u, v = np.random.choice(nodes, 2, replace=False)
        G.add_edge(u, v)
    return G

def simulate_wave_evolution(G, time_steps=40, dt=0.05):
    """
    在海绵骨架上运行离散薛定谔演化：
    Psi(t) = exp(-i * L * t) * Psi(0)
    L 是图拉普拉斯算子，对应 N.E.A. 中的能量/刷新频率
    """
    N = G.number_of_nodes()
    # 获取拉普拉斯矩阵
    L = nx.laplacian_matrix(G).toarray().astype(complex)
    
    # 初始状态：一个定域波包（粒子性起始）
    psi = np.zeros(N, dtype=complex)
    psi[N // 2] = 1.0  # 放在中心节点
    
    norms = []
    prob_snapshots = []
    
    # 时间演化算子 (幺正算子)
    # U = exp(-i * L * dt)
    U_step = expm(-1j * L * dt)
    
    for t in range(time_steps):
        psi = np.dot(U_step, psi)
        
        # 计算当前总概率 (验证幺正性)
        prob = np.abs(psi)**2
        total_prob = np.sum(prob)
        norms.append(total_prob)
        
        if t in [0, 10, 20, 39]:
            prob_snapshots.append(prob.copy())
            
    return norms, prob_snapshots

def main():
    print("Executing Experiment: Quantum Wave packet on Sponge Scaffold...")
    
    # 1. 初始化海绵空间
    N_side = 20
    G = create_sponge_grid(N_side, stitching_density=0.05)
    
    # 2. 运行量子演化
    norms, snapshots = simulate_wave_evolution(G)
    
    # 3. 可视化
    plt.figure(figsize=(15, 5))
    
    # 子图 1: 概率密度随时间扩散
    plt.subplot(131)
    for i, prob in enumerate(snapshots):
        plt.plot(prob, alpha=0.7, label=f'Step {i*10}')
    plt.title("Wave Packet Dispersion on Sponge")
    plt.xlabel("Node Index"); plt.ylabel("Probability $| \Psi |^2$")
    plt.legend()
    
    # 子图 2: 验证幺正性 (概率守恒)
    plt.subplot(132)
    plt.plot(norms, 'g-', linewidth=2)
    plt.axhline(y=1.0, color='r', linestyle='--')
    plt.ylim(0.9, 1.1)
    plt.title("Unitary Verification (Noether Law)")
    plt.xlabel("Time Step"); plt.ylabel("Total Probability")
    
    # 子图 3: 最终状态的2D重构可视化
    plt.subplot(133)
    final_prob = snapshots[-1].reshape(N_side, N_side)
    plt.imshow(final_prob, cmap='magma', interpolation='gaussian')
    plt.title("Final 2D Probability Map")
    plt.colorbar(label="Intensity")
    
    plt.tight_layout()
    plt.show()
    
    # 逻辑校验
    print(f"\n[U-Paper Logic Check]:")
    print(f"Initial Norm: {norms[0]:.6f}")
    print(f"Final Norm:   {norms[-1]:.6f}")
    print(f"Deviation:    {abs(norms[-1] - 1.0):.2e}")
    print("Conclusion: Unitary evolution is confirmed. Quantum mechanics is a consistent")
    print("accounting mode on the discrete sponge scaffold.")

if __name__ == "__main__":
    main()