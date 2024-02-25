
import React, { useEffect, useState } from "react";
import { connectWallet, getAccount } from "../utils/wallet";

const Navbar: React.FC = () => {
  const [account, setAccount] = useState<string>("");
  const [active,setActive] = useState(false);

  const onConnectWallet = async () => {
    await connectWallet();
    const account = await getAccount();
    setAccount(account);
  };


  const isActive = () => {
      window.scrollY > 0 ? setActive (true) : setActive(false);
  }

  return (
    <div className={ "navbar" }>
    <div className='container'>
        <div className='logo'>
            <span className='text'>NFT Gating</span>
            <span className='dot'>...</span>
        </div>
            <span><button
          onClick={onConnectWallet}
          className={ "button px-6 py-2 rounded-sm text-xs font-semibold text-white cursor-pointer"}
        >
          💳{" "}
          {account
            ? account.slice(0, 4) +
              "..." +
              account.slice(account.length - 4, account.length)
            : "Connect"}
          </button></span>
        </div>
    </div>    
  );
}
export default Navbar
