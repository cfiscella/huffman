from ds import btree, pqueue


class HuffmanEncoder:

    def __init__(self, baseMessage):
        self.tree = self._make_tree(baseMessage)
        self.codex = self._build_codex(self.tree)
        self.encodedBaseMessage = self.encode(baseMessage)

    def encode(self, message):
        res = ""
        for char in message:
            res += self.codex["encoder"][char]
        return res

    def decode(self, bitstring):
        curr_b_str = ""
        res = ""
        decoder_codex = self.codex["decoder"]
        for char in bitstring:
            curr_b_str += char
            if curr_b_str in decoder_codex:
                res += decoder_codex[curr_b_str]
                curr_b_str = ""
        return res

    def _calc_frequencies(self, message):
        freq = {}
        for c in message:
            if c in freq:
                oldFreqVal = freq[c]
                freq[c] = [oldFreqVal[0], oldFreqVal[1] + 1]
            else:
                freq[c] = [btree(c), 1]
        return freq

    def _make_tree(self, message):
        # 1. calculate frequencies
        frequencies = self._calc_frequencies(message)
        # 2. make priority queue
        q = pqueue(list(frequencies.values()), invert=True)
        # 3. build tree from bottom up
        self.tree = btree()
        while len(q) > 1:
            # dqueue 2 smallest potential nodes
            node1 = q.poll()
            node2 = q.poll()
            # calculate the sum of their lengs
            nodesum = node1.priority + node2.priority
            # make new tree with summed data
            new_tree = btree(nodesum, node1.value, node2.value)
            # enqueue new tree back
            q.add((nodesum, new_tree))
        final_node = q.poll().value
        return final_node

    def _build_codex(self, tree):
        curr_str = ""
        codex = {"encoder": {}, "decoder": {}}

        def pre_walk(node, direction):
            nonlocal curr_str
            node_data = node.data
            if direction == "left":
                curr_str += "0"
            elif direction == "right":
                curr_str += "1"
            if isinstance(node_data, str):
                codex["encoder"][node_data] = curr_str
                codex["decoder"][curr_str] = node_data

        def post_walk(node, direction):
            nonlocal curr_str
            if direction != "root":
                curr_str = curr_str[:-1]

        tree.dfs_walk(pre_walk_callback=pre_walk, post_walk_callback=post_walk)
        return codex


if __name__ == "__main__":
    string = "BCAADDDCCACACAC"
    my_encoder = HuffmanEncoder(string)
    print(my_encoder.encodedBaseMessage)
    print(my_encoder.decode(my_encoder.encodedBaseMessage))
    print("correct answer", string)
    print("full lengh of stirng")
    print(string == my_encoder.decode(my_encoder.encodedBaseMessage))
