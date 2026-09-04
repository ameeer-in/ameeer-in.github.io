---
title: The workflow I built to ship with a herd of AI agents
date: 2026-08-24
series: AI
description: How I stopped using one AI assistant for everything and started running several with separate jobs, separate context, and a guardrail that once refused my own instruction.
---

Most advice about running AI agents is about getting consistent output. Pin the model, fix the prompt, lower the temperature, make the thing repeatable.

I have gone the other way. I run three harnesses that routinely contradict each other, and I have stopped trying to fix it.

Consistency is what you want from a build system. It is not what you want from a reviewer.

It usually looks like two panes side by side. Same repo, same branch, same question. One agent says the change is safe to ship. The other says it is not, and gives a reason specific enough that I have to go and look.

For a long time I thought my job in that moment was to work out which one was wrong. It is not. Two harnesses can arrive with different models, system instructions, context, tools and blind spots. When they split on the same diff, I treat it as evidence that something in the change deserves a closer look, not proof that one of them has found the truth. Treating the second opinion as a stress test rather than a tie to break changed the shape of everything else.

Here is the rest of it: where the agents run, the guardrails around them, and how a vague ticket turns into code I am willing to send.

## Roles, not rankings

The single biggest change was giving up on one assistant that does everything.

One long chat that plans, writes, reviews and explains is the slowest arrangement I have used. Every new task inherits the last one's confusion, and the model that just spent an hour convincing itself an approach works is the worst possible reviewer of it.

So I split the work into seats:

- **Explore:** one agent reads the ground truth and reports back. It writes nothing.
- **Challenge:** one agent attacks the plan while changing it is still cheap.
- **Implement:** one agent per slice, each with its own clean context.
- **Review:** a different harness reads the result cold, with no memory of writing it.
- **Understand:** me. That seat does not get delegated, and it is what the next post is about.

Note the fourth one. A reviewer that also wrote the code is proofreading its own homework. Using a separate harness is not about which one is smarter, it is about which one has no stake in the answer.

I do not have a favourite. Strong reasoning models take the calls that are hard to reverse. Cheaper, faster ones do the bounded work where the spec is already written down. That routing changes every few months, so I have stopped treating it as a ranking.

![One agent holding every job in a single context, next to five separate seats each starting clean](/assets/img/posts/workflow-herd-of-agents/seats.png)

## Where it all runs

The terminal is just the window. I use one that is fast enough that I stop noticing it, which is the highest compliment a terminal can get.

The workspace is where the idea lives. I use [Herdr](https://herdr.dev/), an agent-aware multiplexer. Every agent runs in a **real pane**, not a hidden background job, so working, blocked and done are visible at a glance and I can step into any pane and take over mid-task.

![My Herdr window: spaces on the left, the agent list beneath them, and a Codex pane open on the right](/assets/img/posts/workflow-herd-of-agents/herdr-spaces.png)

That is a real window. Spaces run down the left, one per context I am holding, and underneath is every agent with its state and its harness, Claude and Codex and Cursor in one list. Nothing is hidden, which is the whole reason I use it.

The part I did not expect to care about: detach once and the agents keep running. I close the laptop, reattach later, and the work is where I left it.

## Two hooks with opposite jobs

I want speed. I also want the terminal to disagree with me sometimes.

So there are two hooks doing opposite jobs. One auto-approves read-only commands so I never confirm `git status` again. The other blocks a short list of patterns before they run: deleting a home directory, piping a URL straight into a shell, force-pushing to master, hard-resetting uncommitted work.

The blocking one earned its place while I was building a talk about this setup. I asked an agent to write the slide describing the dangerous patterns, and the hook refused, because the slide text contained the patterns it is trained to stop.

The guardrail blocked the slide about the guardrail. I sat there mildly annoyed for a second, then realised it had just given me my best demo.

Both are in [this repo](https://github.com/ameeer-in/agent-skills). Read them before you let anything decide what runs on your machine.

## Context is a budget

Two settings do most of the work:

```sh
CLAUDE_CODE_DISABLE_1M_CONTEXT=1
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70
```

One caps the window, the other compacts earlier than the default. Both are deliberate limits on something I could have more of, which sounds backwards until you watch a long session degrade. A long window carries history the current task does not need, and attention thins out before the answers visibly do. You notice late. Compacting at seventy percent makes the boundary between tasks a decision I made, rather than an accident that happens at the worst possible moment.

## One map every agent reads

Without a shared map, every agent invents its own.

I keep one folder holding every repo I touch, with a `CLAUDE.md` at the root carrying repo ownership, branch strategy, release order and review discipline. `AGENTS.md` sits beside it and points at the same file, so the other harnesses read identical rules instead of a slowly diverging copy.

There is also a sync script that fetches everything, skips dirty repos, rebases what should be rebased, and leaves me on the branch I asked for. My first agent is a shell script. It has no opinions, only exit codes.

## From ambiguity to a contract

A ticket is ambiguity. A plan is a contract. Most of the value here lives in the gap between those two sentences.

Three steps, in order. The first interrogates the idea one question at a time until every decision is explicit, and it is very good at finding the uncomfortable question I was avoiding. The second turns that into a written contract: problem, solution, stories, decisions, tests, and an explicit scope boundary. The third cuts it into vertical slices, each declaring what blocks it.

It all lands in one folder per ticket, which becomes the shared index for everything that follows.

## When a method repeats, write it down

I was losing product context. Not the code, the reasoning behind it. Why a thing was built that way, what the customer actually wanted, which failure modes had already been ruled out in a meeting eight months ago.

So when a method repeats, I stop remembering it and write it down as a skill: a small folder of instructions an agent loads on demand. One holds the product model. One turns a class of failure into an evidence trail. One walks a feature from the UI down to storage.

The rule that stops it becoming a swamp: durable knowledge becomes a skill, ticket-specific facts stay in the plan folder. A skill is not magic. It is a checklist that stops me rediscovering the same thing twice.

The generic ones are in the [same repo](https://github.com/ameeer-in/agent-skills) as the hooks. Point your own agent at it and ask it to install them, which is a decent test of whether you trust it yet.

## Draw it, then swarm it

If I cannot draw the change, I do not understand the change. So before implementation starts, the plan becomes a diagram. Missing edges and unclear ownership show up immediately when you try to draw them, and arguing with a picture is much cheaper than arguing with a pull request.

Then the fleet: one agent per slice, each with a bounded context, all reading the same plan folder. Which creates the obvious problem. If the work is spread across panes, the state has to live somewhere outside my head, or I become the bottleneck everything queues behind.

The fix turned out to be boring. The agents never talk to each other. They read and write the same few markdown files, and keeping those current is part of the job I give them. A plan file holds the contract. A pull request file tracks where each repo has got to, polled by a cheap agent that updates only what it can verify. A changelog is appended as the work happens rather than reconstructed at the end.

You can just ask for this. There is no framework, only a folder with some markdown in it, which is precisely why the next agent can pick it up mid-flight without me explaining anything.

## Two reviewers, because they fail differently

I run two code reviews, and the point is that they are bad at different things.

- **The merge gate:** two git refs, one exhaustive pass over the branch diff, high-confidence findings only. Quiet and selective, so when it speaks I listen.
- **The local pass:** a dirty workspace, a commit or a range, before anything is pushed. Path-specific rules per language, file by file. Broad, noisy, occasionally wrong.

The second one is my local emulation of Alibaba's [OpenCodeReview](https://github.com/alibaba/open-code-review), running their prompts and rules through my own tools.

Neither alone is enough. The selective one misses what it was not confident about. The broad one buries a real finding under four cosmetic ones. Running both is the same trick as the two disagreeing agents at the top of this post, applied at the end instead of the beginning.

## What I am not sure about

Whether any of this survives the year.

The tools shift under me constantly. A harness ships something that makes one of my careful workarounds pointless. A model gets better at what I built scaffolding to compensate for. I have already thrown away pieces of this that were load-bearing three months ago.

That is fine, and honestly it is most of the fun. Picking up a big feature and watching it come together through a process that is actually mature, while learning something new in the middle of doing it, is a good way to spend a week. The commands here will age badly. The habits underneath them, separate the context, specialise the agent, capture the process, review the result, are what I would carry to whatever replaces all of this.

Which leaves the thing I think about most. All of this produces code faster than I can read it. One recent stretch touched hundreds of files and added tens of thousands of lines.

I can review that. I am not sure I can understand it. That is the next post.

## References

- [Herdr](https://herdr.dev/), the agent-aware terminal multiplexer the panes run in
- [Ghostty](https://ghostty.org/docs/about), the terminal emulator
- [Archify](https://github.com/tt-a1i/archify), for turning a plan into an architecture diagram
- [OpenCodeReview](https://github.com/alibaba/open-code-review) by Alibaba, the basis for the local review pass
- [The hooks and skills from this post](https://github.com/ameeer-in/agent-skills), if you want to steal any of them
