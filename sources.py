

curve_gov_url = "https://gov.curve.fi/latest"
aave_gov_url = "https://governance.aave.com/latest"
uniswap_gov_url = "https://gov.uniswap.org/latest"
thegraph_gov_url = "https://forum.thegraph.com/latest"
lido_gov_url = "https://research.lido.fi/latest"
unslashed_gov_url = "https://forum.unslashed.finance/latest"
balancer_gov_url = "https://forum.balancer.fi/latest"
maker_gov_url = "https://forum.makerdao.com/latest"
kyber_gov_url = "https://gov.kyber.org/latest"
idle_gov_url = 'https://gov.idle.finance/latest'
badger_gov_url = 'https://forum.badger.finance/latest'
pooltogether_gov_url = 'https://gov.pooltogether.com/latest'
sushi_gov_url = "https://forum.sushi.com/latest"
_1inch_gov_url = "https://gov.1inch.io/latest"
yearn_gov_url = "https://gov.yearn.finance/latest"
synthetix_gov_url = "https://research.synthetix.io/"


#special ones:
compound_gov_url = "https://compound.finance/governance/" #to be developed
ox_gov_url = "https://blog.0x.org/tag/governance/" #to be developed
abracadabra_gov_url ="https://snapshot.org/#/abracadabrabymerlinthemagician.eth" #to be developed
dydx_gov_url = "https://forums.dydx.community/"#to be developed
convex_gov_url = "https://vote.convexfinance.com/#/" #to be developed

#working dict for urls
governance_urls={
'curve' : 'https://gov.curve.fi/latest',
'aave' : 'https://governance.aave.com/latest',
'uniswap' : 'https://gov.uniswap.org/latest',
'thegraph' : 'https://forum.thegraph.com/latest',
'lido' : 'https://research.lido.fi/latest',
'unslashed' : 'https://forum.unslashed.finance/latest',
'balancer' : 'https://forum.balancer.fi/latest',
'maker' : 'https://forum.makerdao.com/latest',
'kyber' : 'https://gov.kyber.org/latest',
'idle' : 'https://gov.idle.finance/latest',
'badger' : 'https://forum.badger.finance/latest',
'pooltogether' : 'https://gov.pooltogether.com/latest',
'sushi' : 'https://forum.sushi.com/latest',
'1inch' : 'https://gov.1inch.io/latest',
'yearn' : 'https://gov.yearn.finance/latest',
'bankless':'https://forum.bankless.community/',
'diversifi':'https://forum.deversifi.com/',
'gnosis' : 'https://forum.gnosis-safe.io/latest',
'nexus': 'https://forum.nexusprotocol.app/',
'maple':'https://community.maple.finance/latest',

}

#checks if url/project is in the dictionary governance_url

def in_gov_scope(item):
    
    item_=str(item)  
    if item_.lower() in governance_urls:
        
        return governance_urls.get(item_)
        
    else:
        return f"[Error]: Please check {item_}, it is not in scope."



