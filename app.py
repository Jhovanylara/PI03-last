
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import plost
import datetime
import time
from PIL import Image
import streamlit as st
from plotly.subplots import make_subplots




# Page settings
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# Open page style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



#texColor="#F0F2F6"

#Data read default
api_url= 'https://ftx.com/api'
market_name='BTC/USD'
Crypto='Bitcoin (BTC/USD)'
resolution=60*60*24 #seconds*minutes*hours

start_d=pd.to_datetime(2019-8-1)
date=start_d.strftime('%m/%d/%Y')
start=start_d.timestamp()


# Define sidebar
with st.sidebar:
    st.image(Image.open('FTX_logo.svg.png'),width=100)
    # Crypto market selection
    Crypto =st.selectbox(label='Select crypto market:', options=('Bitcoin (BTC/USD)', 
                                                'Ethereum (ETH/USD)',
                                                'Tether (USDT/USD)',
                                                'Serum (SRM/USD)',
                                                'Dogecoin (DOGE/USD)',
                                                'Polkadot (DOT/USD)',
                                                'Solana (SOL/USD)',
                                                'Binance (BNB/USD)',
                                                'Ripple payment net (XRP/USD)',
                                                'Shiba Inu (SHIB/USD)'))
    # resolution selection
    resolution_selected=st.selectbox(label='Select resolution:', options=('1 month' ,'1 week','1 day','1 hour'))
    
    #start date selection
    #start_date=st.date_input('Start date:',value=pd.to_datetime('2019-08-01'))
    #start_d=pd.to_datetime(start_date)
    
    #date=start_d.strftime('%m/%d/%Y')
    #start=start_d.timestamp()
          
    # st.markdown("<br></br>",unsafe_allow_html=True)

    #get market price
    #path=f'/markets/{market_name}'
    #url1=api_url+path
    #res= requests.get(url1).json()
    #df=pd.DataFrame(res)['result']
    #price=df.iloc[15]
    #last=df.iloc[11]
    #diference=f'{((price-last)/last)*100}%'
    
    #Asign value to market_name from selected Crypto
    if Crypto=='Bitcoin (BTC/USD)': market_name='BTC/USD'
    if Crypto== 'Ethereum (ETH/USD)':market_name='ETH/USD'
    if Crypto== 'Tether (USDT/USD)':market_name='USDT/USD'
    if Crypto== 'Serum (SRM/USD)':market_name='SRM/USD'
    if Crypto== 'Dogecoin (DOGE/USD)':market_name='DOGE/USD'
    if Crypto== 'Polkadot (DOT/USD)':market_name='DOT/USD'
    if Crypto== 'Solana (SOL/USD)':market_name='SOL/USD'
    if Crypto== 'Binance (BNB/USD)':market_name='(BNB/USD'
    if Crypto== 'Ripple payment net (XRP/USD)':market_name='XRP/USD'
    if Crypto== 'Shiba Inu (SHIB/USD)':market_name='SHIB/USD'

    #Asign value to resolution from resoluction selected 
    if resolution_selected=='1 hour': resolution=60*60
    if resolution_selected=='1 day': resolution=60*60*24
    if resolution_selected=='1 week': resolution=60*60*24*7
    if resolution_selected=='1 month': resolution=60*60*24*30
    
    #Get data
    def getData(market_name, resolution, start):

        #Get data from URL api
        path=f'/markets/{market_name}/candles?resolution={resolution}&start_time={start}'
        url=api_url+path

        historical = requests.get(url).json()
        historical = pd.DataFrame(historical['result'])
        historical['date']=pd.to_datetime(historical['startTime'])
        historical=historical.drop(columns=['startTime', 'time'])
        
        return (historical)
    

    historical=getData(market_name=market_name, resolution=resolution, start=start)
    
    
    price=historical['close'].iat[-1]
    last=historical['close'].iat[-2]
    
   
    diference=f'{round(((price-last)/last)*100,2)}%'
    

    #Calculator
    st.title('Calculator')
    Crypto_calculate=st.number_input('Crypto to USD:', min_value=0)
    dollars=Crypto_calculate*price
    st.text(f'${dollars} USD.')
    # st.markdown("<br></br>",unsafe_allow_html=True)
    Dollar_calculate=st.number_input('USD to crypto:', min_value=0)
    Crypto_c=Dollar_calculate/price
    st.text(f'{Crypto_c} coins.')



#Get variance value from dataframe
variance=historical['close'].var()


#Row A
a1,a2,a3=st.columns(3)
a1.metric("Crypto dashboard", market_name, )
a2.metric("Price", f'{price} USD.', diference)
a3.metric("Variance", int(variance))


# Adds variance columns to plot Media Average    
historical['variance']=historical['close'].rolling(window=2).mean().shift(1)

#Plot together candlestick, scatter, bar
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.3, 
               subplot_titles=("", "Volume"),
               row_width=[0.4 ,0.8])
               

fig.add_trace(go.Candlestick(name=market_name,x=historical['date'],
                open=historical['open'],
                high=historical['high'],
                low=historical['low'],
                close=historical['close']), row=1, col=1)

fig.add_trace(go.Scatter(name='MovAvg2',x=historical['date'],y=historical['variance'], line=dict(color='orange',width=1)),row=1, col=1)

fig.add_trace(go.Bar(name='Volume',x=historical['date'], y=historical['volume'], marker_color= 'green'), row=2, col=1)


fig.update_layout(
    title={'text':f'Historical data {market_name}','y':0.9,'x':0.5,'xanchor':'center','yanchor':'top'},
    yaxis_title="Price",
    width=800,
    height=500
    )

fig

st.caption(f'Short {Crypto} history:')
#Crypto info
if market_name=='BTC/USD':st.write("The history of bitcoin started with its invention and implementation by Satoshi Nakamoto, who integrated many existing ideas from the cryptography community. Over the course of bitcoins history, it has undergone rapid growth to become a significant store of value both on- and offline.From the mid-2010s, some businesses began accepting bitcoin in addition to traditional currencies.")
if market_name=='ETH/USD':st.write("Ether is the native cryptocurrency of the platform Etherium. Among cryptocurrencies, ether is second only to bitcoin in market capitalization.Ether (ETH) is the cryptocurrency generated in accordance with the Ethereum protocol as a reward to miners in a proof-of-work system for adding blocks to the blockchain.Additionally, ether is the only currency accepted by the protocol as payment for a transaction fee, which also goes to the miner. The block reward together with the transaction fees provide the incentive to miners to keep the blockchain growing.  Therefore, ETH is fundamental to the operation of the network.")
if market_name=='USDT/USD':st.write("Teher is an asset-backed cryptocurrency stablecoin. It was launched by the company Tether Limited Inc. in 2014. Tether is described as a stablecoin because it was originally designed to be valued at USD $1.00, with Tether Limited maintaining USD $1.00 of asset reserves for each USDT issued.In 2019, Tether surpassed Bitcoin in trading volume with the highest daily and monthly trading volume of any cryptocurrency on the market.")
if market_name=='SRM/USD':st.write("Serum is a fully decentralized ecosystem based on Solana. Its main focus is interoperability, and the highlight of its ecosystem is decentralibility. Serum offers an easy-to-use platform from which any crypto token can be exchanged for another without the need to go through any KYC procedures. Serum’s DEX uses the traditional swap system, allowing users to add any trading pairs they like. Since Serum is built on Solana’s blockchain, its DEX benefits from capabilities worthy of a centralized exchange while users retain full control of their funds. Thanks to its cross-chain features, you can trade BTC, ETH, ERC20 tokens and SPL tokens (Solana’s token standard), among others. These features allow DeFi users to find in Serum a truly decentralized platform, which has all the convenience offered by centralized platforms and more.")
if market_name=='DOGE/USD':st.write("Dogecoin (DOGE) is a peer-to-peer, open-source cryptocurrency. It is considered an altcoin and was launched in December 2013 with the image of a Shiba Inu dog as its logo. Dogecoin's blockchain has merit with its underlying technology derived from Litecoin. Notable features of Dogecoin, which uses a scrypt algorithm, are its low price and unlimited supply.With losses in 2018, Dogecoin lost much of its value but continues to have a core of supporters who trade it and use it to tip for content on Twitter and Reddit.")
if market_name=='DOT/USD':st.write("Polkadot idea is to “design a sharded version of Ethereum”. Parity Wallet hack and subsequent fundraising efforts Ten days after the token sale ended (Nov. 6, 2017), someone permanently froze the funds in the Parity multisig contract (the second such incident in a matter of months) compromising a little over $90 million worth of ETH equaling around 66% of Polkadot’s token sale proceeds. Polkadot, along with Parity, has petitioned the Ethereum community to consider finding a way to return to the funds, but the situation remains unresolved. Despite the lost funds, Polkadot and Web3 Foundation reported the project still had enough funds to meet its development milestones.")
if market_name=='SOL/USD':st.write("Solana's origins date back to late 2017 when founder Anatoly Yakovenko published a whitepaper draft detailing a new timekeeping technique for distributed systems called Proof of History (PoH). In blockchains like Bitcoin and Etheruem, one of the limitations to scalability is the time required to reach a consensus on the order of transactions. Anatoly believed his new technique could automate the transaction ordering process for blockchains, providing a key piece that would enable crypto networks to scale well-beyond their capabilities at the time.")
if market_name=='BNB/USD':st.write("Binance Coin (BNB) is a cryptocurrency that can be used to trade and pay fees on the Binance cryptocurrency exchange. The Binance Exchange is the largest cryptocurrency exchange in the world as of January 2018, facilitating more than 1.4 million transactions per second.Users of Binance Coin receive a discount in transaction fees on the Binance Exchange as an incentive. BNB can also be exchanged or traded for other cryptocurrencies, such as Bitcoin, Ethereum, Litecoin, etc.")
if market_name=='XRP/USD':st.write("XRP development begins from the observed waste inherent in mining. They sought to create a more sustainable system for sending value")
if market_name=='SHIB/USD':st.write("The Shiba Inu coin was created in August 2020 by an anonymous person named Ryoshi. Much like the situation with Bitcoin and Satoshi Nakamoto, we have no idea of the true identity of the creator. The Shiba Inu Coin has been in the limelight for a number of reasons, though its current value is not very high. However, the coin is taking over a lot of the crypto market and proving itself an excellent choice for investors. ")
#st.plotly_chart(fig2)


st.title('Crypto converter:')
#Row A
c1,c2,c3=st.columns(3)
with c1:
    From=st.selectbox(label='Select crypto to convert:', options=('Bitcoin (BTC)', 
                                                'Ethereum (ETH)',
                                                'Tether (USDT)',
                                                'Serum (SRM)',
                                                'Dogecoin (DOGE)',
                                                'Polkadot (DOT)',
                                                'Solana (SOL)',
                                                'Binance (BNB)',
                                                'Ripple payment net (XRP)',
                                                'Shiba Inu (SHIB'))
    market='BTC/USD'
    if From=='Bitcoin (BTC)': market='BTC/USD'
    if From== 'Ethereum (ETH)':market='ETH/USD'
    if From== 'Tether (USDT)':market='USDT/USD'
    if From== 'Serum (SRM)':market='SRM/USD'
    if From== 'Dogecoin (DOGE)':market='DOGE/USD'
    if From== 'Polkadot (DOT)':market='DOT/USD'
    if From== 'Solana (SOL)':market='SOL/USD'
    if From== 'Binance (BNB)':market='BNB/USD'
    if From== 'Ripple payment net (XRP)':market='XRP/USD'
    if From== 'Shiba Inu (SHIB)':market='SHIB/USD'

    path1=f'/markets/{market}/candles?resolution={resolution}&start_time={start}'
    url1=api_url+path1

    From1 = requests.get(url1).json()
    From1 = pd.DataFrame(From1['result'])
    From1['date']=pd.to_datetime(From1['startTime'])
    From1=From1.drop(columns=['startTime', 'time'])

    price_from=From1['close'].iat[-1]

with c2:
    To=st.selectbox(label='Select destination currency:', options=('Bitcoin (BTC)', 
                                                'Ethereum (ETH)',
                                                'Tether (USDT)',
                                                'Serum (SRM)',
                                                'Dogecoin (DOGE)',
                                                'Polkadot (DOT)',
                                                'Solana (SOL)',
                                                'Binance (BNB)',
                                                'Ripple payment net (XRP)',
                                                'Shiba Inu (SHIB)'))
    market1='BTC/USD'
    if To=='Bitcoin (BTC)': 
        market1='BTC/USD'
        unit='BTC'
    if To== 'Ethereum (ETH)':
        market1='ETH/USD'
        unit='ETH'
    if To== 'Tether (USDT)':
        market1='USDT/USD'
        unit='USDT'
    if To== 'Serum (SRM)':
        market1='SRM/USD'
        unit='SRM'
    if To== 'Dogecoin (DOGE)':
        market1='DOGE/USD'
        unit='DOGE'
    if To== 'Polkadot (DOT)':
        market1='DOT/USD'
        unit='DOT'
    if To== 'Solana (SOL)':
        market1='SOL/USD'
        unit='SOL'
    if To== 'Binance (BNB)':
        market1='BNB/USD'
        unit='BNB'
    if To== 'Ripple payment net (XRP)':
        market1='XRP/USD'
        unit='XRP'
    if To== 'Shiba Inu (SHIB)':
        market1='SHIB/USD'
        unit='SHIB'

    path2=f'/markets/{market1}/candles?resolution={resolution}&start_time={start}'
    url2=api_url+path2

    To1 = requests.get(url2).json()
    To1 = pd.DataFrame(To1['result'])
    To1['date']=pd.to_datetime(To1['startTime'])
    To1=To1.drop(columns=['startTime', 'time'])

    price_to=To1['close'].iat[-1]

with c3:
    Crypto_converter=st.number_input('Crypto amount:', min_value=0)
    dollars1=Crypto_converter*price_from
    result=round(dollars1/price_to,3)
    f'{result} {unit}.'
   
   