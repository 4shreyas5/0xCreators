import React, { useState, useEffect } from "react";
import { connectWallet, getAccount, wallet } from "./utils/wallet";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Components
import Navbar from "./components/Navbar";
import Home from "./components/Home";
import Members from "./components/Members";

const App: React.FC = () => {
  const [isWalletConnected, setIsWalletConnected] = useState(false);

  useEffect(() => {
    const checkWallet = async () => {
      try {
        await connectWallet();
        setIsWalletConnected(true);
      } catch (error) {
        console.error("Error connecting wallet:", error);
      }
    };

    checkWallet();
  }, []);

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/members" element={<Members/>}/>
      </Routes>
    </Router>
  );
};

export default App;
