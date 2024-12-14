import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

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
        if len(self.cells) == self.count:
            return self.cells
        return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        cells_2 = self.cells.copy()
        for c in cells_2:
            if c == cell:
                self.cells.discard(c)
                self.count -= 1
        return True
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        cells_2 = self.cells.copy()
        for c in cells_2:
            if c == cell:
                self.cells.discard(c)
        return True
        raise NotImplementedError


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
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Add surroundings cells and mine count as new knowledge
        surroundings = {(x,y) for x in range(cell[0] - 1,cell[0] + 2) for y in range(cell[1] - 1,cell[1] + 2)}
        surroundings_2=surroundings.copy()
        for s in surroundings:
            if (
                s[0] not in range(self.height)
                or s[1] not in range(self.width)
                or s in self.moves_made
                or s in self.safes
            ):
                surroundings_2.discard(s)
            elif s in self.mines:
                count -= 1
                surroundings_2.discard(s) 
        self.knowledge.append(Sentence(surroundings_2,count))

        # Mark mines and safes according to the new knowledge
        knowledge_2 = copy.deepcopy(self.knowledge)
        for sentence in knowledge_2:
            for mine in sentence.known_mines():
                self.mark_mine(mine)
            for safe in sentence.known_safes():
                self.mark_safe(safe)

        # Add new inferences to the knowledge and update the mines and safes
        while True:
            new_k_created = False
            knowledge_2 = self.knowledge.copy()
            for sen1 in knowledge_2:  
                for sen2 in knowledge_2:
                    if sen1.cells < sen2.cells and len(sen1.cells) != 0:
                        self.knowledge.append(Sentence(sen2.cells - sen1.cells,sen2.count - sen1.count))
                        new_k_created = True
            knowledge_2 = copy.deepcopy(self.knowledge)
            for sentence in knowledge_2:
                for mine in sentence.known_mines():
                    self.mark_mine(mine)
                for safe in sentence.known_safes():
                    self.mark_safe(safe)
            if new_k_created == False:
                return True
        
        return True
   
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) > 0:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return cell
        return None


        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    return (i,j)
        return None




        raise NotImplementedError
