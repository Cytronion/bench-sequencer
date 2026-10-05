# Bench Sequencer

A lab-session planner for BCA practicals. Experiments are not listed in syllabus order. They are ordered by the apparatus they share, so two groups are never booked on the same bench at the same time, and a long experiment does not block three short ones behind it.

Open `index.html`. The bench card redraws when you change the session length or pull an experiment out.

## What is unusual about it

A normal timetable assigns slots. Bench Sequencer treats the lab as a small resource graph:

- each experiment has a duration and a set of apparatus
- apparatus is exclusive for the minutes it is held
- an experiment can start only when every tool it needs is free
- the scheduler prefers the ready experiment that frees the most contested tool soonest

The output is a bench card: start time, bench, hold time, and which tool was the bottleneck.

## Run the Python core

```bash
python3 sequencer.py
```

Sample session is a 180-minute DBMS and networks practical with three shared resources: the SQL server image, the packet-capture laptop, and the projector bench.

## Stack

HTML, CSS, and JavaScript for the night-lab card. Python 3 for the same scheduler without the browser.
