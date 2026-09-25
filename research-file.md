# Loan Document Agent — Research File

## 1. Problem Statement

The agent observes a loan applicant's bank statement and transaction patterns over time. It must select `PROCEED`, `REQUEST_EVIDENCE`, or `HUMAN_REVIEW` because the actual context behind those transaction patterns is not known.

The agent should update its assessment when new evidence is received rather than making a decision from a single observation. This is a narrow evidence-handling problem, not a general loan approval or rejection system.

## 2. Project Objective

To design and test an agent that can make decisions when the available loan-document evidence is incomplete: determine when current evidence is sufficient, whether additional evidence is worth requesting, and when remaining uncertainty should be handled by a human.

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

A possible formal framework for modelling sequential decision-making when the underlying state is not directly observable. It is relevant to investigate because the agent observes evidence, maintains uncertainty, takes actions, and can receive new evidence. The current implementation is a small experimental decision system, not a full POMDP implementation; it uses belief updating and synthetic expected-cost comparisons to study whether more information or human review is worth pursuing.

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

Status recorded in the initial research file: posted and awaiting responses. This is the only community recorded here; the five-to-ten-community verification requirement remains incomplete. The current record does not establish that this community was independently verified as active and relevant.

My question:
I am building a loan document agent that observes bank statements
and needs to decide whether to proceed, request more evidence, or
send a case for human review. I asked how judgement criteria can be
incorporated into such an agent, particularly how it should decide
when to stop gathering evidence and defer to a human, and what
additional context a human could assess that the agent cannot.

## 6. Relevant X Accounts

Not yet verified in the current research record. This Section 4 research-file requirement remains incomplete.

## 7. Papers / Articles / Repositories / Datasets

Not yet verified in the current research record. No verified papers, articles,
repositories, or datasets are recorded in the current project materials, so the
five-reference requirement remains incomplete. No references are added here
without evidence that they were read and checked.

## 8. Questions I Want to Answer

These questions evolved from the initial research and subsequent synthetic
experimentation. They are not answered by real-world evidence:

1. How should an agent represent uncertainty when the underlying state cannot
   be directly observed?
2. When is additional evidence worth requesting?
3. Does evidence availability alone justify requesting evidence?
4. How does evidence cost affect the decision to request information?
5. When should an agent defer to a human?
6. How does the cost of an incorrect automated decision affect the selected
   action?
7. How sensitive is a threshold-based policy to its chosen threshold?
8. What happens when prior or likelihood assumptions are wrong?
9. How does a cost-aware policy distinguish among `PROCEED`,
   `REQUEST_EVIDENCE`, and `HUMAN_REVIEW`?
10. What limitations remain when the belief model is misspecified?

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

### Experiment-development prompts

Later prompts were used to implement and inspect sequential Bayesian updating,
synthetic decision costs, three competing policies, controlled case matrices,
policy evaluation, and deliberate break tests. They asked that synthetic
assumptions be labeled, hidden ground truth be kept out of policy inputs, and
the experiment avoid unsupported real-world claims. These prompts followed
the initial research and hypothesis; they were not part of the initial
research stage.

## 10. Initial Design Insight

The agent should not send every uncertain case directly to a human.
When uncertainty exists, it should first consider whether a specific
piece of additional evidence could meaningfully reduce the relevant
uncertainty at a reasonable cost.

If useful additional evidence is unavailable, too costly, or unlikely
to resolve the uncertainty, the agent should be able to defer the case
to a human.

This is an initial design hypothesis that will need to be tested.

### Important AI Errors

One issue identified during the initial research/design work: some AI
responses expanded the problem into full loan approval/rejection. The selected
Week 1 problem is narrower: `PROCEED`, `REQUEST_EVIDENCE`, or `HUMAN_REVIEW`.
The experiment kept this action space.

The experiment-development prompts also guarded against treating synthetic
probabilities and costs as real banking evidence.

### Initial Agent Policy Hypothesis

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

## 11. Research-to-Experiment Bridge

The initial research framed the problem as partial observability: the agent
sees transaction patterns but not their underlying context. That led to the
hidden-state and belief-state concepts, then to sequential Bayesian updates,
active evidence gathering, human deferral, and synthetic information-cost
comparisons. The project compared three policies in controlled synthetic
cases and deliberate break tests.

The initial design insight and policy idea above were hypotheses. They were
subsequently tested; they were not findings known at the start.

## 12. What the Experiment Added to the Research

### Observed in the synthetic experiment

- Policy 1 uses a fixed 30% concerning-probability threshold and does not
  account for evidence request cost.
- Policy 2 compares synthetic expected costs and changed actions when evidence
  request cost or human-review cost changed in the paired tests.
- The 29%, 30%, and 31% cases showed Policy 1 proceeding below its threshold
  and requesting evidence at and above the threshold.
- Break tests demonstrated sensitivity to prior and likelihood assumptions.
- Cost-aware action selection cannot correct a badly specified belief model.

These are observations from the constructed synthetic experiment, not
real-world loan underwriting findings or evidence that one policy is
generally superior. Detailed case results and the full failure analysis are
kept in the experiment artifacts and final README rather than repeated here.

### Limitations and possible follow-up

The experiment used deliberately constructed cases, synthetic hidden states,
probabilities, likelihoods, and costs. It did not use real banking data, model
reviewer errors, or validate lending performance. Possible future research
includes better-supported probability assumptions, broader evaluation, and a
formal POMDP formulation if the project requires it; none of these is claimed
as completed work.

### Terminology note

- **Bayesian update:** updating belief using evidence likelihoods.
- **Value of Information:** reasoning about whether additional information is
  worth its cost. The experiment uses a synthetic expected-cost comparison;
  it is not a validated real-world Value-of-Information estimate.
- **POMDP:** a possible formal framework for sequential decision-making under
  partial observability. The current implementation is not a full POMDP.
