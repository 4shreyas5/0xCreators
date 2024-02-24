import smartpy as sp

@sp.module
def main():
    balance_of_args: type = sp.record(
        requests=sp.list[sp.record(owner=sp.address, token_id=sp.nat)],
        callback=sp.contract[
            sp.list[
                sp.record(
                    request=sp.record(owner=sp.address, token_id=sp.nat), balance=sp.nat
                ).layout(("request", "balance"))
            ]
        ],
    ).layout(("requests", "callback"))

    class Fa2NftMinimal(sp.Contract):

        def __init__(self, administrator, metadata):
            self.data.administrator = administrator
            self.data.ledger = sp.cast(sp.big_map(), sp.big_map[sp.nat, sp.address])
            self.data.metadata = metadata
            self.data.next_token_id = sp.nat(0)
            self.data.operators = sp.cast(
                sp.big_map(),
                sp.big_map[
                    sp.record(
                        owner=sp.address,
                        operator=sp.address,
                        token_id=sp.nat,
                    ).layout(("owner", ("operator", "token_id"))),
                    sp.unit,
                ],
            )
            self.data.token_metadata = sp.cast(
                sp.big_map(),
                sp.big_map[
                    sp.nat,
                    sp.record(token_id=sp.nat, token_info=sp.map[sp.string, sp.bytes]),
                ],
            )


        @sp.entrypoint
        def transfer(self, batch):
            for transfer in batch:
                for tx in transfer.txs:
                    sp.cast(
                        tx,
                        sp.record(
                            to_=sp.address, token_id=sp.nat, amount=sp.nat
                        ).layout(("to_", ("token_id", "amount"))),
                    )
                    assert tx.token_id < self.data.next_token_id, "FA2_TOKEN_UNDEFINED"
                    assert transfer.from_ == sp.sender or self.data.operators.contains(
                        sp.record(
                            owner=transfer.from_,
                            operator=sp.sender,
                            token_id=tx.token_id,
                        )
                    ), "FA2_NOT_OPERATOR"
                    if tx.amount > 0:
                        assert (
                            tx.amount == 1
                            and self.data.ledger[tx.token_id] == transfer.from_
                        ), "FA2_INSUFFICIENT_BALANCE"
                        self.data.ledger[tx.token_id] = tx.to_

        @sp.entrypoint
        def update_operators(self, actions):
            for action in actions:
                with sp.match(action):
                    with sp.case.add_operator as operator:
                        assert operator.owner == sp.sender, "FA2_NOT_OWNER"
                        self.data.operators[operator] = ()
                    with sp.case.remove_operator as operator:
                        assert operator.owner == sp.sender, "FA2_NOT_OWNER"
                        del self.data.operators[operator]

        @sp.entrypoint
        def balance_of(self, param):
            sp.cast(param, balance_of_args)
            balances = []
            for req in param.requests:
                assert req.token_id < self.data.next_token_id, "FA2_TOKEN_UNDEFINED"
                balances.push(
                    sp.record(
                        request=sp.record(owner=req.owner, token_id=req.token_id),
                        balance=(
                            1 if self.data.ledger[req.token_id] == req.owner else 0
                        ),
                    )
                )

            sp.transfer(reversed(balances), sp.mutez(0), param.callback)

        @sp.entrypoint
        def mint(self, to_, metadata):
            assert sp.sender == self.data.administrator, "FA2_NOT_ADMIN"
            token_id = self.data.next_token_id
            self.data.token_metadata[token_id] = sp.record(
                token_id=token_id, token_info=metadata
            )
            self.data.ledger[token_id] = to_
            self.data.next_token_id += 1

        @sp.offchain_view
        def all_tokens(self):
            return range(0, self.data.next_token_id)

        @sp.offchain_view
        def get_balance(self, params):
            sp.cast(
                params,
                sp.record(owner=sp.address, token_id=sp.nat).layout(
                    ("owner", "token_id")
                ),
            )
            assert params.token_id < self.data.next_token_id, "FA2_TOKEN_UNDEFINED"
            return (
                sp.nat(1)
                if self.data.ledger[params.token_id] == params.owner
                else sp.nat(0)
            )

        @sp.offchain_view
        def total_supply(self, params):
            assert params.token_id < self.data.next_token_id, "FA2_TOKEN_UNDEFINED"
            return 1

        @sp.offchain_view
        def is_operator(self, params):
            return self.data.operators.contains(params)

    class Fa2NftMinimalTest(Fa2NftMinimal):
        def __init__(
            self, administrator, metadata, ledger, token_metadata, next_token_id
        ):
            Fa2NftMinimal.__init__(self, administrator, metadata)

            self.data.next_token_id = next_token_id
            self.data.ledger = ledger
            self.data.token_metadata = token_metadata


if "main" in __name__:

    def make_metadata(symbol, name, decimals):
        return sp.map(
            l={
                "decimals": sp.scenario_utils.bytes_of_string("%d" % decimals),
                "name": sp.scenario_utils.bytes_of_string(name),
                "symbol": sp.scenario_utils.bytes_of_string(symbol),
            }
        )

    admin = sp.test_account("Administrator")
    alice = sp.test_account("Alice")
    tok0_md = make_metadata(name="Token Zero", decimals=1, symbol="Tok0")
    tok1_md = make_metadata(name="Token One", decimals=1, symbol="Tok1")
    tok2_md = make_metadata(name="Token Two", decimals=1, symbol="Tok2")

    @sp.add_test()
    def test():
        scenario = sp.test_scenario("Minimal test", main)
        c1 = main.Fa2NftMinimal(
            admin.address, sp.scenario_utils.metadata_of_url("https://example.com")
        )
        scenario += c1

    from smartpy.templates import fa2_lib_testing as testing

    kwargs = {
        "class_": main.Fa2NftMinimalTest,
        "kwargs": {
            "administrator": admin.address,
            "metadata": sp.scenario_utils.metadata_of_url("https://example.com"),
            "ledger": sp.big_map(
                {0: alice.address, 1: alice.address, 2: alice.address}
            ),
            "token_metadata": sp.big_map(
                {
                    0: sp.record(token_id=0, token_info=tok0_md),
                    1: sp.record(token_id=1, token_info=tok1_md),
                    2: sp.record(token_id=2, token_info=tok2_md),
                }
            ),
            "next_token_id": 3,
        },
        "ledger_type": "NFT",
        "test_name": "",
        "modules": main,
    }

    testing.test_core_interfaces(**kwargs)
    testing.test_transfer(**kwargs)
    testing.test_balance_of(**kwargs)
    testing.test_owner_or_operator_transfer(**kwargs)

#KT1Q9q9qA9wTE1s1sAEW4KS8XzVyGvvN17c9