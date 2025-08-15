import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=15):
        # Validate number of mines
        if mines > height * width:
            raise ValueError("Number of mines cannot exceed total cells.")

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If all cells in this sentence are mines
        if self.count == len(self.cells) and len(self.cells) > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # 1) Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Determine neighbors of the cell that are still unknown
        neighbors = set()
        r, c = cell

        # Check all neighbors within one cell distance
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Check board boundaries
                if 0 <= i < self.height and 0 <= j < self.width:
                    # If already known mine, reduce count
                    if (i, j) in self.mines:
                        count -= 1
                    # Only include unknown cells
                    elif (i, j) not in self.safes:
                        neighbors.add((i, j))

        # Add a new sentence based on these neighbors
        if neighbors:
            self.knowledge.append(Sentence(neighbors, count))

        # 4) Keep updating knowledge until no new cells are marked
        changed = True
        while changed:
            changed = False
            for sentence in self.knowledge:
                # If a sentence shows all its cells are mines
                for m in sentence.known_mines():
                    if m not in self.mines:
                        self.mark_mine(m)
                        changed = True
                # If a sentence shows all its cells are safe
                for s in sentence.known_safes():
                    if s not in self.safes:
                        self.mark_safe(s)
                        changed = True

        # 5) Infer new sentences using subset logic
        new_sentences = []
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2:
                    continue
                # If s1 is subset of s2, create a new sentence
                if s1.cells and s1.cells.issubset(s2.cells):
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                        new_sentences.append(new_sentence)
                # If s2 is subset of s1, create another sentence
                elif s2.cells and s2.cells.issubset(s1.cells):
                    new_cells = s1.cells - s2.cells
                    new_count = s1.count - s2.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                        new_sentences.append(new_sentence)

        # Add new inferred sentences to knowledge
        self.knowledge.extend(new_sentences)

        # Remove empty sentences (optimization)
        self.knowledge = [s for s in self.knowledge if s.cells]

    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        choices = [(i, j) for i in range(self.height) for j in range(self.width)
                   if (i, j) not in self.moves_made and (i, j) not in self.mines]
        return random.choice(choices) if choices else None
