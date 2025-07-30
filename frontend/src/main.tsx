import { useState, useEffect, StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './style.css'
import Layout from './components/Layout.tsx'
import { getCountryCodes } from './services/api.country.ts'
import HomePage from './pages/HomePage.tsx'
import CountryPage from './pages/CountryPage.tsx'
import SigninPage from './pages/SigninPage.tsx'
import SignupPage from './pages/SignupPage.tsx'
import { GoogleOAuthProvider } from '@react-oauth/google';
import { LanguageContextProvider } from './context/LanguageContext.tsx'
import { AuthContextProvider } from './context/AuthContext.tsx'

function Root(){
  const [countryCodes, setCountryCodes] = useState<string[]>([])

  useEffect(() => {
    getCountryCodes().then(codes => {
      setCountryCodes(codes)
    })
  }, [])

  return (
    <BrowserRouter>
      <GoogleOAuthProvider clientId={"757383812276-ihavvt4e4spspv5hr2fgdnpuij2sei2k.apps.googleusercontent.com"}>
        <AuthContextProvider>
          <LanguageContextProvider>
            <Layout>
              <Routes>
                <Route path="/" element={<HomePage countryCodes={countryCodes} />} />
                <Route path="/country/:countryCode" element={<CountryPage />} />
                <Route path="/signin" element={<SigninPage />} />
                <Route path="/signup" element={<SignupPage />} />
              </Routes>
            </Layout>
          </LanguageContextProvider>
        </AuthContextProvider>
      </GoogleOAuthProvider>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)
