# Solana Gasless Research

Tools to calculate stats about wallets with no SOL

----

Sometimes, a friend sends you some USDC for you to experiment with crypto.
Usually, you can't start transacting with it right away: you need native token of the network.
You can't exchange USDC to SOL on a DEX or move it to another wallet — either of these transactions requires SOL at the first place.

[Octane](https://github.com/solana-labs/octane) gasless relayer solves this problem. It allows to pay for transaction
fees in SOL and execute swaps of tokens to SOL without having any SOL.

This repo aggregates tools for research about the tokens-with-no-SOL problem. How common are transfers to wallets without SOL?
How many users Octane integration to a wallet will impact? Which SPL tokens should Octane accept?

## Stats

_Transfers using Token Program, excluding CPI (so, swaps are not counted). Period: 30 days before September 5th, 2022. Approximated using a sample 0.1% of blocks._

| Mint | Transfers | Transfers to no-SOL wallets | No-SOL wallets ratio | Comment
| ---- | --------- | --------------------------- | ------------- | -------
| kinXdEcpDQeHPEuQnqmUgtYykqKGVFq6CeVX5iAHJq6 | 19,933,000 |  13,106,000 | 65% | Kin Foundation. There is already infrastructure to pay transaction fees using KIN within Kin ecosystem.
| AFbX8oGjGpmVFywbVouvhQSRmiW2aR1mohfahi4Y2AdB | 1,156,000 | 83,000 | 7% | StepN's native token
| EcQCUYv57C4V6RoPxkVUiDwtX1SP8y8FP5AEToYL8Az | 935,000 | 166,000 | 17% | Walken NFT game
| CKaKtYvz6dKPyMvYq9Rh3UBrnNqYZAyd7iF4hJtjUvks | 856,000 | 805,000 | 94% | Chingari app's native token
| EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v | 536,000 | 217,000 | 40% | USDC
| 7i5KKsX2weiTkry7jA4ZwSuXGhs5eJBEjY8vVxR4pfRx | 273,000 | 9,000 | 3% | GMT Token
| Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB | 150,000 | 44,000 | 29% | USDT
| DkNihsQs1hqEwf9TgKP8FmGv7dmMQ7hnKjS2ZSmMZZBE | 98,000 | 96,000 | 97% | Quiztok's native token
| 4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R | 51,000 | 13,000 | 25% | Raydium
| 6tAmokk5fqrjm4ho2JerziBsiV3hYzgJZnG6sFXZNXZs | 46,000 | 46,000 | 100% | Grepper's native token


### Notes

1. A high percent of No-SOL wallets for tokens like USDC and USDT might be caused by transfers to accounts owned by exchanges.
2. Calculations are approximate and are based on a tiny subset of blocks.
3. Source JSON files include also approximations on unique wallets. However, there is no reliable way to extrapolate uniques over a sample, so these numbers aren't included here.

You can view the source data as [JSON](https://github.com/sevazhidkov/octane-gasless-research/blob/main/transfers_within_30_days_step_1000_blocks.json) and in [Google Sheets](https://docs.google.com/spreadsheets/d/1uZvy9PBzKhEctgUhii5TmcH-MXbocAnmHelIwJ5VADY/edit?usp=sharing).


# Contributing

Feel free to calculate other stats about no-SOL wallets and include them here. You can also calculate these metrics over a larger dataset increasing the precision or build a simple indexer to calculate these values over all blocks.
