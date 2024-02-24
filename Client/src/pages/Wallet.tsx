import React, { useState } from "react";
import { TezosToolkit } from "@taquito/taquito";

import ConnectButton from "../components/ConnectWallet";
import DisconnectButton from "../components/DisconnectWallet";
import qrcode from "qrcode-generator";
import UpdateContract from "../components/UpdateContract";
import Transfers from "../components/Transfers";




const Wallet=()=>{
    enum BeaconConnection {
        NONE = "",
        LISTENING = "Listening to P2P channel",
        CONNECTED = "Channel connected",
        PERMISSION_REQUEST_SENT = "Permission request sent, waiting for response",
        PERMISSION_REQUEST_SUCCESS = "Wallet is connected",
      }

      const [Tezos, setTezos] = useState<TezosToolkit>(
        new TezosToolkit("https://ghostnet.ecadinfra.com")
      );
      const [contract, setContract] = useState<any>(undefined);
      const [publicToken, setPublicToken] = useState<string | null>(null);
      const [wallet, setWallet] = useState<any>(null);
      const [userAddress, setUserAddress] = useState<string>("");
      const [userBalance, setUserBalance] = useState<number>(0);
      const [storage, setStorage] = useState<number>(0);
      const [copiedPublicToken, setCopiedPublicToken] = useState<boolean>(false);
      const [beaconConnection, setBeaconConnection] = useState<boolean>(false);
      const [activeTab, setActiveTab] = useState<string>("transfer");
    
      // Ghostnet Increment/Decrement contract
      const contractAddress: string = "KT1QMGSLynvwwSfGbaiJ8gzWHibTCweCGcu8";
    
      const generateQrCode = (): { __html: string } => {
        const qr = qrcode(0, "L");
        qr.addData(publicToken || "");
        qr.make();
    
        return { __html: qr.createImgTag(4) };
      };


    return<>
     <div className="main-box">
        <div className="title">
          <h1>NFT GATING WEBSITE</h1>
          </div>
        <div id="dialog">
          <header>Welcome to the NFT Gating Website</header>
          <div id="content">
            <p>Hello!</p>
            <p>
              Connect the wallet to access the website
              <br />
              </p>
              </div>
              <ConnectButton
            Tezos={Tezos}
            setContract={setContract}
            setPublicToken={setPublicToken}
            setWallet={setWallet}
            setUserAddress={setUserAddress}
            setUserBalance={setUserBalance}
            setStorage={setStorage}
            contractAddress={contractAddress}
            setBeaconConnection={setBeaconConnection}
            wallet={wallet}
          />
        </div>
        </div>
    </>
}

export default Wallet;