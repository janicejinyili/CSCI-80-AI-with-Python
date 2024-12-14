import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Check for each value in the domains if it meets the length requirement of the variable
        for var,domain in self.domains.items():
            domain_cp = domain.copy()
            for d in domain_cp:
                if var.length != len(d):
                    self.domains[var].remove(d)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Initialize revised bool and check if there's overlap
        revised = False
        if self.crossword.overlaps[x, y] == None:
            return revised

        # Loop over X's and Y's domains to make sure the binary contraints are met
        x_domain = self.domains[x].copy()
        y_domain = self.domains[y].copy()
        for x_string in x_domain:
            satisfied = False
            for y_string in y_domain:

                # Check if x_string and y_string have overlap at the location specified by self.crossword.overlaps
                if x_string[self.crossword.overlaps[x, y][0]] == y_string[self.crossword.overlaps[x, y][1]]:
                    satisfied = True
            if satisfied == False:

                # If none of the values in Y's domain satisfies the overlap requirement, x_string is removed from the domain
                self.domains[x].remove(x_string)
                revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Define arcs when they are not passed through
        if arcs == None:
            arcs = {(x, y) for x in self.crossword.variables for y in self.crossword.variables if x != y}
        while len(arcs) != 0:
            (X, Y) = arcs.pop()
            if self.revise(X, Y):

                # If the arc is revised, check if the domian of X became 0 in which case False should be returned, 
                # then add all X's arcs with it's neighbor to the queue
                if len(self.domains[X]) == 0:
                    return False
                for Z in self.crossword.neighbors(X):
                    arcs.add((Z, X))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        #Check if assignment has all variables
        return len(assignment) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if there are duplicate strings
        if len(list(assignment.values())) != len(set(assignment.values())):
            return False

        # Check if unary constraints are met
        if any(var.length != len(string) for var, string in assignment.items()):
            return False 

        # Check if binary constraints are met
        for var in assignment.keys():
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment.keys():
                    continue
                if assignment[var][self.crossword.overlaps[(var, neighbor)][0]] != assignment[neighbor][self.crossword.overlaps[(var, neighbor)][1]]:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        ordered_values = list(self.domains[var])
        def heuristic(value):
            h = 0

            # Exclude neighbors that are already assigned
            for neighbor in self.crossword.neighbors(var) - set(assignment.keys()):
                for value_n in self.domains[neighbor]:

                    # heuristic is defined as number of values in the neighbor's domain that doesn't satisfy the overlap requirement
                    if value[self.crossword.overlaps[(var, neighbor)][0]] != value_n[self.crossword.overlaps[(var, neighbor)][1]]:
                        h += 1
            return h
        return sorted(list(self.domains[var]), key = heuristic)

        # return list(i for i in self.domains[var] if i not in assignment.keys())

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Get a list of unassigned variables
        unassigned_var = list(self.crossword.variables - set(assignment.keys()))

        # Order the list by min number of values in domain & max number of neighbors
        return sorted(unassigned_var, key = lambda v: (len(self.domains[v]), -len(self.crossword.neighbors(v))))[0]
        # return list(self.crossword.variables - set(assignment.keys()))[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Return assignment if complete
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable, loop over the values in it's domain and check if consistency is met
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value 
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        # If all values in the domain have been looped over yet no result is found, return none
        return None



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
