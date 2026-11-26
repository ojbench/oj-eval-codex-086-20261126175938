#include <iostream>
#include <utility>
#include <vector>

struct Node {
    int left;
    int right;
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;
    std::vector<Node> nodes(n + 1);
    for (int i = 1; i <= n; ++i) {
        std::cin >> nodes[i].left >> nodes[i].right;
    }

    // Swaps preserve depths, so these values remain valid for all queries.
    std::vector<int> depth(n + 1);
    std::vector<int> stack;
    stack.reserve(n);
    stack.push_back(1);
    depth[1] = 1;
    while (!stack.empty()) {
        int node = stack.back();
        stack.pop_back();
        for (int child : {nodes[node].left, nodes[node].right}) {
            if (child != -1) {
                depth[child] = depth[node] + 1;
                stack.push_back(child);
            }
        }
    }

    int queries;
    std::cin >> queries;
    while (queries--) {
        int k;
        std::cin >> k;
        for (int node = 1; node <= n; ++node) {
            if (depth[node] % k == 0) {
                std::swap(nodes[node].left, nodes[node].right);
            }
        }

        int current = 1;
        bool first = true;
        while (current != -1 || !stack.empty()) {
            while (current != -1) {
                stack.push_back(current);
                current = nodes[current].left;
            }
            current = stack.back();
            stack.pop_back();
            if (!first) std::cout << ' ';
            first = false;
            std::cout << current;
            current = nodes[current].right;
        }
        std::cout << '\n';
    }
}
