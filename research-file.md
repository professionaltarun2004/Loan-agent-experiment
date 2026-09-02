# Loan Document Agent — Research File

## 1. Problem Statement

A loan applicant provides a bank statement as supporting evidence. The agent observes the applicant's transaction history and patterns over time, but it cannot directly observe the actual context behind those transactions.

The agent must decide whether the available evidence is sufficient to accept the case, whether additional evidence should be requested, or whether the case should be sent to a human when the uncertainty cannot be resolved sufficiently.

The agent should be able to update its assessment when new evidence is received rather than making a decision from a single observation.

## 2. Project Objective

To design and test an agent that can make decisions when the available loan-document evidence is incomplete. The agent should determine when the current evidence is sufficient, when it is worth requesting additional evidence, and when the remaining uncertainty should be handled by a human.

## 3. Technical Terms

### 3.1 Partial Observability

The agent can observe the bank statement and transaction patterns, but it cannot directly observe the actual context behind those transactions. Therefore, the information available to the agent does not completely describe the underlying situation.

### 3.2 Hidden / Latent State

The hidden state is the underlying context that cannot be directly observed from the bank statement, such as the actual reason behind an observed transaction pattern.

### 3.3 Belief State

The agent maintains an assessment of what may be happening based on the evidence it has observed so far. When new evidence arrives, this assessment can be updated.

### 3.4 Active Information Gathering

The agent can actively request additional evidence when the information currently available is insufficient to make a decision.

### 3.5 Human-in-the-Loop / Learning to Defer

The agent can defer a case to a human when the available evidence remains insufficient or the uncertainty is too high for the agent to make the decision safely.

### 3.6 POMDP (Partially Observable Markov Decision Process)

A possible formal framework for modelling sequential decision-making when the underlying state is not directly observable. It is relevant to investigate because our agent observes evidence, maintains uncertainty, takes actions, and can receive new evidence.

### 3.7 Value of Information

A concept for evaluating whether obtaining additional information is worth its cost. In this problem, requesting another piece of evidence may reduce uncertainty, but it also creates time, effort, and processing costs.

## 4. Search Queries

1. "bank transaction data credit risk assessment"

2. "bank statement transaction patterns credit scoring"

3. "POMDP credit decision making partial observability"

4. "active information gathering additional evidence decision making"

5. "value of information additional evidence decision making"

6. "learning to defer human in the loop high stakes decision making"

7. "selective prediction reject option uncertainty decision making"

## 5. Reddit Communities

### r/mlscaling

Status: Posted and awaiting responses.

My question:
I am building a loan document agent that observes bank statements
and needs to decide whether to proceed, request more evidence, or
send a case for human review. I asked how judgement criteria can be
incorporated into such an agent, particularly how it should decide
when to stop gathering evidence and defer to a human, and what
additional context a human could assess that the agent cannot.

## 6. Relevant X Accounts

To be researched and verified.

## 7. Papers / Articles / Repositories / Datasets

To be researched and verified.

## 8. Questions I Want to Answer

To be developed from the research.

## 9. AI Prompts Used

### Initial Research Prompt

I am a beginner. I want to design an AI agent for this problem:

The agent observes a loan applicant's bank statement and transaction patterns over time. It must decide whether to accept the available evidence, request additional evidence, or send the case to a human because the actual context behind the observed transaction patterns is not completely known.

The agent must make decisions when information is not complete.

Help me prepare my research.

1. Give me the technical terms for this problem.
2. Give me useful search queries.
3. Find 5 to 10 relevant Reddit communities.
4. Tell me why each community is relevant.
5. Find relevant researchers and engineers on X.
6. Give me questions about hidden states, evidence, actions, and errors.
7. Identify each claim that needs a source or a test.
8. Tell me which parts of my problem are not clear.

Do not present uncertain information as fact.

### Initial Design Insight

The agent should not send every uncertain case directly to a human.
When uncertainty exists, it should first consider whether a specific
piece of additional evidence could meaningfully reduce the relevant
uncertainty at a reasonable cost.

If useful additional evidence is unavailable, too costly, or unlikely
to resolve the uncertainty, the agent should be able to defer the case
to a human.

This is an initial design hypothesis that will need to be tested.

## 10. Important AI Errors

To be recorded as the research is verified.

One issue already identified: some AI responses expanded the problem into full loan approval/rejection. The selected Week 1 problem is narrower: accept the available evidence, request additional evidence, or send the case to a human.

## Initial Agent Policy Hypothesis

The agent should not make a decision based only on which outcome is
most likely.

It should consider:
- its current belief about the possible hidden states,
- the remaining uncertainty,
- whether useful additional evidence is available,
- the cost of obtaining that evidence,
- and the cost of being wrong.

The agent can then choose between:
1. Accepting the available evidence and proceeding,
2. Requesting additional evidence, or
3. Deferring to a human.

Human review is treated as an intentional action when the remaining
uncertainty and potential cost of an incorrect decision make further
automated decision-making inappropriate.

This is an initial policy hypothesis and will be tested using synthetic
cases before being treated as a final design.