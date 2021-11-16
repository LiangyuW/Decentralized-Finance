
import config
from flask import Flask, render_template, request, flash, redirect
from web3 import Web3
import ccxt
import time

app=Flask(__name__)
w3=Web3(Web3.HTTPProvider(config.INFURA_URL))


@app.route("/")
def index():
    eth = w3.eth

    binance=ccxt.binance()
    eth_price=binance.fetch_ticker('ETH/USDC')

    last_blocks=[]
    for blk_number in range(w3.eth.block_number, w3.eth.block_number-10, -1):
        block=w3.eth.get_block(blk_number)
        last_blocks.append(block)

    last_trans=[]
    for tx in last_blocks[-1]['transactions'][-10:]:
        tran=w3.eth.get_transaction(tx)
        last_trans.append(tran)
    
    cur_time=time.time()

    return render_template("index.html", 
    miners=config.MINERS,
    eth=eth,
    cur_time=cur_time,
    eth_price=eth_price, 
    last_blocks=last_blocks,
    last_trans=last_trans)

@app.get("/tx/<hash>")
def transaction(hash):
    tx=w3.eth.get_transaction(hash)
    value=w3.fromWei(tx.value, 'ether')
    receipt=w3.eth.get_transaction_receipt(hash)
    binance=ccxt.binance()
    eth_price=binance.fetch_ticker('ETH/USDC')
    gas_price=w3.fromWei(tx.gasPrice, 'ether')
    return render_template("transaction.html",
        tx=tx, value=value, receipt=receipt,
        gas_price=gas_price, eth_price=eth_price)

@app.get("/address")
def address():

    addr=request.args.get('address')
    binance=ccxt.binance()
    eth_price=binance.fetch_ticker('ETH/USDC')

    try:
        address=w3.toChecksumAddress(addr)
    except:
        flash('Invalid ethereum address', 'danger')
        return redirect('/')

    balance=w3.eth.get_balance(addr)
    balance=w3.fromWei(balance, 'ether')

    return render_template("address.html", eth_price=eth_price, addr=addr, balance=balance)

@app.get("/block/<blk_number>")
def block(blk_number):
    block=w3.eth.get_block(int(blk_number))
    return render_template("block.html", block=block)

app.run()