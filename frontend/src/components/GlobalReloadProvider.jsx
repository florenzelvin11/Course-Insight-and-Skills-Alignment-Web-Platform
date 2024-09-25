import * as React from "react";
import { createContext, useContext, useState } from "react";

const GlobalReloadContext = createContext();

export function GlobalReloadProvider({ children }) {
  const [globalReload, setGlobalReload] = useState(false);

  return (
    <GlobalReloadContext.Provider value={{ globalReload, setGlobalReload }}>
      {children}
    </GlobalReloadContext.Provider>
  );
}

export function useGlobalState() {
  const context = useContext(GlobalReloadContext);

  return context;
}
