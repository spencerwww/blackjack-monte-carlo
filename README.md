# Blackjack Monte Carlo Simulation Engine

## Overview
This project implements a rule-configurable blackjack simulation engine in Python and uses Monte Carlo methods to evaluate the expected value (EV), variance, and risk characteristics of different playing and betting strategies under stochastic uncertainty.

The focus of the project is correctness, system design, and statistical evaluation, rather than UI or gameplay. Blackjack is used as a controlled probabilistic environment with known structure to study decision-making, simulation accuracy, and strategy performance.

## Key Projected Features
- Modular game engine

  - Clean separation between game logic, rules, strategies, and simulation

  - Event-driven hand resolution (hit, stand, double, split, insurance, surrender)

- Rule configurability

  - Number of decks

  - Dealer S17 / H17 behavior

  - Blackjack payout

  - Double, split, and surrender rules

  - Shoe cut-card randomization

- Strategy abstraction

  - Pluggable strategy interface

  - Supports basic strategy, card counting, deviation and betting policies

  - Manual action driver for engine validation

- Monte Carlo simulation

  - Large-scale repeated trials

  - Empirical estimation of EV and variance

  - Designed for convergence and sensitivity analysis

- Testing & validation

  - Unit tests for deterministic components (hand evaluation, actions, payouts)

  - Manual scenario driving for edge-case validation

  - Randomness isolated from core logic

## Engine Design

The engine models blackjack as a stateful stochastic process:

- `Shoe`: card generation, shuffling, cut-card logic

- `Hand`: card state, hand value (soft/hard), bet tracking

- `Game`: state transitions and action handling

- `Rules`: encapsulates table-specific constraints

Actions (`hit`, `stand`, `double`, `split`, `insurance`, `surrender`) mutate game state deterministically, enabling precise testing and reproducibility.

## Simulation Methodology

Strategies are evaluated via Monte Carlo simulation:

1. Initialize game with fixed rules and shoe configuration

2. Repeatedly simulate independent rounds

3. Record PnL per round

4. Estimate:

   - Expected value (EV)

   - Variance

   - Distributional behavior

5. Analyze convergence as the number of trials increases

This mirrors the structure of backtesting and risk simulation in financial systems.