---
title: Code got cheaper. Understanding did not.
date: 2026-09-03
series: AI
description: Agents are getting better at checking their own work. That is good, and it is not the thing I was worried about. I read the code to stay in the conversation, not to approve it.
---

The moment that started this was not a failure. It was the opposite, which is why it stuck.

I was testing an agentic setup, and it went off and did a long, high-effort research pass, and came back having enabled a handful of things I did not know existed. Not wrong things. Good things. It had found capabilities in a system I thought I knew, and it was right about all of them.

And my reaction, sitting there looking at a working result, was: *hang on, how does any of this actually work?*

That is the whole essay, really. Not "the agent broke something." The agent did fine. I was the one who had quietly stopped following.

## Numbers

Let me put a number on it, because the number is what made this concrete for me.

One recent stretch of work: 372 files touched. Around fifty-five thousand lines added, three thousand removed. One human.

I could review that. Reviewing is a sampling exercise and always has been. I could open the important files, check the dangerous paths, run the tests, read the diff on anything touching money or auth, and sign off with a reasonably clear conscience.

But reviewing it and understanding it are not the same activity, and I had been letting myself pretend they were.

## Verification

Here is the argument against worrying about this, and it is a strong one, so I want to state it properly rather than knock over a strawman.

Agents are getting measurably better at checking their own work. They write the test, run it, watch it fail, fix it, run it again. They catch their own type errors before I see them. Give one a second agent as a reviewer and the pair catches things I would have missed on a tired Friday. This is genuinely good and I have no interest in pretending otherwise. I like it when my agent does not make mistakes.

And the second half of the argument is even harder to answer: you do not read every line of every library you import. Nobody does. You trust the interface, the tests, and the blast radius. Software has always run on layers of things we use without understanding, and it has mostly worked out.

So if verification keeps improving, and we already accept opacity everywhere else, what exactly am I complaining about?

## Participation

This is the turn, and it took me a while to find the words for it.

Verification was never the thing I was worried about. The question is not "can I confirm this is correct." The question is: **can I still take part in what happens next?**

Because a project is not one loop. You do not describe a feature, receive a feature, and walk away. You go around dozens of times. Build it, look at it, notice it is wrong in a way nobody could have predicted from the spec, change your mind about the shape, go again. The interesting work lives in the going again.

And the thing that generates the next loop is not the agent. It is whatever model of the system you are carrying in your head. Ideas come from having enough concepts loaded to feel that two of them rub against each other. If your mental model of the system is thin, you can still ask for changes, but they will be small and obvious ones, because small and obvious is all a thin model can see.

That is the loss. Not correctness. Imagination.

![A project drawn as a run of repeated loops along a line, each one starting from what you understand about the system](/assets/img/posts/code-got-cheaper-understanding-did-not/loops.png)

You can be handed a perfectly correct system and still be unable to say anything interesting about where it should go. And the worst part is that this failure is invisible. Nothing breaks. No test goes red. You just slowly become a person who approves things.

## Debt

The closest analogy I have is technical debt, and I think it is closer than an analogy usually gets.

Technical debt works because you can absolutely get away with it in the short term. The shortcut ships. The feature works. You bank the speed now and the interest is charged much later, at a time you do not choose, usually when you are least equipped to pay it.

Not understanding your own system behaves exactly the same way. In the short run it costs nothing. The code is correct. The reviews pass. You look fast. Then some incident happens at an inconvenient hour, or somebody asks why the thing was built this way, or you need to make a change that requires knowing which assumptions are load-bearing, and the bill arrives with interest.

The difference is that you can point at technical debt. It is in the repo. This other kind sits in your head, or rather it does not sit anywhere, which is the problem.

## Reading

So I added a step, and it is the only part of my workflow I am dogmatic about.

Before anything gets sent, I make the change explain itself to me. Not the diff. A diff is a format built for a version control system, not for a person trying to learn something. It is ordered by file path, which is a fine way to store a change and a terrible way to teach one.

Instead: why this change exists, before a single line of code. Then the shape of the solution in one paragraph. Then the code in the order a person would learn it, which is almost never the order the files are in. Then five questions about it that I answer without asking the agent.

That last part is not a habit I rely on remembering. It is [a skill I run](https://github.com/ameeer-in/agent-skills/blob/main/skills/explain-diff/explain-diff-html.md), and it writes the whole thing out as one page with the quiz as actual multiple choice at the bottom, so I cannot quietly award myself a pass on questions I only half know.

If I cannot answer them, I am not done reading. That is the whole rule and it is not negotiable, mostly because I have already caught myself trying to negotiate with it.

I am not doing this to give a final thumbs up. I am doing it so I can take part in the next decision.

## Bias

I should say plainly where I am standing, because it tints all of this.

I love this stuff. I find it genuinely fun to point a fleet of agents at something big and watch it come together properly, and I learn more in a week now than I used to in a month. I am not a sceptic writing a cautionary piece. I am an enthusiast who noticed something and cannot un-notice it.

Which means I am exactly the person most likely to rationalise. Maybe the understanding step is a comfort ritual. Maybe in three years the tools will be good enough that insisting on it will look like a mainframe operator refusing to trust a compiler, and my grandchildren will find this post very funny.

I do not think so. But I notice that I want it to be true, and wanting it to be true is not evidence.

What I am more confident about is the direction. Producing code is getting cheaper every few months and shows no sign of stopping. The effort required to genuinely understand a system has not moved at all, because it is bounded by human attention, and human attention is the one input in this whole industry that has never once gotten cheaper.

That gap is widening. It is going to keep widening. Everything I do differently now is a response to it.

Code got cheaper. Understanding did not. Only one of those is my job.
