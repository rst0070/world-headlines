import { createContext, useContext, useState, type ReactNode } from "react";

interface LanguageContextType {
    language: string; // en, original
    setLanguage: (language: string) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageContextProvider = ({ children }: { children: ReactNode }) => {
    const [language, setLanguage] = useState("en");

    return (
        <LanguageContext.Provider value={{ language, setLanguage }}>
            {children}
        </LanguageContext.Provider>
    );
}

export const useLanguageContext = () => useContext(LanguageContext);