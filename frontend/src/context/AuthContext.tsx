import { createContext, useContext, useState, type ReactNode, useEffect } from "react";

interface AuthContextType {
    isGoogleLoggedIn: boolean;
    setIsGoogleLoggedIn: (isGoogleLoggedIn: boolean) => void;
    hasAccount: boolean;
    setHasAccount: (hasAccount: boolean) => void;
    // isAuthenticated: boolean;
    // setIsAuthenticated: (isAuthenticated: boolean) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthContextProvider = ({ children }: { children: ReactNode }) => {
    const [isGoogleLoggedIn, setIsGoogleLoggedIn] = useState(false);
    const [hasAccount, setHasAccount] = useState(false);

    useEffect(() => {
        if (isGoogleLoggedIn) {
            setHasAccount(true);
        }
    }, [isGoogleLoggedIn]);

    return (
        <AuthContext.Provider value={{ isGoogleLoggedIn, setIsGoogleLoggedIn, hasAccount, setHasAccount }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuthContext = () => useContext(AuthContext);