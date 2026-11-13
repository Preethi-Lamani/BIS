
import numpy as np

fault_matrix = np.array([
    [1, 0, 0, 0],  # T1 detects F1
    [0, 1, 0, 0],  # T2 detects F2
    [1, 1, 1, 0],  # T3 detects F1, F2, F3
    [0, 0, 1, 1],  # T4 detects F3, F4
    [0, 0, 0, 1]   # T5 detects F4
])

test_names = ["T1", "T2", "T3", "T4", "T5"]
num_tests, num_faults = fault_matrix.shape

def calculate_apfd(order):
    tf_sum = 0
    for fault_idx in range(num_faults):
        for position, test_idx in enumerate(order):
            if fault_matrix[test_idx, fault_idx] == 1:
                tf_sum += position + 1
                break

    apfd = 1 - (tf_sum / (num_tests * num_faults)) + (1 / (2 * num_tests))
    return apfd

def decode_wolf(position_vector):
    return np.argsort(position_vector)

def gwo_test_prioritization(num_wolves=10, max_iter=20, seed=42):
    np.random.seed(seed)

    wolves = np.random.uniform(-1, 1, (num_wolves, num_tests))

    alpha_pos = np.zeros(num_tests)
    alpha_score = -float("inf")

    beta_pos = np.zeros(num_tests)
    beta_score = -float("inf")

    delta_pos = np.zeros(num_tests)
    delta_score = -float("inf")

    for t in range(max_iter):
        for i in range(num_wolves):
            test_order = decode_wolf(wolves[i])
            fitness = calculate_apfd(test_order)

            if fitness > alpha_score:
                delta_score, delta_pos = beta_score, beta_pos.copy()
                beta_score, beta_pos = alpha_score, alpha_pos.copy()
                alpha_score, alpha_pos = fitness, wolves[i].copy()

            elif fitness > beta_score:
                delta_score, delta_pos = beta_score, beta_pos.copy()
                beta_score, beta_pos = fitness, wolves[i].copy()

            elif fitness > delta_score:
                delta_score, delta_pos = fitness, wolves[i].copy()

        a = 2 - t * (2 / max_iter)

        for i in range(num_wolves):
            for j in range(num_tests):
                r1, r2 = np.random.rand(), np.random.rand()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha_pos[j] - wolves[i, j])
                X1 = alpha_pos[j] - A1 * D_alpha

                r1, r2 = np.random.rand(), np.random.rand()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta_pos[j] - wolves[i, j])
                X2 = beta_pos[j] - A2 * D_beta

                r1, r2 = np.random.rand(), np.random.rand()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta_pos[j] - wolves[i, j])
                X3 = delta_pos[j] - A3 * D_delta

                wolves[i, j] = (X1 + X2 + X3) / 3.0

        if (t + 1) % 5 == 0 or t == 0:
            current_seq = [test_names[idx] for idx in decode_wolf(alpha_pos)]
            print(f"Iteration {t+1:02d} | Best APFD: {alpha_score:.4f} | Order: {current_seq}")

    return decode_wolf(alpha_pos), alpha_score

unprioritized_order = [0, 1, 2, 3, 4]
initial_apfd = calculate_apfd(unprioritized_order)

print("--- Unprioritized Execution ---")
print(f"Order: {test_names} | APFD: {initial_apfd:.4f} ({initial_apfd*100:.2f}%)")

print("\n--- GWO Optimization Progress ---")
best_order_idx, best_apfd = gwo_test_prioritization()
best_order_names = [test_names[idx] for idx in best_order_idx]

print("\n--- Final Prioritized Result ---")
print(f"Optimal Alpha Order: {best_order_names}")
print(f"Optimized APFD: {best_apfd:.4f} ({best_apfd*100:.2f}%)")
print(f"Improvement: +{(best_apfd - initial_apfd)*100:.2f}%")
