import random


class Chessboard:
    def __init__(self, *args):
        if len(args) < 1:  # CONSTRUCTOR
            self.team_white = []  # list containing white pieces
            self.team_black = []  # list containing black pieces
            self.board = []

            self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]  # position
            self.numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]  # height

            # creates and enumerate cb matrix[Depth][position] 8x8
            for height in range(len(self.numbers)):
                current_row = []
                for position in range(len(self.letters)):
                    current_row.append(self.letters[position] + self.numbers[height])
                self.board.append(current_row)

        elif len(args) == 1 and type(args[0]) == Chessboard:  # COPY CONSTRUCTOR
            self.team_white = args[0].team_white
            self.team_black = args[0].team_black
            self.board = args[0].board

            self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]  # position
            self.numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]  # height

        else:
            print("copy constructor only takes one parameter")

    def place_piece(self, piece, pos: str, team: str):
        position = self.translate_pos(pos)

        # checks if queen is not present already
        if self.board[position[0]][position[1]] != "Qb" or self.board[position[0]][position[1]] != "Qw":
            self.board[position[0]][position[1]] = "Q" + piece.team[0]  # places queen
        else:
            print("position occupied")

    def print_board(self):

        for height in range(len(self.numbers)):
            aux = []
            for position in range(len(self.letters)):
                aux.append(self.board[height][position])
            print("\t", aux)

    # turns chess positions into matrix[][] positions
    def translate_pos(self, pos: str):
        for height in range(len(self.numbers)):
            for position in range(len(self.letters)):
                if self.letters[position] == pos[0] and self.numbers[height] == pos[1]:
                    return height, position
                else:
                    print("position not found")

    # flips chessboard matrix
    def invert(self):
        inverted_board = []

        # inverts matrix
        for height in reversed(range(len(self.numbers))):
            current_row = []
            for position in reversed(range(len(self.letters))):
                current_row.append(self.board[height][position])
            inverted_board.append(current_row)

        # renames elements
        for height in range(len(self.numbers)):
            for position in range(len(self.letters)):
                if inverted_board[height][position] != "Qw" and inverted_board[height][position] != "Qb":
                    inverted_board[height][position] = \
                        self.letters[position] + self.numbers[height]

        self.board = inverted_board

    def play(self):
        solution = False
        cQ1w = 0
        cQ2w = 0
        cQ1b = 0
        cQ2b = 0

        # Queens
        Q1w = Queen("white", [0, 0], self)
        Q2w = Queen("white", [0, 7], self)
        Q1b = Queen("black", [7, 0], self)
        Q2b = Queen("black", [7, 7], self)

        # input report
        print("***Input Report***")
        print("Starting positions: ")
        self.print_board()

        # objective
        objective = Chessboard(self)
        objective.invert()

        while not solution:
            # white movements
            if self.board[Q1w.placement[0]][Q1w.placement[1]] != objective.board[Q1w.placement[0]][Q1w.placement[1]]:
                Q1w.random_move(self)
                cQ1w += 1
            if self.board[Q2w.placement[0]][Q2w.placement[1]] != objective.board[Q2w.placement[0]][Q2w.placement[1]]:
                Q2w.random_move(self)
                cQ2w += 1

            # black movements
            if self.board[Q1b.placement[0]][Q1b.placement[1]] != objective.board[Q1b.placement[0]][Q1b.placement[1]]:
                Q1b.random_move(self)
                cQ1b += 1
            if self.board[Q2b.placement[0]][Q2b.placement[1]] != objective.board[Q2b.placement[0]][Q2b.placement[1]]:
                Q2b.random_move(self)
                cQ2b += 1

            if self.board == objective.board:
                solution = True

        # output report
        print("\n\n***Output Report***")
        print("Number of moves: ", cQ1w + cQ2w + cQ1b + cQ2b)
        print("Final board: ")
        self.print_board()
        print("\nNumber of Q1w moves: ", cQ1w)
        print("Q1w move history: ", Q1w.visited_pos)
        print("\nNumber of Q2w moves: ", cQ2w)
        print("Q2w move history: ", Q2w.visited_pos)
        print("\nNumber of Q1b moves: ", cQ1b)
        print("Q1b move history: ", Q1b.visited_pos)
        print("\nNumber of Q2b moves: ", cQ2b)
        print("Q2b move history: ", Q2b.visited_pos)


class Queen:
    def __init__(self, team: str, pos: list[int], cb: Chessboard):
        self.team = team
        self.letters = ["A", "B", "C", "D", "E", "F", "G", "H"]  # position
        self.numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]  # height
        self.placement = [pos[0], pos[1]]  # [height][position]
        cb.board[pos[0]][pos[1]] = "Q" + self.team[0]
        self.visited_pos = []
        # self.visited_pos.append(self.letters[pos[1]] + self.numbers[pos[0]])

    # def move(self, cb: Chessboard, pos: tuple[int]):

    def random_move(self, cb: Chessboard):
        possible_moves = self.check(cb)  # returns list of possible positions
        # chooses next position
        move = possible_moves[random.randint(0, len(possible_moves) - 1)]
        # adds old position to visited positions
        self.visited_pos.append(self.letters[self.placement[1]] + self.numbers[self.placement[0]])
        # cleans old position
        cb.board[self.placement[0]][self.placement[1]] = \
            self.letters[self.placement[1]] + self.numbers[self.placement[0]]
        # places piece in new position
        cb.board[move[0]][move[1]] = "Q" + self.team[0]
        # saves new position in object
        self.placement = [move[0], move[1]]

    def check(self, cb: Chessboard):
        possible_moves = []
        height = self.placement[0]
        position = self.placement[1]
        size = len(cb.letters)

        # check horizontally (fixed: y)
        for element in range(len(cb.letters)):
            if not (cb.board[height][element] == "Qw" or cb.board[height][element] == "Qb") \
                    and cb.board[height][element] not in self.visited_pos:
                possible_moves.append([height, element])

        # check vertically (fixed: x)
        for element in range(len(cb.numbers)):
            if not (cb.board[element][position] == "Qw" or cb.board[element][position] == "Qb") \
                    and cb.board[element][position] not in self.visited_pos:
                possible_moves.append([element, position])

        # check diagonally (upwards)
        aux_Height = height
        aux_Pos = position

        while aux_Height < size - 1 and aux_Pos > 0:  # goes to the bottom left of the diagonal
            aux_Height += 1
            aux_Pos -= 1

        while aux_Height >= 0 and aux_Pos <= size - 1:
            if not (cb.board[aux_Height][aux_Pos] == "Qw" or cb.board[aux_Height][aux_Pos] == "Qb") \
                    and cb.board[aux_Height][aux_Pos] not in self.visited_pos:
                possible_moves.append([aux_Height, aux_Pos])
            aux_Height -= 1
            aux_Pos += 1

        # check diagonally (downwards)
        aux_Height = height
        aux_Pos = position

        while aux_Height > 0 and aux_Pos > 0:
            aux_Height -= 1
            aux_Pos -= 1

        while aux_Height <= size - 1 and aux_Pos <= size - 1:
            if not (cb.board[aux_Height][aux_Pos] == "Qw" or cb.board[aux_Height][aux_Pos] == "Qb") \
                    and cb.board[aux_Height][aux_Pos] not in self.visited_pos:
                possible_moves.append([aux_Height, aux_Pos])
            aux_Height += 1
            aux_Pos += 1

        # failsafe in case piece traps itself
        if len(possible_moves) == 0:
            self.visited_pos = []
            possible_moves = self.check(cb)

        return possible_moves


# graveyard
"""
 def check(self):
        for depth in range(self.Size):
            for position in range(self.Size):
                if self.Board[depth][position] == 11:
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

                    while aux_Depth >= 0 and aux_Pos <= self.Size - 1:
                        if self.Board[aux_Depth][aux_Pos] == "Q":
                            checks += 1
                        aux_Depth -= 1
                        aux_Pos += 1

                    # check diagonally (downwards)
                    aux_Depth = depth
                    aux_Pos = position

                    while aux_Depth > 0 and aux_Pos > 0:
                        aux_Depth -= 1
                        aux_Pos -= 1

                    while aux_Depth <= self.Size - 1 and aux_Pos <= self.Size - 1:
                        if self.Board[aux_Depth][aux_Pos] == 1:
                            checks += 1
                        aux_Depth += 1
                        aux_Pos += 1

                    if checks > 4:
                        print("Not Possible")
                        return False
"""