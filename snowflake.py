# 0 - red, 1 - blue.
import math
import random
from plot_population import plot
from tqdm import tqdm


def main(n, k, alpha, beta, adv, rounds):
    splits = []
    colors = []
    decided = []
    cnt = []
    honest = math.floor(n * (1.0 - adv))

    def total_blues():
        return sum(colors)

    def total_reds():
        return honest - total_blues()

    def query(requester_ind, responder_ind):
        if responder_ind < honest:
            return colors[responder_ind]
        # Adversarial case
        blues = total_blues()
        reds = total_reds()
        if abs(blues - reds) < honest * 0.1:
            return requester_ind % 2
        else:
            return 0 if reds < blues else 1

    for i in range(honest):
        # Initialize with 50/50 split.
        colors.append(i % 2)
        decided.append(False)
        cnt.append(0)

    for r in tqdm(range(rounds)):
        for i in range(honest):
            if decided[i]:
                continue
            peers = random.sample([x for x in range(n) if x != i], k)
            queries = [query(i, p) for p in peers]
            for col in 0, 1:
                if len([q for q in queries if q == col]) > alpha*k:
                    if col != colors[i]:
                        colors[i] = col
                        cnt[i] = 0
                    else:
                        cnt[i] += 1
                        if cnt[i] > beta:
                            decided[i] = True

        if all(decided):
            print("Consensus achieved!")
        splits.append((r, total_reds() / honest))

    return splits


if __name__ == "__main__":
    n = 2000
    k = 10
    alpha = 0.8
    beta = 120
    adv = 0.17
    rounds = 500
    rounds = main(n, k, alpha, beta, adv, rounds)
    plot(rounds, [0.5 - adv, 0.5 + adv], "Snowflake. n={0}; k={1}; alpha={2}; beta={3}; adversaries={4}; ".format(n, k, alpha, beta, adv),
         "/tmp/snowflake.gif")
