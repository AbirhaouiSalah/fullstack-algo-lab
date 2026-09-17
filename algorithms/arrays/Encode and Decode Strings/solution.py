class Solution:

    def encode(self, strs):
        encoded_string = ""
        if strs[0] == "":
            return strs[0]

        for s in strs:
            encoded_string += s + "#"

        return encoded_string

    def decode(self, s: str):
        encoded_string = []
        if s == "":
            return [""]

        splited_string = s.split("#")

        for part in splited_string:

            if part == "#" or part == "":
                continue
            encoded_string.append(part)

        return encoded_string


class Solution2:
    DELIM = "\ue000"

    def encode(self, strs) -> str:
        return self.DELIM.join(strs)

    def decode(self, s: str):
        return s.split(self.DELIM)


class Solution3:
    def encode(self, strs: list[str]) -> str:
        encoded_parts = []
        for s in strs:
            # Combine the three important pieces:
            # length + separator + content
            encoded_parts.append(str(len(s)))
            encoded_parts.append("#")
            encoded_parts.append(s)
        return "".join(encoded_parts)

    def decode(self, encoded: str) -> list[str]:
        decoded = []
        i = 0
        n = len(encoded)

        while i < n:
            # 1. Read the length digits until the separator '#'
            j = i
            while j < n and encoded[j] != "#":
                j += 1

            length = int(encoded[i:j])

            # 2. Skip the separator '#'
            start = j + 1

            # 3. Read exactly `length` characters as the content
            end = start + length
            decoded.append(encoded[start:end])

            # Move to the next encoded string
            i = end

        return decoded


def solve():
    # TODO: implement solution
    pass
