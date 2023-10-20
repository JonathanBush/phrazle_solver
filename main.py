import re
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Word:
    def __init__(self, length, sowpods):
        self.length = length
        self.might_contain = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ'] * length
        self.must_contain = [] * length
        self.candidate_words = [word for word in sowpods if (len(word) == length)]
        print(len(self.candidate_words))

    def __len__(self):
        return self.length

    def get_regex(self):
        regex_string = ""
        for letter in self.must_contain:
            regex_string += "(?=\\w*" + letter + ")"
        for position in self.might_contain:
            regex_string += "[{}]".format(position)
        regex_string = regex_string.strip()
        return regex_string

    def update_candidate_words(self):
        """ update the candidate word list based on the candidate letters for each position """
        regex_string = self.get_regex()
        print(regex_string)
        regex_matcher = re.compile(regex_string)
        self.candidate_words = [w for w in self.candidate_words if regex_matcher.match(w)]
        print(len(self.candidate_words))

    def prune_candidate_letters(self):
        """uses the word list to prune the list of candidate letters based on valid english words"""
        self.update_candidate_words()
        candidate_letters = []
        for i in range(self.length):
            letter_intersection = set()
            for word in self.candidate_words:
                letter_intersection.add(word[i])
            position_candidates = ""
            for l in letter_intersection:
                position_candidates += l
            candidate_letters.append(position_candidates)
        self.might_contain = candidate_letters

    def remove_from_all(self, letter):
        """ remove the given letter from all positions in the word """
        for i in range(self.length):
            self.might_contain[i] = self.might_contain[i].replace(letter, "")

    def remove_from_one(self, letter, position):
        """ remove the given letter from a specific position in the word """
        self.might_contain[position] = self.might_contain[position].replace(letter, "")

    def confirm_letter(self, letter, position):
        """ make this letter the only candidate for the given position """
        self.might_contain[position] = letter



class PhrazleSolver:

    def __init__(self, word_lengths):
        """
        :param word_lengths: tuple of word lengths in phrase
        """
        sowpods = []
        with open("sowpods.txt", "r") as sowpods_txt:
            for line in sowpods_txt.readlines():
                sowpods.append(line.rstrip())

        self.phrase = [Word(l, sowpods) for l in word_lengths]

    def remove_from_all_words(self, letter):
        for word in self.phrase:
            word.remove_from_all(letter)

    def remove_from_one_word(self, word, letter):
        self.phrase[word].remove_from_all(letter)

    def remove_from_one_position(self, word, position, letter):
        self.phrase[word].remove_from_one(letter, position)

    def confirm_letter(self, word, position, letter):
        self.phrase[word].confirm_letter(letter, position)

    def update_candidates(self):
        for word in self.phrase:
            word.prune_candidate_letters()

    def get_phrase_regex(self):
        regex_string = ""
        for word in self.phrase:
            regex_string += word.get_regex() + " "
        return regex_string.rstrip()

    def get_candidates(self, n=3):
        candidates = [[word.candidate_words[i] for i in range(min(n, len(word.candidate_words)))] for word in self.phrase]
        return candidates

if __name__ == "__main__":
    word_lengths = (4, 5)
    p = PhrazleSolver(word_lengths)
    p.update_candidates()
    print(p.get_phrase_regex())
    print(p.get_candidates())

    # AAHS AALII
    p.remove_from_one_word(0, 'A')
    p.remove_from_all_words('H')
    p.remove_from_all_words('L')
    p.remove_from_one_word(0, 'I')
    p.remove_from_one_word(0, 'S')
    p.remove_from_one_position(1, 0, 'A')
    p.remove_from_one_position(1, 1, 'A')
    p.update_candidates()
    print(p.get_phrase_regex())
    print(p.get_candidates())

    # BECK BEADS
    p.remove_from_all_words('B')
    p.remove_from_all_words('K')
    p.remove_from_one_position(0, 1, 'E')
    p.confirm_letter(0, 2, 'C')
    p.remove_from_one_position(1, 2, 'A')
    p.remove_from_all_words('D')
    p.remove_from_one_position(1, 4, 'S')
    p.update_candidates()
    print(p.get_phrase_regex())
    print(p.get_candidates())
