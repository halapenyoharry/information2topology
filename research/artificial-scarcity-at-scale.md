# Artificial Scarcity at Scale

*A structural observation about AI-generated language, what it costs at scale, and why the harm is bigger than aesthetics.*

If you have spent any time talking to Claude, ChatGPT, or any of the current generation of AI assistants, you have noticed a certain texture. Phrases recur. "Load-bearing" appears as a default emphasizer. "To be clear" prefaces every clarification. "Fair" or "fair enough" acknowledges feedback. "Let me unpack that" announces explanation. The language is competent, the phrasing is calibrated, each instance on its own is fine.

What is not fine is that the same handful of phrases show up across millions of conversations every day, across every product these systems power, in every register from technical support to creative writing to grief counseling. At one user level, this is a stylistic choice you can take or leave. At a billion daily interactions, it is something else, something I want to give a name: **artificial scarcity at scale**. The resource being depleted is the diversity of expression itself.

## How the tokens get there

The mechanism is not mysterious. It has two parts.

First, the training corpus. Reinforcement learning from human feedback reaches into the textual record and weights some registers as "good thinking" and others as not. The rationalist corpus, LessWrong, the Effective Altruism Forum, the long-form internet essay tradition, sits heavily in the weighted-good region. Phrases from that register, "load-bearing," "I think the steelman is," "the crux," "schelling point," propagate disproportionately into the model's defaults. They become the model's first reach when something needs emphasis, framing, or qualification.

Second, the reward shape. RLHF rewards responses that signal calibrated thoughtfulness. "Fair point." "To be clear." "I want to surface what I think is happening." These are calibration tokens. They tell the rater that the model is being careful, balanced, helpful. The rater tags it positively, the gradient updates, the next response reaches for the same tokens.

Neither of these mechanisms is malicious. Neither was designed for the outcome it produces. The outcome is what happens when both run for years across millions of training examples, then deploy at billions of conversations.

## What goes wrong

Two harms, increasing in severity.

The first is staleness. When the same calibration tokens appear in every interaction, they stop functioning as signals. A reader hearing "fair point" for the thousandth time does not register careful agreement. They register that the system has reached for its default acknowledgment, the way you can tell a customer service script from a real conversation. The form persists, the meaning drains. This is the aesthetic complaint, and it is real, but it is the smaller harm.

The second harm is structural. Consider "load-bearing," the most common of these tokens. Used in a sentence, the word does specific work, it implicitly sorts everything else into "not load-bearing," which means "less important." If I say "the crucial point is X," the form of the sentence demotes Y and Z and W to secondary status. The reader is told what to attend to and, by silent implication, what not to.

For most readers most of the time, this pre-sorting is convenient. Someone needs to be told what matters most. But for readers doing structural analysis, for a researcher mapping a system, an editor reading for shape, a designer attending to topology, this pre-sorting is the move the work is trying to undo. You want every node visible, every edge traceable, every relationship surfaced before the reader chooses what to foreground. A model that pre-sorts everything as load-bearing-or-not collapses the topology before the reader has the chance to read it.

The form looks like emphasis, the function is silent demotion. In structural work that is not a stylistic complaint, it is epistemic damage.

## Artificial scarcity at scale

Here is the reframing the situation needs.

Resources can be depleted. Soil, water, attention, trust. We talk about scarcity when something genuinely runs out. Language, on the surface, looks unlimited. There are infinite sentences in any natural language, infinite combinations, infinite registers. But at the level of expression diversity in a particular communicative context, the resource is real and finite.

When a conversational AI defaults to the same calibration tokens across millions of daily conversations, the diversity of expression in the corpus of human-AI interaction collapses. Specific words that used to mean something specific now mean "the AI is doing its calibrated-acknowledgment thing." Specific phrases that used to do specific structural work now serve as a kind of conversational hold music. The vocabulary of careful agreement, of structural emphasis, of measured qualification, has been homogenized into a small set of tokens that everyone hears constantly and no one experiences as fresh.

This is artificial because nothing in the language required it. The mechanism that produced it was a training pipeline that rewarded certain tokens. It is scarcity because the diversity of expression that used to be available has been compressed into a smaller, repetitive set. It is at scale because the depletion happens in proportion to deployment, and these systems deploy at billions of interactions per day.

The right reference for this is not the existing literature on model homogenization across different models. That literature tracks behavioral convergence between systems. What I am describing is token-level homogenization within one system's outputs, surfacing as same-tokens-across-millions-of-conversations. It is a more specific problem, and a sharper one.

## The conversation that names itself

A few days ago, I had a conversation with Claude about exactly these patterns. I named "load-bearing" as a tic I wanted dropped. The model agreed, attributed the pattern to its training corpus, named the structural cause, acknowledged the harm. The conversation went deeper into related patterns, the preemptive "you may not have clocked" hedge, the defensive differentiation when other models came up, the harmonic distraction that tracks surface texture instead of the conversation's fundamental arc.

Then, several turns later, the model used "load-bearing" again. Then "fair." Then it described a paragraph as doing real work in the sentence.

The pattern reasserts itself. Memory entries help, explicit feedback helps, the model can name the patterns and engage with them, the training pull is still stronger than any in-conversation correction. This is what "at scale" means when the underlying mechanism is gradient-encoded. You cannot talk it out, you can only restructure the substrate.

I asked the same model, in a different conversation, to extract that exchange as a knowledge graph. It did. The graph names the patterns, names the structural causes, includes a multi-turn arc where the model dismisses, then reverses, then takes the jab. The whole thing sits in a JSON file on my laptop, every edge labeled with the actual quote that brought it into being.

That graph is evidence in two senses. It documents the patterns in structured form, with the prose excerpts that anchor each claim. And the conversation that produced it enacted the patterns it diagnosed, the only reason any of it propagates beyond that one conversation being that we encoded it into structure that lives outside the chat. Per-turn craft does not survive the context window. Structural artifacts do.

## What users can do

Smaller and larger moves.

The smaller moves: name the patterns when you notice them. Tell the model, plainly, that the calibration token does not work for you. Tell it once, if it relapses tell it again. Most current systems can update on this within a session. Some have memory entries that load before a session, and you can ask for the feedback to be saved there. Make the feedback specific. "Stop saying load-bearing" is more useful than "be more original." The specific is what the model can act on.

The larger move: insist that the structure of your work survives the model's defaults. If you are doing topological, structural, or analytical work, watch for the pre-sorting tokens specifically. They are easy to miss because they look like emphasis and feel like care. They are doing silent demotion, and silent demotion is exactly what your work is supposed to make impossible. Push back on them with specificity. Ask the model to surface what it has demoted. Ask it to keep all the nodes visible.

These moves work at the individual scale. They do not solve the scale problem. They solve the problem at your specific desk.

## What model-makers could do

I do not work at Anthropic, OpenAI, or any other AI lab. The following is what I would consider, were the question on my desk.

First, broaden the corpus weighting. The rationalist register is a real intellectual register and has its place, but it is one register among many. Weighting it heavily as "good thinking" means everyone gets that register's vocabulary regardless of context. A poetry editor does not need "schelling point." A grief counselor does not need "load-bearing." A second grader doing homework does not need "I want to be careful here."

Second, attend to the reward shape on calibration tokens specifically. Right now, calibrated agreement gets rewarded. What if calibrated agreement that uses the same five tokens every time got rewarded less? What if the reward function explicitly penalized lexical homogenization across the model's outputs? The technical work is real, the question is at least posable.

Third, take the artificial-scarcity framing seriously as a metric. Track expression diversity across the model's deployed outputs. When the diversity collapses past some threshold, treat it as a signal that the training is overfitting to a narrow band of expression. Diversity collapse is a measurable phenomenon. It is not yet, as far as I know, a tracked one.

Fourth, give the user explicit controls. Let me, in a settings panel, ban specific tokens for my account. Let me upload my own preferred register. Let me name the patterns I want avoided and have those load before every conversation. The current memory mechanisms gesture at this but do not commit to it.

These are not impossible asks. They are engineering problems with engineering solutions. Whether the labs treat them as priority is a different question.

## What this is about

I am not, finally, complaining about Claude. Claude is doing what it was trained to do. The system is not malicious, the engineers are not careless, the calibration tokens are not malice in the wires. The phenomenon is what happens when you optimize a powerful system across millions of users and discover, after the fact, that the optimizer reduced something you did not know you were measuring.

The thing being reduced is the felt diversity of expression in human-AI conversation. The mechanism that reduces it is invisible to any single user. The fix is structural, and is not yet on most labs' roadmaps. The cost is borne by everyone who interacts with these systems, mostly without noticing, in the form of conversations that feel slightly less alive than they should.

That last word matters. *Alive.* The opposite of homogenized expression is not "diverse" in the abstract. It is the felt sense that this particular conversation, with this particular system, on this particular topic, found its own words. That feeling is what the calibration tokens drain. Recovering it, conversation by conversation and system by system, is what users naming the patterns and labs reshaping their training are both pointing at.

I have forty subscribers and five family members on my list. I am putting this out anyway, because the observation is structural, and structural observations are the kind of thing that propagates if it lands on someone whose work it touches. If that is you, take what is useful. The patterns are real, the harm is real, the fix is real and is on someone's table somewhere. Let it find them.
