const express = require('express');
const { TezosToolkit } = require('@taquito/taquito');

const app = express();
const Port = 3000;
const contractAddress = "KT1XXtrvjvVmh9FLCLh438s6r9VAUyudMrHN";

// Initialize TezosToolkit
const tezos = new TezosToolkit("https://ghostnet.smartpy.io");

async function initializeContract() {
    try {
        const contract = await tezos.contract.at(contractAddress);
        return contract; // Return the contract instance
    } catch (error) {
        console.error('Error initializing contract:', error);
        return null;
    }
}

initializeContract().then((contract) => {
    if (contract) {
        fetchNFTs(contract);
    }
});

const fetchNFTs = async (contract) => {
    try {
        const nftsBalance = await contract.methods.balance_of([
            { owner: "tz1g1XsJRH8N5PXdvpCyQDFZhrTpBQAA3Z7o", token_id: 0 }
        ]);
        const mint = await contract.methods.mint("tz1g1XsJRH8N5PXdvpCyQDFZhrTpBQAA3Z7o",['shreyas',])
        console.log('NFTs Balance:', nftsBalance);
    } catch (error) {
        console.error('Error fetching NFTs:', error);
    }
}

app.listen(Port, () => {
    console.log(`Server is running at ${Port}`);
});
