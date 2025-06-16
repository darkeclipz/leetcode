class Solution:
    def convert(self, s: str, numRows: int) -> str:
        rows = [[] for _ in range(numRows)]
        select_next_row = self.next_row_generator(rows)
        for letter in s:
            row = next(select_next_row)
            row.append(letter)
        return self.collect(rows)
    def next_row_generator(self, list_of_lists):
        i = 0
        n = len(list_of_lists)
        indices = list(range(n))
        indices.extend(list(range(1, n-1))[::-1])
        while True:
            yield list_of_lists[indices[i%len(indices)]]
            i += 1
    def collect(self, list_of_lists):
        str = ""
        for list in list_of_lists:
            for letter in list:
                str += letter
        return str