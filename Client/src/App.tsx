import React, { useState, useEffect } from "react";
import { connectWallet, getAccount } from "./utils/wallet";
import {createBrowserRouter,RouterProvider,Routes, Route } from "react-router-dom";

// Components
import Navbar from "./components/Navbar";
// import Home from "./components/Home";


const App: React.FC = () => {
  const [acc] = useState<string>("");
  const onConnectWallet = async () => {
    await connectWallet();
    const acc = await getAccount();
  };


  return(
  <>
  <Navbar/>

  </>
  )

};

export default App;
