# This program uses Python 3.7 and calculates the score for a game of bowling. It assumes that the game is valid, there
# are 10 frames and no scores per frame are > 10. In the problem statement it states that the input will be an integer
# array however for a strike there would be a X and for a spare there would be a /. To accommodate this the program
# checks if the frame is a X, an integer or if / is present in the frame and calculates the score accordingly. After it
# calculates the score it will print the frames and the final score.
import sys
import json

class CalculateScore:
    frames = []
    finalScore = 0

    def __init__(self, frames):
        self.frames = frames
        self.finalScore = self.calculate_score(self.frames)

    def get_final_score(self):
        return self.finalScore

    @staticmethod
    def frame_score(frame, curr_frame_num):
        score = 0

        # Calculate score if we are not in the last frame.
        if curr_frame_num != 9:
            # If the current frame is a strike add 10 points to the score + the points for the next 2 throws.
            if frame == 'X':
                score = score + 10
            # Check if the current frame is an integer. If it is we know there was not a strike or spare so add up
            # the number of pins for each throw and add that to the score.
            elif isinstance(frame, int):
                curr_frame = [int(throw) for throw in str(frame)]
                for throw in curr_frame:
                    score = score + throw
            # If there is a / in the frame then this frame was a spare. Add the number of pins downed on the first
            # throw to the score and the points for the next throw.
            elif '/' in frame:
                score = score + 10
        # Calculate score for the last frame.
        else:
            # If the lat frame is all strikes add 30 to the score.
            if frame == 'XXX':
                score = score + 30
            # Check if the last frame is an integer. If it is we know there was not a strike or spare so add up
            # the number of pins for each throw and add that to the score.
            elif isinstance(frame, int):
                last_frame = [int(throw) for throw in str(frame)]
                for throw in last_frame:
                    score = score + throw
            # If there is a / in the last frame then there was a spare. Add the number of pins downed on the first
            # throw to the score and 10 points for the spare.
            elif '/' in frame:
                score = score + 10
            # If the first throw on the last frame was a spare there will be two bonus throws. Add 10 points for the
            # strike and the number of pins downed on the two bonus throws.
            elif 'X' in frame:
                frame_score = 0
                for throw in frame:
                    if throw == 'X':
                        frame_score = frame_score + 10
                    else:
                        frame_score = frame_score + int(throw)
                score = score + frame_score
        return score

    def calculate_score(self, frames):
        n = len(frames)
        perfect_game = 0
        spare_game = 0
        frame_scores = []
        i = 0
        j = 0

        # We know that a perfect score is 300 and a all spare game is 150 so check for those first.
        for frame in frames:
            if frame == 'X' and j < 9:
                perfect_game = perfect_game + 1
            elif not isinstance(frame, int) and '/' in frame:
                spare_game = spare_game + 1
            else:
                if frame == 'XXX':
                    perfect_game = perfect_game + 1
                elif not isinstance(frame, int) and '/' in frame:
                    spare_game = spare_game + 1
            j = j+1

        # If it is a perfect game score = 300
        if perfect_game == 10:
            return 300

        # If it is a all spare game score = 150
        if spare_game == 10:
            return 150

        # Loop through the frames.
        while i < n:
            # Calculate the individual frame score.
            frame_score = 0
            if i < 9:
                # If the current frame is a strike add 10 points and the next frames score.
                if frames[i] == 'X' and i < 9:
                    frame_score = frame_score + 10 + self.frame_score(frames[i+1], i+1)
                # If the frame is not a strike or score add the number of pines down for both throws.
                elif isinstance(frames[i], int):
                    frame_score = frame_score + self.frame_score(frames[i], i)
                # If the current frame is a spare add 10 points and the number of pins down for the first throw of the
                # next frame.
                elif '/' in frames[1] and i < 8:
                    frame_score = frame_score + 10
                    if frames[i+1] != 'X' and isinstance(frames[i+1], int):
                        extra_pts = [int(throw) for throw in str(frames[i+1])]
                        frame_score = frame_score + extra_pts[0]
                    else:
                        if '/' in frames[i+1][1]:
                            extra_pts = int(frames[i+1][0])
                            frame_score = frame_score + extra_pts
            # Calculate the score for the last frame.
            else:
                frame_score = frame_score + self.frame_score(frames[i], i)
            frame_scores.append(frame_score)
            i = i+1

        # Sum up all the individual frames scores and return the final score.
        return sum(frame_scores)


# Program will expect 10 'frames' entered as numbers of 'X' for a strike or '5/' for a spare (doesn't have to be 5)
def main():
    frames = []
    for frame in sys.argv[1:]:
        if isinstance(frame, str) and 'X' not in frame and '/' not in frame:
            frames.append(int(frame))
        elif 'X' or '/' in frame:
            frames.append(frame)

    game = CalculateScore(frames)
    print(frames)
    print("Game Score: " + str(game.get_final_score()))
    print()


if __name__ == "__main__":
    main()

# Score = 300
frames1 = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'XXX']
game1 = CalculateScore(frames1)
print(frames1)
print("Game 1 Score: " + str(game1.get_final_score()))
print()

Score = 90
frames2 = [45, 54, 36, 27, 9, 63, 81, 18, 90, 72]
game2 = CalculateScore(frames2)
print(frames2)
print("Game 2 Score: " + str(game2.get_final_score()))
print()

# Score = 150
frames3 = ['5/', '5/', '5/', '5/', '5/', '5/', '5/', '5/', '5/', '5/']
game3 = CalculateScore(frames3)
print(frames3)
print("Game 3 Score: " + str(game3.get_final_score()))
print()

# Score = 114
frames4 = ['5/', '5/', 27, '5/', 9, '5/', 50, '5/', 00, 'X55']
game4 = CalculateScore(frames4)
print(frames4)
print("Game 4 Score: " + str(game4.get_final_score()))
print()

# Score = 103
frames5 = ['5/', '5/', 27, 'X', 9, 'X', 50, '5/', 00, 63]
game5 = CalculateScore(frames5)
print(frames5)
print("Game 5 Score: " + str(game5.get_final_score()))
print()

# Score = 0
frames6 = [00, 00, 00, 00, 00, 00, 00, 00, 00, 0]
game6 = CalculateScore(frames6)
print(frames6)
print("Game 6 Score: " + str(game6.get_final_score()))
print()
