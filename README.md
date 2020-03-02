# 1. Génération de clé
La génération de clés a été mise en place avec une seed = 0 (fichier keys.py), le processus de création est le suivant :
### 1.1. Génération d'une clé privée aléatoire (avec un random), on y ajoute le bon préfixe pour le testnet ('0xef') ou le mainnet ('0x80')
### 1.2. Calcul de la liste de mot à partir de cette clé privée
### 1.3. Calcul de la clé publique et de l'adresse correspondante
Bitcoin utilise spec256k1 pour obtenir la clé publique. 
Pour obtenir l'adresse, on hash deux fois la clé publique, d'abord avec SHA256 puis RIPEMD360, puis on y ajoute le préfixe du réseau souhaité (mainnet ou testnet) et un suffixe correspondant au checksum de cette adresse. Enfin, on encode en base58 pour obtenir l'adresse.
### 1.4. Calcul du WIF à partir de la clé privée
Correspond à un double hash 256 de la clé privée, auquel on ajoute le préfixe du réseau souhaité puis un suffixe correspondant au checksum de la clé. Enfin on encode en base58 pour obtenir la clé WIF

### 1.5. Résultat
```sh
get_keys_w_seed(0)
```
Output :
```sh
Private key : c5d71484f8cf9bf4b76f47904730804b9e3225a9f133b5dea168f4e2851f072f
Words : quitter physique botte tumulte vétuste victoire sirop taxer littoral couvrir boiser matériel styliste aspirer nuisible cachette pénétrer vacarme espoir tension campagne lionceau biberon trancher
Public key : 043bb41cf878973e10da570d5aca731d24adb02533fdf69e0ccf69e07a3a1e3ea57a9a9273623c38c8a27348843b4ed434096b5dff817cd9d8671869fd736af058
WIF : 9363iyQYqSejRUQgFTdjWzahrDJYFk2g3pTbc49LL6y1ZGoy3bi
Public Address : mvPuJFmdE3iv8xJgB9cwDzogsGV369Jz63
```

# 2. Transaction

### 2.1. Création d'une adresse multisig'
```sh
bitcoin-cli -testnet createmultisig 2 '["02e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff34","02c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f07","03f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d94"]'
```
Output :
```sh
{
  "address": "2N6TdNCysspNgxoEt8Npsqc2KDuJ4W1zvTL",
  "redeemScript": "522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453ae"
}
```

### 2.2. Alimente cette adresse en bitcoin et création d'une raw transaction
Pour alimenter cette adresse, j'utilise une UTXO de mon wallet electrum. On trouve toutes les infos nécessaires à la requête createrawtransaction ici :
https://api.blockcypher.com/v1/btc/test3/txs/05a62d7727d237f249f86ae3eb6a255a3c5cd40a406065e2c64292d311e75d30?limit=50&includeHex=true
```sh
bitcoin-cli -testnet createrawtransaction '[{"txid":"05a62d7727d237f249f86ae3eb6a255a3c5cd40a406065e2c64292d311e75d30","vout":0,"scriptPubKey":"a91490f224460e4fd1015baf429c229d6bb5e464413587","redeemScript":"522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453ae"}]' '{"tb1q9yw25trkqlzrrju38c6wy8rqr4qlnrf4j0h5xt":0.01}'
```
Output:
```sh
0200000001305de711d39242c6e26560400ad45c3c5a256aebe36af849f237d227772da6050000000000ffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000
```

### 2.3. Signature de la transaction
On utilise une des clés privées générant l'adresse multisig pour signer la transction
```sh
bitcoin-cli -testnet signrawtransactionwithkey '0200000001305de711d39242c6e26560400ad45c3c5a256aebe36af849f237d227772da6050000000000ffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000' '["cStuGJkCJkjUX4naKB5E8MWJNFVgCLLXDFuns7rbCN16KrY9iNdE"]' '[{"txid":"05a62d7727d237f249f86ae3eb6a255a3c5cd40a406065e2c64292d311e75d30","vout":0,"scriptPubKey":"a91490f224460e4fd1015baf429c229d6bb5e464413587","redeemScript":"522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453ae"}]'
```
Output:
```sh
{
  "hex": "0200000001305de711d39242c6e26560400ad45c3c5a256aebe36af849f237d227772da60500000000b50047304402200cdd01ea4db19c578c0fb09b517bc72cd215dd87f5cd0c6e4295136285b6b72502206c790ef84d16a1835cc4c506e854b620635f4f25cf2c43f6000da5b2107aa4cf01004c69522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453aeffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000",
  "complete": false,
  ... etc,
}
```
Cela génère une erreur, qui nous prévient que la transaction n'est pas encore valide (il est nécessaire de la signer 2 fois puisque c'est une 2 sur 3 multisig). On reprend l'hex de la transaction signée une première fois et on signe avec une autre clé.
```sh
bitcoin-cli -testnet signrawtransactionwithkey '0200000001305de711d39242c6e26560400ad45c3c5a256aebe36af849f237d227772da60500000000b50047304402200cdd01ea4db19c578c0fb09b517bc72cd215dd87f5cd0c6e4295136285b6b72502206c790ef84d16a1835cc4c506e854b620635f4f25cf2c43f6000da5b2107aa4cf01004c69522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453aeffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000' '["cPVXpU3axwSWptbppzkVKL1Ep8jLqrcxSsiNnqyDfkwu9z9xUArK"]' '[{"txid":"05a62d7727d237f249f86ae3eb6a255a3c5cd40a406065e2c64292d311e75d30","vout":0,"scriptPubKey":"a91490f224460e4fd1015baf429c229d6bb5e464413587","redeemScript":"522103be9ab01b98f61bc85beaf6e442115c07136ddac6fb55778d62846758929e19142102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453ae"}]'

```
Output:
```sh
{
  "hex": "0200000001305de711d39242c6e26560400ad45c3c5a256aebe36af849f237d227772da60500000000fc004730440220114a5bfee1abed50d0085fd05530b45315257f0076f1ae54fc2b355988cfa52a022023887ff7cd17d273db5915aa44215db4a9c8062cb37aa413002b5c147970edd30147304402200cdd01ea4db19c578c0fb09b517bc72cd215dd87f5cd0c6e4295136285b6b72502206c790ef84d16a1835cc4c506e854b620635f4f25cf2c43f6000da5b2107aa4cf014c69522102e8c3591920ea995332889ff3b66df83b5a26fb9cd6ab10d78e54909e2892ff342102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453aeffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000",
  "complete": true
}
```

### 2.4. Envoi de la transaction sur le réseau
```sh
bitcoin-cli -testnet sendrawtransaction 020000000118d256339e320ef6c97fcc26c991857e12b1dceecebae53e0a681daae9c5291400000000fc004730440220219574f9fc29735f0d00d89b5ca1ac5d2467243cc4f5b9bfaaad152f548e1fa902204abf62325616bedbeb7a9dd9d346f4e1d2f17a6c41d58ebb801d34681ba68cba01473044022011a8cbf7b3be462a708b2aba8683ec9e58a7fa11a180e948ccbf57e1c1c4b89b02203c8f6391d72b8000c0ea2135e982fe56ef8bb7d6b072654441804aea185b9964014c69522103be9ab01b98f61bc85beaf6e442115c07136ddac6fb55778d62846758929e19142102c522ba9d5063c526c46c5750f22c96d0593c40537e19dc3ffd41a98914f39f072103f587bc04d50edd8a4c1e99f9cdb503e0e55e354b97d7ed9f79017f0c42589d9453aeffffffff0140420f0000000000160014291caa2c7607c431cb913e34e21c601d41f98d3500000000
```
Output:
```sh
25cdf0f32318db8744e8796e85cb0641c68cfd3d28d7f75779616c6a0562ad3a
```

### 2.5. Visualisation
On peut voir la transaction sur https://live.blockcypher.com/btc-testnet/tx/25cdf0f32318db8744e8796e85cb0641c68cfd3d28d7f75779616c6a0562ad3a/
