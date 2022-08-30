class Chessboard:
    def __init__(self, n, k):
        self.Queens = k
        self.Size = n
        self.Board = []  # [Depth][position]

        y = 0
        for depth in range(n):
            current_row = []
            for position in range(n):
                current_row.append(y)
                y += 1
            self.Board.append(current_row)

    def check(self):
        for depth in range(self.Size):
            for position in range(self.Size):
                if self.Board[depth][position] == 1:
                    checks = 0
                    # check horizontally (fixed: y)
                    for element in range(self.Size):
                        if self.Board[depth][element] == "Q":
                            checks += 1

                    # check vertically (fixed: x)
                    for element in range(self.Size):
                        if self.Board[element][position] == "Q":
                            checks += 1

                    # check diagonally (upwards)
                    aux_Depth = depth
                    aux_Pos = position

                    while aux_Depth < self.Size - 1 and aux_Pos > 0:  # goes to the bottom left of the diagonal
                        aux_Depth += 1
                        aux_Pos -= 1
                    print(self.Board[aux_Depth][aux_Pos])

                    while aux_Depth >= 0 and aux_Pos <= self.Size - 1:
                        if self.Board[aux_Depth][aux_Pos] == "Q":
                            checks += 1
                        aux_Depth -= 1
                        aux_Pos += 1

                    # check diagonally (downwards)
                    aux_Depth = depth
                    aux_Pos = position


x = Chessboard(4, 1)
print(x.Board)
# print(x.Board[1][0])
x.check()
