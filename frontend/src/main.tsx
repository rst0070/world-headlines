import { useState, useEffect, StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './style.css'
import Layout from './components/Layout.tsx'
import { getCountryCodes } from './services/api.country.ts'
import HomePage from './pages/HomePage.tsx'
import CountryPage from './pages/CountryPage.tsx'

function Root(){
  const [countryCodes, setCountryCodes] = useState<string[]>([])

  useEffect(() => {
    getCountryCodes().then(codes => {
      setCountryCodes(codes)
    })
  }, [])

  return (
    <BrowserRouter>
      <Layout countryCodes={countryCodes}>
        <Routes>
          <Route path="/" element={<HomePage countryCodes={countryCodes} />} />
          <Route path="/country/:countryCode" element={<CountryPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Root />
  </StrictMode>,
)
