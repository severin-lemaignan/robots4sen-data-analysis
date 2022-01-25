import re
from glob import glob
import os.path
import sys

raw_notes = []
notes = []

coding = {
    "M": "Mood modulation/reflection",
    "P": "Unstructured/playful",
    "S": "Social (e.g. treating Pepper as a social entity)",
    "G": "Group interactions (with other students and/or staff)",
    "H": "Hidden interactions (e.g. watching Pepper from a distance)",
    "C": "Comments about Pepper (e.g. things they liked/disliked about Pepper, interpretations of the robot's behaviour)",
    "T": "Touch (e.g. holding Pepper's hand, moving Pepper, stroking Pepper's head, hugs, does NOT include touching the interface)",
    "Q": "Questions",
    "D": "Things that affecting the data collection (e.g. media days, testing/demonstrating things, robot errors, non-responsive interface)",
    "U": "Unclassfied, doesn't fit in any other category, but still interesting/useful",
}
students = {
    "F": "Student F",
    "L": "Student L",
    "J": "Student J",
    "X": "Student X",
    "N": "Student M",
}


days = [
    "15.06",
    "16.06",
    "17.06",
    "18.06",
    "21.06",
    "22.06",
    "23.06",
    "24.06",
    "25.06",
    "29.06",
    "30.06",
    "01.07",
    "02.07",
]
logs = {}
for day in days:
    d, m = day.split(".")
    logs[day] = [
        os.path.basename(f) for f in sorted(glob("../logs-*-%s-%s/notes/*" % (m, d)))
    ]


def to_id(label):
    return (
        label.replace(" ", "-")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "")
        .replace(",", "")
        .replace("'", "")
        .lower()
    )


class Note:
    note_id = 0

    def __init__(self, raw):

        raw = raw.strip()
        self.date = raw[0:5]
        self.day_id = int(raw[6:8])
        self.id = Note.note_id
        Note.note_id += 1
        head, tail = raw.split(" ", 1)
        self.code = head[9:]
        self.text = tail

        self.log = (
            logs[self.date][self.day_id]
            if self.day_id < len(logs[self.date])
            else "written note"
        )

    def __str__(self):
        # return "- **#%s** (%s/%s) [%s]:\n\n%s\n\n``%s``\n\n" % (self.id, self.date, self.day_id, self.code, self.text,self.log)
        return "- **Note %s** (%s, note #%s that day): %s\n\n" % (
            self.id,
            self.date,
            self.day_id,
            self.text,
        )


with open("raw_note_transcripts", "r") as f:
    raw_notes = f.readlines()


for l in raw_notes:

    l = l.strip()
    if re.match("\d\d.\d\d-\d\d", l):
        notes.append(Note(l))

# date = ""
# for n in notes:
#    if n.date != date:
#        print("## " + n.date)
#        date = n.date
#    print(n)
# sys.exit(0)

print("# Transcript of notes (after coding)\n")

print(
    """

## Table of Contents

- [Overview](#overview)
- [Notes ordered by construct](#constructs)"""
)

for c in coding:
    print("  - [%s](#%s)" % (coding[c], to_id(coding[c])))

print("- [Notes ordered by specific children](#specific-students)")

for s in students:
    print("  - [%s](#%s)" % (students[s], to_id(students[s])))

print("- [Other notes](#non-coded-notes)")

print(
    """

## Overview

"""
)

print("Total: %s notes over 13 days\n" % len(notes))


for c in coding:

    count = 0
    for n in notes:
        if c in n.code:
            count += 1

    print("- %s: %s notes\n" % (coding[c], count))

print("\n## Constructs\n")

for c in coding:
    print("\n### %s\n" % coding[c])

    for n in notes:
        if c in n.code:
            print(n)

print("\n## Specific students \n")

for s in students:
    print("\n### %s\n" % students[s])

    for n in notes:
        if s in n.code:
            print(n)


print("\n## Non-coded notes \n")


for n in notes:
    if not n.code:
        print(n)
