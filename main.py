from ConditionFile import NumericCondition
from NodeFile import BranchNode, LeafNode, GenericNode
from AnswerGroupFile import AnswerGroup
from typing import List, Optional


class DecisionTree:

    def __init__(self):
        self.decision_tree_root: Optional[GenericNode] = None

    def build_condition_tree(self):
        """
        We're building a tree based on 2 questions, "Is it cold outside 1-5" and "Are you dressed warmly? 1-5"
        that will classify the answers either "dressed appropriately" or "dressed inappropriately." Note the
        standard for the warm dress depends on whether it is cold or not.

                                          +-Root-----------+
                                          | 1.cold <= 3    |
                                          +----------------+
                                        /                   \
                                      yes                   no
                                      /                       \
                        +-node_a ------------- +             +-node_b --------------+
                        |  2.dressed_warm <3.5 |             |  3.dressed_warm < 2.5|
                        +--------------------- +             +----------------------+
                       /                \                        /                  \
                    yes                  no                    yes                  no
                    /                     \                   /                       \
                  [Appropriate]     [Inappropriate]       [Inappropriate]           [Appropriate]

        :return: None
        """

        # -------------------------------------

        # TODO: Replace this code with your tree-building code!
        # set up the conditions we'll be using.
        first_condition = NumericCondition(attribute_name="cold", threshold=3)
        second_condition = NumericCondition(attribute_name="dressed_warm",
                                            threshold=3.5)  # Note that conditions 2 and 3 use the same question, but
        third_condition = NumericCondition(attribute_name="dressed_warm", threshold=2.5)  # different thresholds

        # create the first ("root") node
        self.decision_tree_root = BranchNode(first_condition, depth=0)
        # create the nodes meant for first node's children
        node_a = BranchNode(second_condition, depth=1)
        node_b = BranchNode(third_condition, depth=1)

        # link the root node to its children
        self.decision_tree_root.set_yes_node(node_a)
        self.decision_tree_root.set_no_node(node_b)

        # create/link the leaf nodes as child nodes for node_a
        node_a.set_yes_node(LeafNode("Dressed Appropriately", depth=2))
        node_a.set_no_node(LeafNode("Dressed Inappropriately", depth=2))

        # create/link the leaf nodes as child nodes for node_b
        node_b.set_yes_node(LeafNode("Dressed Inappropriately", depth=2))
        node_b.set_no_node(LeafNode("Dressed Appropriately", depth=2))
        # -----------------------------------

        print("---------------------------------------------")
        print("Describing Tree:")
        print(self.decision_tree_root)
        print("---------------------------------------------")

    def predict(self, AG_to_check: AnswerGroup) -> str:
        return self.decision_tree_root.predict(AG_to_check)

# ================================================================= END OF DECISION TREE CLASS

def ask_questions_and_predict(tree: DecisionTree):
    """
    We're going to ask both questions of the user and then have the computer tell us what it thinks about
    our weather/clothing options.
    :return: None
    """
    # ------------------------------------
    # TODO: Replace this code to ask _Your_ questions and make predictions.
    attribute_names = ["cold", "dressed_warm"]
    for i in range(5):
        print(f"Attempt #{i + 1}:")
        cold_response = ask_likert_question("Is it cold outside?")
        dressed_response = ask_likert_question("Are you dressed warmly?")

        AG_to_check = AnswerGroup(attribute_names, [cold_response, dressed_response])
        print(f"Answer Group to check: {AG_to_check}")

        recommendation = tree.predict(AG_to_check)
        print(f"The computer thinks you are: {recommendation}\n")
    # ------------------------------------

def ask_likert_question(prompt: str) -> float:
    """
    prompts the user for a question with a 1-5 range answer. Keeps prompting until the user gives one. Returns the
    (legal) value that the user entered.

    :param prompt: the question to be asked
    :return: a number from 1-5, perhaps a fractional value.
    """
    response = ""  # temp/dummy value - this will get updated.
    result_num = 1  # temp/dummy value - we'll replace this, too.

    good_response = False
    while not good_response:
        try:
            response = input(f"{prompt} Pick a number 1-5 (1=not at all; 5=lots!)")
            result_num = float(response)
            if result_num < 1 or result_num > 5:
                print(f"That number, {result_num}, is out of range.")
            else:
                good_response = True
        except ValueError:  # This will happen if response can't be converted to a number (i.e., a "float").
            print(f"You said {response}. That was not a number.")

    return result_num


# Note: the Choose from list method is not needed for this project, but might be handy if you are exploring the Category Conditions.
def choose_from_list(prompt: str, list_of_choices: List[str]) -> str:
    """
    prints the prompt and asks the user to select from a list of choices. Keeps asking until it gets one.
    (Note responses are case-insensitive, but the same capitalization as found in list is what is returned.)
    :param prompt: A string to print when we ask for a choice
    :param list_of_choices: A list of strings - the only acceptable options that can be returned
    :return: a string from the list of strings, as selected by the user.
    """
    response = ""  # temp - we'll update this value in a couple of lines from now.
    good_response = False
    while not good_response:
        response = input(f"{prompt} Select from {list_of_choices}")
        for choice in list_of_choices:
            if choice.casefold() == response.casefold():  # compare (case-insensitive)
                response = choice  # make sure we get the capitalization version the computer _expects_
                good_response = True
                break  # stop checking for matches - we found one!

        if not good_response:
            print("That did not match your choices. Please try again.")

    return response


if __name__ == '__main__':
    the_tree = DecisionTree
    the_tree.build_condition_tree()
    ask_questions_and_predict(the_tree)

