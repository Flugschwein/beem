from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from beem import Steem
from beem.amount import Amount
from beem.witness import Witness
from beem.account import Account
from beem.instance import set_shared_steem_instance, shared_steem_instance, set_shared_config
from beem.blockchain import Blockchain
from beem.block import Block
from beem.market import Market
from beem.price import Price
from beem.comment import Comment
from beem.vote import Vote
from beemapi.exceptions import RPCConnection
from beem.wallet import Wallet
from beem.transactionbuilder import TransactionBuilder
from beembase.operations import Transfer
from beemgraphenebase.account import PasswordKey, PrivateKey, PublicKey
from beem.utils import parse_time, formatTimedelta
from beem.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "STM"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(steem_instance=Steem(node=cls.nodelist.get_nodes(hive=True), num_retries=10))
        stm = Steem(node=cls.nodelist.get_nodes(hive=True))
        stm.config.refreshBackup()
        stm.set_default_nodes(["xyz"])
        del stm

        cls.urls = cls.nodelist.get_nodes(hive=True)
        cls.bts = Steem(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_steem_instance(cls.bts)
        acc = Account("fullnodeupdate", steem_instance=cls.bts)
        comment = Comment(acc.get_blog_entries(limit=20)[-1], steem_instance=cls.bts)
        cls.authorperm = comment.authorperm
        votes = comment.get_votes()
        last_vote = votes[-1]
        cls.authorpermvoter = comment['authorperm'] + '|' + last_vote["voter"]

    @classmethod
    def tearDownClass(cls):
        stm = Steem(node=cls.nodelist.get_nodes())
        stm.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.blockchain.rpc.url, self.urls)
            self.assertIn(acc["balance"].blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            acc = Account("test", steem_instance=stm)
            self.assertIn(acc.blockchain.rpc.url, self.urls)
            self.assertIn(acc["balance"].blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            stm = Steem(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_steem_instance(self.bts)
            o = Amount("1 %s" % self.bts.backed_token_symbol)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 %s" % self.bts.backed_token_symbol, steem_instance=stm)
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Amount("1 %s" % self.bts.backed_token_symbol, steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 %s" % self.bts.backed_token_symbol)

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Block(1)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Block(1, steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Blockchain(steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Comment(self.authorperm, steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Market()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Market(steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol))
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol), steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol), steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "%s/%s" % (self.bts.token_symbol, self.bts.backed_token_symbol))

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Vote(self.authorpermvoter, steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Wallet()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
                o.blockchain.get_config()
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Wallet(steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.blockchain.get_config()

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Witness("gtg", steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(steem_instance=Steem(node="https://abc.d", autoconnect=False, num_retries=1))
                o.blockchain.get_config()
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = TransactionBuilder(steem_instance=stm)
            self.assertIn(o.blockchain.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.blockchain.get_config()

    @parameterized.expand([
        ("instance"),
        ("steem")
    ])
    def test_steem(self, node_param):
        if node_param == "instance":
            set_shared_steem_instance(self.bts)
            o = Steem(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = Steem(node="https://abc.d", autoconnect=False, num_retries=1)
                stm.get_config()
        else:
            set_shared_steem_instance(Steem(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = stm
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = shared_steem_instance()
                stm.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_steem_instance(None)
        o = shared_steem_instance()
        self.assertIn(o.rpc.url, self.urls)
