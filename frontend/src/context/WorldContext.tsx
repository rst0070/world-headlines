import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getCountryCodes } from "../services/api.country";

interface WorldContextType {
  countryCodes: string[];
}

const WorldContext = createContext<WorldContextType | undefined>(undefined);

export const WorldContextProvider = ({ children, initialCountryCodes }: { children: ReactNode, initialCountryCodes: string[] }) => {
    const [countryCodes, setCountryCodes] = useState<string[]>(initialCountryCodes);

    // if (countryCodes.length === 0) {
    //     getCountryCodes().then((codes) => {
    //         setCountryCodes(codes);
    //     });
    // }

    return (
        <WorldContext.Provider value={{ countryCodes }}>
            {children}
        </WorldContext.Provider>
    );
}

export const useWorldContext = () => useContext(WorldContext);