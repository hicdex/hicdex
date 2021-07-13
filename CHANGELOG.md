# `v1.2.0`

* Add `english_auction.hash` and `dutch_auction.hash`

# `v1.1.1`

* Fix a bug in `holder.description` indexing

# `v1.1.0`

* [Retry failed requests](https://github.com/dipdup-net/dipdup-py/pull/81)
* Add `holder.description`, normalizing subjkt's metadata `description` field

# `v1.0.0`

### `swap`

* Add boolean `swap.is_valid`, `false` indicates a swap with a token creator different than the objkt creator or with royalties different than objkt royalties
